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
           min_objective=np.inf, c=0.01, min_captured_correct=0.01,
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
    elif (method == 'random'):
        heap_metric = lambda key: np.random.random()
    else:
        assert (method == 'depth_first')
        heap_metric = lambda key: 1. / (len(key) + 1.)

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
                           sample=sample, do_garbage_collection=garbage_collect,
                           max_prefix_length=max_prefix_length, c=c)

    if False: #(froot == 'adult_R'):
        pfx = (43, 69, 122, 121)
        (max_accuracy, min_objective, best_prefix) = \
        given_prefix(pfx, cache, rules, ones, ndata, c=c,
                     min_captured_correct=min_captured_correct)
        print cache[pfx]
        for k in cache.keys():
            if (k != ()):
                cache.pop(k)
        print cache

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

    counter = 0
    tic = time.time()

    fh.write(cache.metrics.names_to_string() + '\n')
    fh.write(cache.metrics.to_string() + '\n')
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
            #cached_prefix.reject_list = cache[prefix_start[:-1]].reject_list
            #print prefix_start, cache[prefix_start[:-1]].reject_list
            rl = set([])
            for ind in range(len(prefix_start)):
                try:
                    rl.update(cache[cache.pdict[prefix_start[:ind] + prefix_start[(ind+1):]][0]].reject_list)
                except:
                    pass
            rl = list(rl)
            rl.sort()
            cached_prefix.reject_list = rl

        # construct a queue of all prefixes starting with prefix_start and
        # appended with one additional rule
        rules_to_consider = rule_set.difference(set(prefix_start))
        if len(prefix_start):
            # prune rules that commute with the last rule in prefix_start and
            # have a smaller index
            r0 = len(rules_to_consider)
            rtc = rules_to_consider.difference(set(cdict[prefix_start[-1]]))
            cache.metrics.commutes[i] += r0 - len(rtc)
            # prune rules that are dominated by rules in prefix_start
            # definition: A dominates B if A captures all data that B captures
            r1 = len(rtc)
            rtc = rtc.difference(utils.all_relations(rdict, prefix_start))
            cache.metrics.dominates[i] += r1 - len(rtc)
            # prune rules in the reject_list (that will not capture sufficient
            # data, given prefix_start and min_captured_correct)
            r2 = len(rtc)
            rtc = rtc.difference(set(cached_prefix.reject_list))
            cache.metrics.rejects[i] += r2 - len(rtc)
            rules_to_consider = rtc
        queue = [prefix_start + (t,) for t in list(rules_to_consider)]
        lower_bound = None

        while(queue):
            # remove a prefix from the queue
            prefix = queue.pop(0)

            old_min_objective = min_objective
            # compute cache entry for prefix via incremental computation
            cache_entry = incremental(cache, prefix, rules, ones, ndata,
                                      cached_prefix, c=c, quiet=quiet,
                                      min_captured_correct=min_captured_correct)

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
            if (cache.metrics.min_objective < min_objective):
                min_objective = cache.metrics.min_objective
                best_prefix = cache.metrics.best_prefix
                max_accuracy = cache.metrics.accuracy

            # if min_objective is the minimum possible, given prefix's length
            if (min_objective == (c * len(prefix))):
                # insert prefix into the cache
                cache.insert(prefix, cache_entry)
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
                    # add prefix to cache and priority_queue if its children are
                    # at most as long as max_prefix_len_check and its children's
                    # bounds can be less than min_objective
                    if ((cache_entry.lower_bound + c) < min_objective):
                        cache.insert(prefix, cache_entry)
                        assert (cache.metrics.pdict_length == len(cache.pdict)), \
                               (cache.metrics.pdict_length, len(cache.pdict), prefix)
                        # prefix is not necessarily inserted into the cache due
                        # to symmetry-aware garbage collection
                        if (prefix in cache):
                            heapq.heappush(priority_queue, (heap_metric(prefix), prefix))

            # if the best min_objective so far is due to prefix, then update
            # some metrics, write a log entry, and garbage collect the cache
            if (cache.metrics.min_objective < old_min_objective):
                cache.metrics.priority_queue_length = len(priority_queue)
                cache.metrics.seconds = time.time() - tic
                size_before_gc = sum(cache.metrics.cache_size)
                cache.garbage_collect(min_objective)
                cache.metrics.garbage_collect += size_before_gc - sum(cache.metrics.cache_size)
                fh.write(cache.metrics.to_string() + '\n')
                fh.flush()
                print cache.metrics

        if clear and (prefix_start != best_prefix):
            cached_prefix.clear()

        if not certify:
            """
            # update lower bounds
            if (cached_prefix.lower_bound > lower_bound):
                size_before_lb = sum(cache.metrics.cache_size)
                cache.update_lower_bound(prefix_start, lower_bound, min_objective)
                print 'after lb:', size_before_lb - sum(cache.metrics.cache_size)
            """
            # prune up: remove dead ends from the cache
            if (cached_prefix.num_children == 0):
                cache.prune_up(prefix_start)

        if (() not in cache):
            done = True
            break

        # write a log entry for every 1000 outer loop iterations that reach here
        counter += 1
        if ((counter % 1000) == 0):
            cache.metrics.priority_queue_length = len(priority_queue)
            cache.metrics.seconds = time.time() - tic
            fh.write(cache.metrics.to_string() + '\n')
            fh.flush()
            print cache.metrics

        if False: #(method == 'breadth_first'):
            if (i > (finished_max_prefix_length + 1)):
               finished_max_prefix_length += 1
               assert cache.metrics.check(finished_max_prefix_length, nrules)
               print ('checked cache size for prefixes of lengths %d and %d' %
                     (finished_max_prefix_length, finished_max_prefix_length - 1))

        if (len(cache) >= max_cache_size):
            break

    # write final log entry
    cache.metrics.priority_queue_length = len(priority_queue)
    cache.metrics.seconds = time.time() - tic
    fh.write(cache.metrics.to_string())
    fh.close()

    print 'prefix length:', len(cache.metrics.best_prefix)
    print cache.metrics
    print cache.metrics.print_summary()

    cc = cache.best
    descr = ''
    if (cc is not None):
        print cc
        descr = print_rule_list(cc.prefix, cc.prediction, cc.default_rule, rule_names)

    figs.viz_log(metadata=metadata, din=dlog, dout=dfigs, delimiter=',', lw=3, fs=14)
    #"""
    try:
        if (len(priority_queue) > 0):
            fname = os.path.join(dout, '%s.txt' % metadata)
            cache.to_file(fname=fname, delimiter=delimiter)
            x = tb.tabarray(SVfile=fname, delimiter=delimiter)
            x.sort(order=['length', 'first'])
            x.saveSV(fname, delimiter=delimiter)
            figs.make_figure(metadata=metadata, din=dout, dout=dfigs)
    except:
        pass
    #"""
    return (metadata, cache.metrics, cache, priority_queue, cc, descr)

def tdata_1():
    (metadata, metrics, cache, priority_queue, best, rule_list) = \
    bbound(din=os.path.join('..', 'data'), dout=os.path.join('..', 'cache'),
           dlog=os.path.join('..', 'logs'), dfigs=os.path.join('..', 'figs'),
           froot='tdata_R', warm_start=False, max_accuracy=0., best_prefix=(),
           min_objective=1., c=0.01, min_captured_correct=0.01,
           max_prefix_length=20, max_cache_size=3000000, delimiter='\t',
           method='breadth_first', seed=0, sample=1., quiet=True, clear=False,
           garbage_collect=True)
    return (metadata, metrics, cache, priority_queue, best, rule_list)

def tdata_2():
    (metadata, metrics, cache, priority_queue, best, rule_list) = \
    bbound(din=os.path.join('..', 'data'), dout=os.path.join('..', 'cache'),
           dlog=os.path.join('..', 'logs'), dfigs=os.path.join('..', 'figs'),
           froot='tdata_R', warm_start=False, max_accuracy=0., best_prefix=(),
           min_objective=1., c=0., min_captured_correct=0.,
           max_prefix_length=90, max_cache_size=3000000, delimiter='\t',
           method='curiosity', seed=0, sample=1., quiet=True, clear=False,
           garbage_collect=True)
    return (metadata, metrics, cache, priority_queue, best, rule_list)

def tdata_3():
    (metadata, metrics, cache, priority_queue, best, rule_list) = \
    bbound(din=os.path.join('..', 'data'), dout=os.path.join('..', 'cache'),
           dlog=os.path.join('..', 'logs'), dfigs=os.path.join('..', 'figs'),
           froot='tdata_R', warm_start=False, max_accuracy=0., best_prefix=(),
           min_objective=1., c=0.001, min_captured_correct=0.001,
           max_prefix_length=10, max_cache_size=30000, delimiter='\t',
           method='curiosity', seed=0, sample=1., quiet=True, clear=True,
           garbage_collect=True)
    return (metadata, metrics, cache, priority_queue, best, rule_list)

def example_adult(method='breadth_first', max_cache_size=2600000, c=0.01):
    (metadata, metrics, cache, priority_queue, best, rule_list) = \
    bbound(din=os.path.join('..', 'data'), dout=os.path.join('..', 'cache'),
           dlog=os.path.join('..', 'logs'), dfigs=os.path.join('..', 'figs'),
           froot='adult_R', warm_start=False, max_accuracy=0., best_prefix=(),
           min_objective=1., c=c, min_captured_correct=c,
           max_prefix_length=10, max_cache_size=max_cache_size, delimiter='\t',
           method=method, seed=0, sample=0.1, quiet=True, clear=True,
           garbage_collect=True)
    return (metadata, metrics, cache, priority_queue, best, rule_list)

def small(froot, c=0.01, min_captured_correct=0.01, method='curiosity',
          max_cache_size=3000000):
    (metadata, metrics, cache, priority_queue, best, rule_list) = \
    bbound(din=os.path.join('..', 'data'), dout=os.path.join('..', 'cache'),
           dlog=os.path.join('..', 'logs'), dfigs=os.path.join('..', 'figs'),
           froot=froot, warm_start=False, max_accuracy=0., best_prefix=(),
           min_objective=1., c=c, min_captured_correct=min_captured_correct,
           max_prefix_length=20, max_cache_size=max_cache_size, delimiter='\t',
           method=method, seed=0, sample=1., quiet=True, clear=True,
           garbage_collect=True)
    return (metadata, metrics, cache, priority_queue, best, rule_list)

def bcancer():
    return small('bcancer_R')

def cars():
    return small('cars_R')

def haberman():
    return small('haberman_R')

def monks1():
    return small('monks1_R')

def monks2():
    return small('monks2_R')

def monks3():
    return small('monks3_R')

def votes():
    return small('votes_R')

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
    ones = utils.mpz_to_array(ones)
    rules = utils.rules_to_array(rules)
    commuting_pairs = utils.find_commuting_pairs(rules)
    cdict = utils.commuting_dict(commuting_pairs, nrules)
    return (nrules, ndata, ones, rules, rule_set, rule_names)

def tdata():
    return load_data(froot='tdata_R')

def adult():
    return load_data(froot='adult_R')

def small_datasets(dout='../results/', fout='small.md'):
    import pylab
    if not os.path.exists(dout):
        os.mkdir(dout)
    fh = open(os.path.join(dout, fout), 'w')
    descr = []
    fh.write('##small datasets (with varying amounts of regularization)\n\n')
    fh.write('| dataset | c | d | time (s) | objective | lower bound | accuracy | upper bound | length |\n')
    fh.write('| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n')
    template = '| %s | %1.3f | %1.3f | %2.3f | %1.3f | %1.3f | %1.3f | %1.3f | %d |\n'
    flist = ['bcancer', 'cars', 'haberman', 'monks1', 'monks2', 'monks3', 'votes']
    params = [(0.01, 0.01), (0.003, 0.003), (0.001, 0.001), (0., 0.)]
    for f in flist:
        froot = '%s_R' % f
        for (c, d) in params:
            print froot, c, d
            pylab.close('all')
            (metadata, metrics, cache, priority_queue, best, rule_list) = \
                                                              small(froot, c, d)
            rec = (f, c, d, metrics.seconds, best.objective, best.lower_bound,
                   best.accuracy, best.upper_bound, len(best.prefix))
            fh.write(template % rec)
            descr += [(f, c, d, rule_list, metadata)]
    for (f, c, d, rule_list, md) in descr:
        fh.write('\n###%s, c=%1.3f, d=%1.3f\n\n' % (f, c, d))
        rl = '\n'.join(['\t' + line for line in rule_list.strip().split('\n')])
        fh.write('%s\n' % rl)
        if os.path.exists('../figs/%s-log.png' % md):
            fh.write('\n![%s-log](../figs/%s-log.png)\n' % (md, md))
        if os.path.exists('../figs/%s-cache.png' % md):
            fh.write('![%s-cache](../figs/%s-cache.png)\n' % (md, md))
    fh.close()
    return

def adult_metrics(dout='../results/', fout='adult-metrics.md'):
    import pylab
    if not os.path.exists(dout):
        os.mkdir(dout)
    fh = open(os.path.join(dout, fout), 'w')
    descr = []
    fh.write('##adult dataset with different priority metrics (c = d = 0.01)\n\n')
    fh.write('stop after 2,600,000 cache entries\n\n')
    fh.write('| priority metric | time (s) | objective | lower bound | accuracy | upper bound | best prefix |\n')
    fh.write('| --- | --- | --- | --- | --- | --- | --- |\n')
    template = '| %s | %2.3f | %1.3f | %1.3f | %1.3f | %1.3f | %s |\n'
    params = ['breadth_first', 'curiosity', 'lower_bound', 'objective']
    f = 'adult'
    froot = '%s_R' % f
    for method in params:
        print froot, method
        pylab.close('all')
        (metadata, metrics, cache, priority_queue, best, rule_list) = \
                                    example_adult(method=method, max_cache_size=2600000)
        rec = (method, metrics.seconds, best.objective, best.lower_bound,
               best.accuracy, best.upper_bound, best.prefix.__repr__())
        fh.write(template % rec)
        descr += [(method, rule_list, metadata)]
    for (method, rule_list, md) in descr:
        fh.write('\n###%s\n\n' % (method))
        rl = '\n'.join(['\t' + line for line in rule_list.strip().split('\n')])
        fh.write('%s\n' % rl)
        if os.path.exists('../figs/%s-log.png' % md):
            fh.write('\n![%s-log](../figs/%s-log.png)\n' % (md, md))
        if os.path.exists('../figs/%s-leaves.png' % md):
            fh.write('![%s-cache](../figs/%s-leaves.png)\n' % (md, md))
        if os.path.exists('../figs/%s-cache.png' % md):
            fh.write('![%s-cache](../figs/%s-cache.png)\n' % (md, md))
    fh.close()
    return

def adult_regularize(dout='../results/', fout='adult-regularize.md'):
    import pylab
    if not os.path.exists(dout):
        os.mkdir(dout)
    fh = open(os.path.join(dout, fout), 'w')
    descr = []
    fh.write('##adult dataset with varying regularization (breadth-first, c = d, max_cache_size=3000000)\n\n')
    fh.write('stop after 3,000,000 cache entries\n\n')
    fh.write('| c | time (s) | objective | lower bound | accuracy | upper bound | best prefix |\n')
    fh.write('| --- | --- | --- | --- | --- | --- | --- |\n')
    template = '| %1.2f | %2.3f | %1.3f | %1.3f | %1.3f | %1.3f | %s |\n'
    params = np.arange(0.1, 0., -0.01)
    f = 'adult'
    froot = '%s_R' % f
    for c in params:
        print froot, c
        pylab.close('all')
        (metadata, metrics, cache, priority_queue, best, rule_list) = \
                        example_adult(method='breadth_first', max_cache_size=3000000, c=c)
        rec = (c, metrics.seconds, best.objective, best.lower_bound,
               best.accuracy, best.upper_bound, best.prefix.__repr__())
        fh.write(template % rec)
        descr += [(c, rule_list, metadata)]
    for (c, rule_list, md) in descr:
        fh.write('\n###c = %1.2f\n\n' % (c))
        rl = '\n'.join(['\t' + line for line in rule_list.strip().split('\n')])
        fh.write('%s\n' % rl)
        if os.path.exists('../figs/%s-log.png' % md):
            fh.write('\n![%s-log](../figs/%s-log.png)\n' % (md, md))
        if os.path.exists('../figs/%s-leaves.png' % md):
            fh.write('![%s-cache](../figs/%s-leaves.png)\n' % (md, md))
        if os.path.exists('../figs/%s-cache.png' % md):
            fh.write('![%s-cache](../figs/%s-cache.png)\n' % (md, md))
    fh.close()
    return

def tdata(dout='../results/', fout='tdata.md'):
    import pylab
    if not os.path.exists(dout):
        os.mkdir(dout)
    fh = open(os.path.join(dout, fout), 'w')
    descr = []
    fh.write('##tic-tac-toe dataset (curiosity, c = d = 0.01)\n\n')
    f = 'tdata'
    froot = '%s_R' % f
    print froot
    pylab.close('all')
    (metadata, metrics, cache, priority_queue, best, rule_list) = tdata_3()
    descr += [(rule_list, metadata)]
    for (rule_list, md) in descr:
        rl = '\n'.join(['\t' + line for line in rule_list.strip().split('\n')])
        fh.write('%s\n' % rl)
        if os.path.exists('../figs/%s-log.png' % md):
            fh.write('\n![%s-log](../figs/%s-log.png)\n' % (md, md))
        if os.path.exists('../figs/%s-leaves.png' % md):
            fh.write('![%s-cache](../figs/%s-leaves.png)\n' % (md, md))
        if os.path.exists('../figs/%s-cache.png' % md):
            fh.write('![%s-cache](../figs/%s-cache.png)\n' % (md, md))
    fh.close()
    return

def small_expanded(dout='../results/', foutroot='small_expanded', method='breadth_first',
                   max_cache_size=1000000):
    import pylab
    if not os.path.exists(dout):
        os.mkdir(dout)
    fout = '%s-method=%s-max_cache_size=%d.md' % (foutroot, method, max_cache_size)
    fh = open(os.path.join(dout, fout), 'w')
    descr = []
    fh.write('##small datasets (%s, max_cache_size=%d)\n\n' % (method, max_cache_size))
    fh.write('| dataset | c | d | time (s) | objective | lower bound | accuracy | upper bound | length |\n')
    fh.write('| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n')
    template = '| %s | %1.3f | %1.3f | %2.3f | %1.3f | %1.3f | %1.3f | %1.3f | %d |\n'
    flist = ['bcancer', 'cars', 'haberman', 'monks1', 'monks2', 'monks3', 'votes']
    params = [(0.01, 0.01)]
    for f in flist:
        froot = '%s' % f
        for (c, d) in params:
            print froot, c, d
            pylab.close('all')
            (metadata, metrics, cache, priority_queue, best, rule_list) = \
                small(froot, c, d, method=method, max_cache_size=max_cache_size)
            rec = (f, c, d, metrics.seconds, best.objective, best.lower_bound,
                   best.accuracy, best.upper_bound, len(best.prefix))
            fh.write(template % rec)
            descr += [(f, c, d, rule_list, metadata)]
    for (f, c, d, rule_list, md) in descr:
        fh.write('\n###%s, c=%1.3f, d=%1.3f\n\n' % (f, c, d))
        rl = '\n'.join(['\t' + line for line in rule_list.strip().split('\n')])
        fh.write('%s\n' % rl)
        if os.path.exists('../figs/%s-log.png' % md):
            fh.write('\n![%s-log](../figs/%s-log.png)\n' % (md, md))
        if os.path.exists('../figs/%s-cache.png' % md):
            fh.write('![%s-cache](../figs/%s-cache.png)\n' % (md, md))
    fh.close()
    return