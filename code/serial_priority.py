"""
Serial branch-and-bound algorithm for constructing rule lists.

Input files:

    label_file : string, e.g.,'tdata_R.label'

        Path to space-delimited text file containing two rows and (ndata + 1)
        columns.  Each row indicates which of the ndata training data points
        have a particular label; since the labels are binary, the two rows
        contain equivalent binary information (they are inverses).  The two
        entries in the first column are the strings `{label=0}` and `{label=1}`,
        and the remaining entries are each 0 or 1.

    out_file : string, e.g., 'tdata_R.out'

        Path to space-delimited text file containing nrules rows and (ndata + 1)
        columms.  Each row indicates which of the ndata training data points
        obeys a particular rule: its first entry is a string description of a
        rule, e.g., `{c1=b,c2=o}`, and its remaining entries are each 0 or 1.

"""
import heapq
import os
import time

import numpy as np
import gmpy2
from gmpy2 import mpz
import tabular as tb

from branch_bound import given_prefix, initialize, incremental, print_rule_list
import figs
import rule
import utils

def bbound(din=os.path.join('..', 'data'), dout=os.path.join('..', 'cache'),
           dlog=os.path.join('..', 'logs'), dfigs=os.path.join('..', 'figs'),
           froot='tdata_R', warm_start=False, max_accuracy=0., best_prefix=(),
           min_objective=np.inf, c=0.00001, min_captured_correct=0.003,
           max_prefix_length=20, max_cache_size=3000000, delimiter='\t',
           method='curiosity', seed=0, sample=1., quiet=True,
           garbage_collect=True):
    """
    Serial branch-and-bound algorithm for constructing rule lists.

    Uses caching, symmetries, priority queue.

    **Parameters**

    **method** : string

        String in ['breadth_first', 'curiosity', 'lower_bound', 'objective', 'random'].

    """
    ## greedy algorithm is currently broken

    if (method == 'breadth_first'):
        heap_metric = lambda key: len(key)  # equivalent to breadth-first search
    elif (method == 'curiosity'):
        heap_metric = lambda key: cache[key].curiosity
    elif (method == 'lower_bound'):
        heap_metric = lambda key: cache[key].lower_bound
    elif (method == 'objective'):
        heap_metric = lambda key: cache[key].objective
    else:
        assert (method == 'random')
        heap_metric = lambda key: np.random.random()

    if not os.path.exists(dout):
        os.mkdir(dout)
    if not os.path.exists(dlog):
        os.mkdir(dlog)
    if not os.path.exists(dfigs):
        os.mkdir(dfigs)

    label_file = '%s.label' % froot
    out_file = '%s.out' % froot

    (nrules, ndata, ones, rules, rule_set, rule_names,
     max_accuracy, min_objective, best_prefix, cache) = \
                initialize(din, dout, label_file, out_file, warm_start,
                           max_accuracy, min_objective, best_prefix, seed, sample)

    print 'c:', c
    print 'min_objective:', min_objective

    metadata = ('%s-serial_priority-c=%2.5f-min_cap=%1.3f-min_objective=%1.3f-method=%s-max_cache_size=%d-sample=%2.2f' %
                (froot, c, min_captured_correct, min_objective, method, max_cache_size, sample))
    flog = os.path.join(dlog, '%s.txt' % metadata)
    print 'Writing log to', flog
    fh = open(flog, 'w')

    x = utils.rules_to_array(rules)
    commuting_pairs = utils.find_commuting_pairs(x)
    cdict = utils.commuting_dict(commuting_pairs, nrules)

    print froot
    print 'nrules:', nrules
    print 'ndata:', ndata

    # queue is a list of tuples encoding prefixes in the queue, where the ith entry
    # in such a tuple is the (row) index of a rule in the rules matrix
    queue = []

    # priority_queue is a min heap of prefixes ordered by values such as curiosity
    # or the lower bound on the objective
    priority_queue = []
    heapq.heappush(priority_queue, (heap_metric(()), ()))

    # pdict is a dictionary used for garbage collection that groups together
    # prefixes that are equivalent up to a permutation; its keys are tuples of
    # sorted prefix indices; each key maps to a list of prefix tuples in the cache
    # that are equivalent
    pdict = {}

    metrics = utils.Metrics(max_prefix_length + 1)
    metrics.cache_size[0] = 1
    metrics.priority_queue_length = 1
    metrics.best_prefix = best_prefix
    metrics.min_objective = min_objective
    metrics.accuracy = max_accuracy

    counter = 0
    tic = time.time()

    fh.write(metrics.names_to_string() + '\n')
    fh.write(metrics.to_string() + '\n')
    fh.flush()

    finished_max_prefix_length = 0
    max_prefix_len_check = 100

    while (priority_queue):
        (hm, prefix_start) = heapq.heappop(priority_queue)
        i = len(prefix_start) + 1
        if (i > max_prefix_len_check):
            continue

        try:
            # cached_prefix is the cached data about a previously evaluated prefix
            cached_prefix = cache[prefix_start]
        except:
            # prefix_start was in the priority_queue but has since been removed from
            # the cache
            continue

        if (cached_prefix.lower_bound > min_objective):
            # we don't need to evaluate any prefixes that start with prefix_start if
            # its upper_bound is less than max_accuracy
            metrics.dead_prefix_start[i] += 1
            if not quiet:
                print prefix_start, len(cache), 'lb(cached)>min', \
                      '%1.3f %1.3f %1.3f' % (cached_prefix.objective,
                      cached_prefix.lower_bound, min_objective)
            continue
        elif (cached_prefix.objective == cached_prefix.lower_bound):
            metrics.stunted_prefix[i] += 1
            continue

        # construct a queue of all prefixes starting with prefix_start and
        # appended with one additional rule
        assert len(queue) == 0
        rules_to_consider = rule_set.difference(set(prefix_start))
        if len(prefix_start):
            last_rule = prefix_start[-1]
            rtc = rules_to_consider.difference(set(cdict[last_rule]))
            metrics.commutes[i] += len(rules_to_consider) - len(rtc)
            rules_to_consider = rtc
        queue = [prefix_start + (t,) for t in list(rules_to_consider)]

        while(queue):
            # prefix is the first prefix tuple in the queue
            prefix = queue.pop(0)

            # compute cache entry for prefix via incremental computation, and add to
            # cache if relevant
            (max_accuracy, new_min_objective, best_prefix, cz, it, dp, ir) = \
                incremental(cache, prefix, rules, ones, ndata, cached_prefix,
                max_accuracy=max_accuracy, min_objective=min_objective, c=c,
                min_captured_correct=min_captured_correct, best_prefix=best_prefix,
                garbage_collect=garbage_collect, pdict=pdict, quiet=quiet)

            metrics.best_prefix = best_prefix
            metrics.min_objective = min_objective
            metrics.accuracy = max_accuracy
            metrics.captured_zero[i] += cz
            metrics.insufficient[i] += it
            metrics.dead_prefix[i] += dp
            metrics.inferior[i] += ir

            if ((cz == 0) and (it == 0) and (dp == 0) and (ir == 0)):
                metrics.cache_size[i] += 1
            if (prefix in cache):
                if (cache[prefix].lower_bound == cache[prefix].objective):
                    if (len(prefix) < max_prefix_len_check):
                        print ('objective = lower bound, max prefix length to check:', 
                               max_prefix_len_check, '->', len(prefix))
                        max_prefix_len_check = len(prefix)
                else:
                    heapq.heappush(priority_queue, (heap_metric(prefix), prefix))

            if (new_min_objective < min_objective):
                min_objective = new_min_objective
                metrics.priority_queue_length = len(priority_queue)
                metrics.seconds = time.time() - tic
                fh.write(metrics.to_string() + '\n')
                fh.flush()
                """
                # very basic pruning
                # prune any prefixes starting with rule r such that the lower bound
                # of (r,) exceeds the minimum observed objective
                for r in range(nrules):
                    if (r,) in cache:
                        if (cache[(r,)].lower_bound >= min_objective):
                            priority_queue = [(val, key) for (val, key) in
                                              priority_queue if (key[:1] != (r,))]
                print 'len(priority_queue)', len(priority_queue)
                """

        counter += 1
        if ((counter % 1000) == 0):
            metrics.priority_queue_length = len(priority_queue)
            metrics.seconds = time.time() - tic
            fh.write(metrics.to_string() + '\n')
            fh.flush()
            if not quiet:
                print metrics

        if False:#(method == 'breadth_first'):
            if (i > (finished_max_prefix_length + 1)):
               finished_max_prefix_length += 1
               assert metrics.check(finished_max_prefix_length, nrules)
               print ('checked cache size for prefixes of lengths %d and %d' %
                     (finished_max_prefix_length, finished_max_prefix_length - 1))

        if (len(cache) >= max_cache_size):
            break

        if (min_objective == 0.):
            break

    metrics.priority_queue_length = len(priority_queue)
    metrics.seconds = time.time() - tic
    fh.write(metrics.to_string())
    fh.close()

    print 'prefix length:', len(best_prefix)
    print metrics
    print metrics.print_summary()

    try:
        cc = cache[best_prefix]
        print_rule_list(cc.prefix, cc.prediction, cc.default_rule, rule_names)
        print cc
    except:
        print 'best prefix not in cache'

    figs.viz_log(metadata=metadata, din=dlog, dout=dfigs, delimiter=',', lw=3, fs=14)

    fname = os.path.join(dout, '%s.txt' % metadata)
    cache.to_file(fname=fname, delimiter=delimiter)
    x = tb.tabarray(SVfile=fname, delimiter=delimiter)
    x.sort(order=['length', 'first'])
    x.saveSV(fname, delimiter=delimiter)

    figs.make_figure(metadata=metadata, din=dout, dout=dfigs,
                     max_accuracy=max_accuracy, max_length=x[-1]['length'])

    return (metadata, metrics, cache, priority_queue)

def tdata_1():
    (metadata, metrics, cache, priority_queue) = \
    bbound(din=os.path.join('..', 'data'), dout=os.path.join('..', 'cache'),
           dlog=os.path.join('..', 'logs'), dfigs=os.path.join('..', 'figs'),
           froot='tdata_R', warm_start=False, max_accuracy=0., best_prefix=(),
           min_objective=np.inf, c=0., min_captured_correct=0.,
           max_prefix_length=20, max_cache_size=3000000, delimiter='\t',
           method='breadth_first', seed=0, sample=1., quiet=True,
           garbage_collect=True)
    return (metadata, metrics, cache, priority_queue)

def tdata_2():
    (metadata, metrics, cache, priority_queue) = \
    bbound(din=os.path.join('..', 'data'), dout=os.path.join('..', 'cache'),
           dlog=os.path.join('..', 'logs'), dfigs=os.path.join('..', 'figs'),
           froot='tdata_R', warm_start=False, max_accuracy=0., best_prefix=(),
           min_objective=np.inf, c=0., min_captured_correct=0.,
           max_prefix_length=90, max_cache_size=3000000, delimiter='\t',
           method='curiosity', seed=0, sample=1., quiet=True,
           garbage_collect=True)
    return (metadata, metrics, cache, priority_queue)

def tdata_3():
    (metadata, metrics, cache, priority_queue) = \
    bbound(din=os.path.join('..', 'data'), dout=os.path.join('..', 'cache'),
           dlog=os.path.join('..', 'logs'), dfigs=os.path.join('..', 'figs'),
           froot='tdata_R', warm_start=False, max_accuracy=0., best_prefix=(),
           min_objective=np.inf, c=0.00001, min_captured_correct=0.,
           max_prefix_length=20, max_cache_size=3000000, delimiter='\t',
           method='curiosity', seed=0, sample=1., quiet=True,
           garbage_collect=True)
    return (metadata, metrics, cache, priority_queue)

# accuracy = 0.83 # 0.835438
# min_objective = 0.06
"""
if False: #(froot == 'adult_R'):
    pfx = (43, 69, 122, 121)
    (max_accuracy, min_objective, best_prefix) = \
    given_prefix(pfx, cache, rules, ones, ndata, max_accuracy=max_accuracy,
                 min_objective=min_objective, c=c, best_prefix=best_prefix)
    print cache[pfx]
    for k in cache.keys():
        if (k != ()):
            cache.pop(k)
    print cache
"""
def example_adult():
    (metadata, metrics, cache, priority_queue) = \
    bbound(din=os.path.join('..', 'data'), dout=os.path.join('..', 'cache'),
           dlog=os.path.join('..', 'logs'), dfigs=os.path.join('..', 'figs'),
           froot='adult_R', warm_start=False, max_accuracy=0., best_prefix=(),
           min_objective=np.inf, c=0.00001, min_captured_correct=0.003,
           max_prefix_length=20, max_cache_size=3000000, delimiter='\t',
           method='curiosity', seed=0, sample=0.1, quiet=True,
           garbage_collect=True)
    return (metadata, metrics, cache, priority_queue)
