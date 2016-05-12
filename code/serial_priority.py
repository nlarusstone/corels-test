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

din = os.path.join('..', 'data')
dout = os.path.join('..', 'cache')
dlog = os.path.join('..', 'logs')
froot = 'tdata_R'
warm_start = False ## greedy algorithm is currently broken
max_accuracy = 0.999
best_prefix = None
min_objective = 1.
c = 0.
max_prefix_length = 8
delimiter = '\t'
quiet = True
garbage_collect = True
seed = None
sample = None
method = 'lower_bound' # 'curiosity' # 'objective' # 'breadth-first' #
max_cache_size = 5000000

#"""
froot = 'adult_R'
max_accuracy = None #0.83 # 0.835438
min_objective = None # 673. #512.
c = 10.
max_prefix_length = 10
seed = 0
sample = 0.1
#"""

if (method == 'breadth-first'):
    heap_metric = lambda key: len(key)  # equivalent to breadth-first search
elif (method == 'curiosity'):
    heap_metric = lambda key: cache[key].curiosity
elif (method == 'lower_bound'):
    heap_metric = lambda key: cache[key].lower_bound
else:
    assert (method == 'objective')
    heap_metric = lambda key: cache[key].objective

if not os.path.exists(dout):
    os.path.mkdir(dout)
if not os.path.exists(dlog):
    os.path.mkdir(dlog)

label_file = '%s.label' % froot
out_file = '%s.out' % froot

(nrules, ndata, ones, rules, rule_set, rule_names,
 max_accuracy, min_objective, best_prefix, cache) = \
            initialize(din, dout, label_file, out_file, warm_start,
                       max_accuracy, min_objective, best_prefix, seed, sample)

print 'c:', c
print 'min_objective:', min_objective

if (froot == 'adult_R'):
    pfx = (43, 69, 122, 121)
    (max_accuracy, min_objective, best_prefix) = \
    given_prefix(pfx, cache, rules, ones, ndata, max_accuracy=max_accuracy,
                 min_objective=min_objective, c=c, best_prefix=best_prefix)
    print cache[pfx]
    for k in cache.keys():
        if (k != ()):
            cache.pop(k)
    print cache

metadata = ('%s-serial_priority-max_accuracy=%1.3f-max_length=%d-c=%d-method=%s-max_cache_size=%d' %
            (froot, max_accuracy, max_prefix_length, c, method, max_cache_size))
flog = os.path.join(dlog, '%s.txt' % metadata)
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

m = max_prefix_length + 1

cache_size = np.zeros(m, int)
cache_size[0] = 1

dead_prefix_start = np.zeros(m, int)
captured_zero = np.zeros(m, int)
stunted_prefix = np.zeros(m, int)
commutes = np.zeros(m, int)
dead_prefix = np.zeros(m, int)
inferior = np.zeros(m, int)

seconds = np.zeros(m)

# lazily add prefixes to the queue
# for i in range(1, max_prefix_length + 1):
#    print 'prefix length:', i
#    tic = time.time()

# pdict is a dictionary used for garbage collection that groups together prefixes that
# are equivalent up to a permutation; its keys are tuples of sorted prefix indices;
# each key maps to a list of prefix tuples in the cache that are equivalent
pdict = {}

counter = 0

#for prefix_start in prefix_list:
while (priority_queue):
    (hm, prefix_start) = heapq.heappop(priority_queue)

    try:
        # cached_prefix is the cached data about a previously evaluated prefix
        cached_prefix = cache[prefix_start]
    except:
        continue

    if (cached_prefix.lower_bound > min_objective):
        # we don't need to evaluate any prefixes that start with
        # prefix_start if its upper_bound is less than max_accuracy
        # dead_prefix_start[i] += 1
        print prefix_start, len(cache), 'lb(cached)>min', \
              '%1.3f %1.3f %1.3f' % (cached_prefix.objective,
                                     cached_prefix.lower_bound, min_objective)
        continue
    elif (cached_prefix.objective == cached_prefix.lower_bound):
        # stunted_prefix[i] += 1
        continue

    # num_already_captured is the number of data captured by the cached
    # prefix
    num_already_captured = cached_prefix.num_captured

    # num_already_correct is the number of data that are both captured by
    # the cached prefix and correctly predicted
    num_already_correct = cached_prefix.num_captured_correct

    # not_yet_captured is a binary vector of length ndata indicating which
    # data are not captured by the cached prefix
    not_yet_captured = cached_prefix.get_not_captured()

    cached_prediction = cached_prefix.prediction

    # construct a queue of all prefixes starting with prefix_start and
    # appended with one additional rule
    assert len(queue) == 0
    rules_to_consider = rule_set.difference(set(prefix_start))
    if len(prefix_start):
        last_rule = prefix_start[-1]
        rtc = rules_to_consider.difference(set(cdict[last_rule]))
        # commutes[i] += len(rules_to_consider) - len(rtc)
        rules_to_consider = rtc
    queue = [prefix_start + (t,) for t in list(rules_to_consider)]

    while(queue):
        # prefix is the first prefix tuple in the queue
        prefix = queue.pop(0)

        prefix_length = len(prefix)

        # compute cache entry for prefix via incremental computation, and
        # add to cache if relevant
        (max_accuracy, min_objective, best_prefix, cz, dp, ir) = \
            incremental(cache, prefix, rules, ones, ndata,
            num_already_captured, num_already_correct, not_yet_captured,
            cached_prediction, max_accuracy=max_accuracy,
            min_objective=min_objective, c=c, best_prefix=best_prefix,
            garbage_collect=garbage_collect, pdict=pdict, quiet=quiet)

        #captured_zero[i] += cz
        #dead_prefix[i] += dp
        #inferior[i] += ir

        if ((cz == 0) and (dp == 0) and (ir == 0)):
            heapq.heappush(priority_queue, (heap_metric(prefix), prefix))
            cache_size[prefix_length] += 1

    counter += 1
    if ((counter % 1000) == 0):
        fh.write(([counter, len(priority_queue)] + list(cache_size)).__repr__().strip('[]').replace(' ', '') + '\n')
        fh.flush()
        print counter, prefix, len(cache), len(priority_queue), max_accuracy, \
              min_objective, best_prefix, hm
        print cache_size

    if (len(cache) >= max_cache_size):
        break

#cache_size[i] = len(cache) - cache_size[:i].sum()
#seconds[i] = time.time() - tic

#assert ((cache_size[i] + commutes[i] + captured_zero[i] + dead_prefix[i] + inferior[i])
#       == ((nrules - i + 1) * (cache_size[i-1] - dead_prefix_start[i] - stunted_prefix[i])))

fh.write(([counter, len(priority_queue)] + list(cache_size)).__repr__().strip('[]').replace(' ', ''))
fh.close()

print 'max accuracy:', max_accuracy
print 'cache size:', cache_size.tolist()
print 'dead prefix start:', dead_prefix_start.tolist()
print 'caputed zero:', captured_zero.tolist()
print 'stunted prefix:', stunted_prefix.tolist()
print 'commutes:', commutes.tolist()
print 'dead prefix:', dead_prefix.tolist()
print 'inferior:', inferior.tolist()
print 'seconds:', [float('%1.2f' % s) for s in seconds.tolist()]
print 'growth:', [float('%1.2f' % s) for s in np.cast[float](cache_size[1:]) / cache_size[:-1]]

try:
    cc = cache[best_prefix]
    print_rule_list(cc.prefix, cc.prediction, cc.default_rule, rule_names)
    print cc
except:
    pass

fname = os.path.join(dout, '%s.txt' % metadata)
cache.to_file(fname=fname, delimiter=delimiter)
x = tb.tabarray(SVfile=fname, delimiter=delimiter)
x.sort(order=['length', 'first'])
x.saveSV(fname, delimiter=delimiter)

dfigs = os.path.join('..', 'figs')
if not os.path.exists(dfigs):
    os.mkdir(dfigs)

figs.make_figure(metadata=metadata, din=dout, dout=dfigs,
                 max_accuracy=max_accuracy, max_length=max_prefix_length)
