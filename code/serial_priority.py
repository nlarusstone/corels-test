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

import gmpy2
from gmpy2 import mpz
import numpy as np
import pylab
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
           garbage_collect=True, do_pruning=False):
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
    print 'c:', c
    print 'min_objective:', min_objective
    metadata = ('%s-serial_priority-c=%2.5f-min_cap=%1.3f-min_objective=%1.3f-method=%s-max_cache_size=%d-sample=%2.2f' %
                (froot, c, min_captured_correct, min_objective, method, max_cache_size, sample))
    flog = os.path.join(dlog, '%s.txt' % metadata)
    print 'Writing log to', flog
    fh = open(flog, 'w')

    delete_set = set()
    for i in range(nrules - 1):
        for j in range(i + 1, nrules):
            if (rules[i] == rules[j]):
                ri = len(rule_names[i].split(','))
                rj = len(rule_names[j].split(','))
                if (ri < rj):
                    delete_set.add(j)
                elif (rj < ri):
                    delete_set.add(i)
                elif (rule_names[i] < rule_names[j]):
                    delete_set.add(j)
                else:
                    delete_set.add(i)

    print 'deleting', len(delete_set), 'redundant rules'
    rules = [rules[i] for i in range(nrules) if i not in delete_set]
    rule_names = [rule_names[i] for i in range(nrules) if i not in delete_set]
    nrules = len(rules)
    rule_set = set(range(nrules))

    x = utils.rules_to_array(rules)
    commuting_pairs = utils.find_commuting_pairs(x)
    cdict = utils.commuting_dict(commuting_pairs, nrules)
    rdict = utils.relations_dict(x)

    y = utils.mpz_to_array(ones)
    captured = [y[rule.nonzero()[0]] for rule in x]
    perfect_rules = [i for i in range(nrules) if (captured[i].sum() in [0, len(captured[i])])]
    for i in range(nrules):
        if i not in perfect_rules:
            ri = list(set(list(rdict[i]) + perfect_rules))
            ri.sort()
            rdict[i] = tuple(ri)
        else:
            ci = [j for j in perfect_rules if j > i]
            ci = list(set(list(cdict[i]) + ci))
            ci.sort()
            cdict[i] = tuple(ci)

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
    cache.metrics.priority = heap_metric(())

    fh.write(cache.metrics.names_to_string() + '\n')
    fh.write(cache.metrics.to_string() + '\n')
    fh.flush()

    finished_max_prefix_length = 0
    if (c == 0.):
        cache.max_prefix_len_check = 100
    else:
        cache.max_prefix_len_check = int(np.floor(min_objective / c))

    done = False
    while (priority_queue and (not done)):
        (hm, prefix_start) = heapq.heappop(priority_queue)
        i = len(prefix_start) + 1
        if (i > cache.max_prefix_len_check):
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
                    rl.update(cache[cache.pdict[prefix_start[:ind] + prefix_start[(ind+1):]][0]].reject_set)
                except:
                    pass
            cached_prefix.reject_set = rl

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
            # prune rules in the reject_set (that will not capture sufficient
            # data, given prefix_start and min_captured_correct)
            r2 = len(rtc)
            rtc = rtc.difference(set(cached_prefix.reject_set))
            cache.metrics.rejects[i] += r2 - len(rtc)
            rules_to_consider = rtc
        queue = [prefix_start + (t,) for t in list(rules_to_consider)]
        lower_bound = None
        captured_dict = {}

        while(queue):
            if prefix_start not in cache:
                break

            # remove a prefix from the queue
            prefix = queue.pop(0)

            # compute cache entry for prefix via incremental computation
            cache_entry = incremental(cache, prefix, rules, ones, ndata,
                            cached_prefix, c=c, quiet=quiet,
                            captured_dict=captured_dict, rule_names=rule_names,
                            min_captured_correct=min_captured_correct)

            if cache_entry is None:
                # incremental(.) did not return a cache entry for prefix
                continue

            old_min_objective = min_objective
            min_objective = cache.metrics.min_objective
            best_prefix = cache.metrics.best_prefix

            """
            if (lower_bound is None):
                lower_bound = cache_entry.lower_bound
            else:
                lower_bound = max(lower_bound, cache_entry.lower_bound)
            """

            # insert prefix into the cache
            cache.insert(prefix, cache_entry)
            cache.metrics.inserts[len(prefix)] += 1
            assert (cache.metrics.pdict_length == len(cache.pdict)), \
                       (cache.metrics.pdict_length, len(cache.pdict), prefix)

            # if min_objective is the minimum possible, given prefix's length
            if (min_objective == (c * len(prefix))):
                if certify or (method == 'breadth_first') or (min_objective == 0.):
                    # we have identified a global optimum
                    done = True
                    break
                if (len(prefix) <= cache.max_prefix_len_check):
                    # we don't need to check longer prefixes, so now we should
                    # update max_prefix_len_check
                    print 'objective = best possible, max prefix length to check:', \
                           cache.max_prefix_len_check, '->', len(prefix) - 1
                    cache.max_prefix_len_check = len(prefix) - 1
                    # switch to certification mode, i.e., breadth-first policy
                    #certify = True
                    #heap_metric = lambda key: len(key)
                    #priority_queue = [(heap_metric(key), key) for (val, key) in priority_queue]
                    #heapq.heapify(priority_queue)
                    #print 're-prioritized for breadth-first search policy'
            else:
                # add prefix to priority_queue
                heapq.heappush(priority_queue, (heap_metric(prefix), prefix))

            # if the best min_objective so far is due to prefix, then update
            # some metrics, write a log entry, and garbage collect the cache
            if (min_objective < old_min_objective):
                cache.metrics.priority_queue_length = len(priority_queue)
                cache.metrics.seconds = time.time() - tic
                size_before_gc = cache.metrics.cache_size.copy()
                cache.garbage_collect(min_objective)
                cache.metrics.garbage_collect += (size_before_gc - cache.metrics.cache_size)
                cache.metrics.priority = hm
                fh.write(cache.metrics.to_string() + '\n')
                fh.flush()
                print cache.metrics

        if clear and (prefix_start != best_prefix):
            cached_prefix.clear()

        if not certify:
            # update lower bounds (seems costly, not sure)
            """
            if ((prefix_start in cache) and (lower_bound is not None) and
               (cached_prefix.lower_bound < lower_bound)):
                # print cached_prefix.lower_bound, lower_bound
                size_before_lb = sum(cache.metrics.cache_size)
                cache.update_lower_bound(prefix_start, lower_bound, min_objective)
                lb_diff = size_before_lb - sum(cache.metrics.cache_size)
                print 'lb > 0:',  lb_diff
            """
            # prune up: remove dead ends from the cache
            if (do_pruning and (cached_prefix.num_children == 0)):
                cache.prune_up(prefix_start)

        if (() not in cache):
            done = True
            break

        # write a log entry for every 1000 outer loop iterations that reach here
        counter += 1
        if ((counter % 1000) == 0):
            cache.metrics.priority_queue_length = len(priority_queue)
            cache.metrics.seconds = time.time() - tic
            cache.metrics.priority = hm
            fh.write(cache.metrics.to_string() + '\n')
            fh.flush()
            print cache.metrics

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
    pylab.draw()
    #"""
    try:
        if (len(priority_queue) > 0):
            fname = os.path.join(dout, '%s.txt' % metadata)
            cache.to_file(fname=fname, delimiter=delimiter)
            x = tb.tabarray(SVfile=fname, delimiter=delimiter)
            x.sort(order=['length', 'first'])
            x.saveSV(fname, delimiter=delimiter)
            figs.make_figure(metadata=metadata, din=dout, dout=dfigs)
            pylab.draw()
    except:
        pass
    #"""
    return (metadata, cache.metrics, cache, priority_queue, cc, descr)

