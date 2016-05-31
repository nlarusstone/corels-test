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
           method='curiosity', seed=0, sample=1., quiet=True, clear=False,
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

    if (method == 'breadth_first'):
        certify = True
    else:
        certify = False

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
                           max_accuracy, min_objective, best_prefix, seed=seed,
                           sample=sample, do_garbage_collection=garbage_collect)

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
    rdict = utils.relations_dict(x)

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
    if (c == 0.):
        max_prefix_len_check = 100
    else:
        max_prefix_len_check = int(np.floor(min_objective / c))

    done = False
    while (priority_queue and (not done)):
        (hm, prefix_start) = heapq.heappop(priority_queue)
        i = len(prefix_start) + 1
        if (i > max_prefix_len_check):
            continue
        try:
            # cached_prefix corresponds to a previously evaluated prefix
            cached_prefix = cache[prefix_start]
        except:
            # prefix_start was in the priority_queue but has since been removed
            # from the cache
            continue
        if (i > 1):
            cached_prefix.reject_list = cache[prefix_start[:-1]].reject_list

        # construct a queue of all prefixes starting with prefix_start and
        # appended with one additional rule
        rules_to_consider = rule_set.difference(set(prefix_start))
        if len(prefix_start):
            # prune rules that commute with the last rule in prefix_start and
            # have a smaller index
            rtc = rules_to_consider.difference(set(cdict[prefix_start[-1]]))
            # prune rules that are dominated by rules in prefix_start
            # definition: A dominates B if A captures all data that B captures
            rtc = rtc.difference(utils.all_relations(rdict, prefix_start))
            # prune rules in the reject_list (that will not capture sufficient
            # data, given prefix_start and min_captured_correct)
            rtc = rtc.difference(set(cached_prefix.reject_list))
            metrics.commutes[i] += len(rules_to_consider) - len(rtc)
            rules_to_consider = rtc
        queue = [prefix_start + (t,) for t in list(rules_to_consider)]
        lower_bound = None

        while(queue):
            # remove a prefix from the queue
            prefix = queue.pop(0)

            old_min_objective = min_objective
            # compute cache entry for prefix via incremental computation
            (metrics, cache_entry) = \
                incremental(cache, prefix, rules, ones, ndata, cached_prefix,
                            c=c, min_captured_correct=min_captured_correct,
                            quiet=quiet, metrics=metrics)

            if cache_entry is None:
                # incremental(.) did not return a cache entry for prefix
                continue
            else:
                if (lower_bound is None):
                    lower_bound = cache_entry.lower_bound
                else:
                    lower_bound = max(lower_bound, cache_entry.lower_bound)

            # if the minimum observed objective improved, update min_objective,
            # best_prefix, and "max_accuracy"
            if (metrics.min_objective < min_objective):
                min_objective = metrics.min_objective
                best_prefix = metrics.best_prefix
                max_accuracy = metrics.accuracy

            # if min_objective is the minimum possible, given prefix's length
            if (min_objective == (c * len(prefix))):
                # insert prefix into the cache
                metrics = cache.insert(prefix, cache_entry, metrics)
                if certify or (method == 'breadth_first') or (min_objective == 0):
                    # we have identified a global optimum
                    done = True
                    break
                if (len(prefix) <= max_prefix_len_check):
                    # we don't need to check longer prefixes, so now we should
                    # switch to certification mode, i.e., breadth-first policy
                    print 'objective = best possible, max prefix length to check:', \
                           max_prefix_len_check, '->', len(prefix) - 1
                    max_prefix_len_check = len(prefix) - 1
                    #certify = True
                    #heap_metric = lambda key: len(key)
                    #priority_queue = [(heap_metric(key), key) for (val, key) in priority_queue]
                    #heapq.heapify(priority_queue)
                    #print 're-prioritized for breadth-first search policy'
            else:
                if (len(prefix) < max_prefix_len_check):
                    # add prefix to cache priority_queue if its children are at
                    # most as long as max_prefix_len_check
                    if ((cache_entry.lower_bound + c) < min_objective):
                        metrics = cache.insert(prefix, cache_entry, metrics)
                        assert (metrics.pdict_length == len(cache.pdict)), (metrics.pdict_length, len(cache.pdict), prefix)
                        if (prefix in cache):
                            heapq.heappush(priority_queue, (heap_metric(prefix), prefix))
                else:
                    # if prefix is longer, only add to cache if it is also
                    # best_prefix, but do not add to priority_queue
                    if (prefix == best_prefix):
                        metrics = cache.insert(prefix, cache_entry, metrics)

            # if the best min_objective so far is due to prefix, then update
            # some metrics, write a log entry, and garbage collect the cache
            if (metrics.min_objective < old_min_objective):
                metrics.priority_queue_length = len(priority_queue)
                metrics.seconds = time.time() - tic
                fh.write(metrics.to_string() + '\n')
                fh.flush()
                size_before_gc = sum(metrics.cache_size)
                metrics = cache.garbage_collect(min_objective, metrics=metrics)
                metrics.garbage_collect += size_before_gc - sum(metrics.cache_size)
                print metrics

        if clear and (prefix_start != best_prefix):
            cached_prefix.clear()

        if not certify:
            """
            # update lower bounds
            if (cached_prefix.lower_bound > lower_bound):
                size_before_lb = sum(metrics.cache_size)
                metrics = cache.update_lower_bound(prefix_start, lower_bound, min_objective, metrics)
                print 'after lb:', size_before_lb - sum(metrics.cache_size)
            """
            # prune up: remove dead ends from the cache
            if (cached_prefix.num_children == 0):
                size_before_pu = sum(metrics.cache_size)
                metrics = cache.prune_up(prefix_start, metrics)
                metrics.prune_up += size_before_pu - sum(metrics.cache_size)

        if (() not in cache):
            done = True
            break

        # write a log entry for every 1000 outer loop iterations that reach here
        counter += 1
        if ((counter % 10000) == 0):
            metrics.priority_queue_length = len(priority_queue)
            metrics.seconds = time.time() - tic
            fh.write(metrics.to_string() + '\n')
            fh.flush()
            print metrics

        if False: #(method == 'breadth_first'):
            if (i > (finished_max_prefix_length + 1)):
               finished_max_prefix_length += 1
               assert metrics.check(finished_max_prefix_length, nrules)
               print ('checked cache size for prefixes of lengths %d and %d' %
                     (finished_max_prefix_length, finished_max_prefix_length - 1))

        if (len(cache) >= max_cache_size):
            break

    # write final log entry
    metrics.priority_queue_length = len(priority_queue)
    metrics.seconds = time.time() - tic
    fh.write(metrics.to_string())
    fh.close()

    print 'prefix length:', len(metrics.best_prefix)
    print metrics
    print metrics.print_summary()

    """
    try:
        cc = cache[metrics.best_prefix]
        print_rule_list(cc.prefix, cc.prediction, cc.default_rule, rule_names)
        print cc
    except:
        print 'best prefix not in cache'

    """
    figs.viz_log(metadata=metadata, din=dlog, dout=dfigs, delimiter=',', lw=3, fs=14)
    """
    try:
        fname = os.path.join(dout, '%s.txt' % metadata)
        cache.to_file(fname=fname, delimiter=delimiter)
        x = tb.tabarray(SVfile=fname, delimiter=delimiter)
        x.sort(order=['length', 'first'])
        x.saveSV(fname, delimiter=delimiter)
        figs.make_figure(metadata=metadata, din=dout, dout=dfigs,
                         max_accuracy=metrics.accuracy, max_length=x[-1]['length'])
    except:
        pass
    """
    return (metadata, metrics, cache, priority_queue)

def tdata_1():
    (metadata, metrics, cache, priority_queue) = \
    bbound(din=os.path.join('..', 'data'), dout=os.path.join('..', 'cache'),
           dlog=os.path.join('..', 'logs'), dfigs=os.path.join('..', 'figs'),
           froot='tdata_R', warm_start=False, max_accuracy=0., best_prefix=(),
           min_objective=1., c=0., min_captured_correct=0.,
           max_prefix_length=20, max_cache_size=3000000, delimiter='\t',
           method='breadth_first', seed=0, sample=1., quiet=True, clear=False,
           garbage_collect=True)
    return (metadata, metrics, cache, priority_queue)

def tdata_2():
    (metadata, metrics, cache, priority_queue) = \
    bbound(din=os.path.join('..', 'data'), dout=os.path.join('..', 'cache'),
           dlog=os.path.join('..', 'logs'), dfigs=os.path.join('..', 'figs'),
           froot='tdata_R', warm_start=False, max_accuracy=0., best_prefix=(),
           min_objective=1., c=0., min_captured_correct=0.,
           max_prefix_length=90, max_cache_size=3000000, delimiter='\t',
           method='curiosity', seed=0, sample=1., quiet=True, clear=False,
           garbage_collect=True)
    return (metadata, metrics, cache, priority_queue)

def tdata_3():
    (metadata, metrics, cache, priority_queue) = \
    bbound(din=os.path.join('..', 'data'), dout=os.path.join('..', 'cache'),
           dlog=os.path.join('..', 'logs'), dfigs=os.path.join('..', 'figs'),
           froot='tdata_R', warm_start=False, max_accuracy=0., best_prefix=(),
           min_objective=1., c=0.001, min_captured_correct=0.,
           max_prefix_length=20, max_cache_size=3000000, delimiter='\t',
           method='curiosity', seed=0, sample=1., quiet=True, clear=False,
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
           method='curiosity', seed=0, sample=0.1, quiet=True, clear=True,
           garbage_collect=True)
    return (metadata, metrics, cache, priority_queue)

def load_data(froot):
    label_file = '%s.label' % froot
    out_file = '%s.out' % froot
    (nrules, ndata, ones, rules, rule_set, rule_names,
     max_accuracy, min_objective, best_prefix, cache) = \
            initialize(din=os.path.join('..', 'data'),
                       dout=os.path.join('..', 'cache'),
                       label_file=label_file, out_file=out_file,
                       warm_start=False, max_accuracy=0., min_objective=1.,
                       best_prefix=(), seed=0, sample=1.)
    rules = utils.rules_to_array(rules)
    commuting_pairs = utils.find_commuting_pairs(rules)
    cdict = utils.commuting_dict(commuting_pairs, nrules)
    return (nrules, ndata, ones, rules, rule_set, rule_names)

def tdata():
    return load_data(froot='tdata_R')

def adult():
    return load_data(froot='adult_R')
