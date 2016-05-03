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
import os
import time

import numpy as np
import gmpy2
from gmpy2 import mpz
import tabular as tb

from branch_bound import CacheEntry, initialize, compute_default, print_rule_list
import figs
import rule

din = os.path.join('..', 'data')
dout = os.path.join('..', 'cache')
froot = 'tdata_R'
warm_start = True ## greedy algorithm is currently broken
max_accuracy = 0.999
best_prefix = None
max_prefix_length = 5
delimiter = '\t'
quiet = True
garbage_collect = True
seed = None
sample = None

#"""
froot = 'adult_R'
max_accuracy = 0.835438
max_prefix_length = 1
seed = 0
sample = 0.1
#"""

label_file = '%s.label' % froot
out_file = '%s.out' % froot

(nrules, ndata, ones, rules, rule_set, rule_names,
 max_accuracy, best_prefix, cache) = initialize(din, dout, label_file, out_file,
                                        warm_start, max_accuracy, best_prefix,
                                        seed, sample)

print froot
print 'nrules:', nrules
print 'ndata:', ndata

# queue is a list of tuples encoding prefixes in the queue, where the ith entry
# in such a tuple is the (row) index of a rule in the rules matrix
queue = []

m = max_prefix_length + 1

cache_size = np.zeros(m, int)
cache_size[0] = 1

dead_prefix_start = np.zeros(m, int)
captured_zero = np.zeros(m, int)
stunted_prefix = np.zeros(m, int)
dead_prefix = np.zeros(m, int)
inferior = np.zeros(m, int)

seconds = np.zeros(m)

# lazily add prefixes to the queue
for i in range(1, max_prefix_length + 1):
    print 'prefix length:', i
    tic = time.time()

    # prefix_list is a list of prefixes in the cache after the last round
    prefix_list = [p for p in cache if (len(p) == (i - 1))]

    # pdict is a dictionary used for garbage collection that groups together prefixes that
    # are equivalent up to a permutation; its keys are tuples of sorted prefix indices;
    # each key maps to a list of prefix tuples in the cache that are equivalent
    pdict = {}

    for prefix_start in prefix_list:
        # cached_prefix is the cached data about a previously evaluated prefix
        cached_prefix = cache[prefix_start]

        if (cached_prefix.upper_bound < max_accuracy):
            # we don't need to evaluate any prefixes that start with
            # prefix_start if its upper_bound is less than max_accuracy
            dead_prefix_start[i] += 1
            print i, prefix_start, len(cache), 'ub(cached)<max', \
                  '%1.3f %1.3f %1.3f' % (cached_prefix.accuracy,
                                        cached_prefix.upper_bound, max_accuracy)
            continue
        elif (cached_prefix.accuracy == cached_prefix.upper_bound):
            # in this case, no rule list starting with and longer than
            # prefix_start can achieve a higher accuracy
            stunted_prefix[i] += 1
            continue

        #if (cached_prefix.curiosity > 0.02):
        #    continue

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
        queue = [prefix_start + (t,) for t in list(rule_set.difference(set(prefix_start)))]

        while(queue):
            # prefix is the first prefix tuple in the queue
            prefix = queue.pop(0)

            # new_rule is the (row) index in the rules matrix of the last rule
            # in prefix, which starts with prefix_start
            new_rule = prefix[-1]

            # captured_nz is an bitmap of data captured by the new
            # rule, given the cached prefix
            cappd = rule.rule_vand(not_yet_captured, rules[new_rule])
            captured_nz = cappd[0]

            # num_captured is the number of data captured by the new rule, given
            # the cached prefix
            num_captured = cappd[1]

            # the additional rule is useless if it doesn't capture any data
            if (num_captured == 0):
                captured_zero[i] += 1
                if not quiet:
                    print i, prefix, len(cache), 'num_captured=0', \
                          '%d %d %d' % (-1, -1, -1)
                continue

            # not_captured is a binary vector of length ndata indicating those
            # data that are not captured by the current prefix, i.e., not
            # captured by the rule list given by the cached prefix appended with
            # the new rule
            not_cappd = rule.rule_vandnot(not_yet_captured, rules[new_rule])
            not_captured = not_cappd[0]
            assert not_yet_captured == (not_captured | captured_nz) 

            # not_captured_nz is an array of data indices not captured by prefix
            #not_captured_nz = not_cappd[1]

            # num_not_captured is the number of data not captured by prefix
            num_not_captured = not_cappd[1]

            # the data not captured by the cached prefix are either captured or
            # not captured by the new rule
            assert rule.count_ones(not_yet_captured) == (num_captured + num_not_captured)

            # num_captured_ones is the number of data captured by the new rule,
            # given the cached prefix, with label 1
            num_captured_ones = rule.rule_vand(captured_nz, ones)[1]

            # fraction_captured_ones is the fraction of data captured by the new
            # rule, given the cached prefix, with label 1
            fraction_captured_ones = float(num_captured_ones) / num_captured

            if (fraction_captured_ones >= 0.5):
                # the predictions of prefix are those of the cached prefix
                # appended by the prediction that the data captured by the new
                # rule have label 1
                prediction = cached_prediction + (1,)

                # num_captured_correct is the number of data captured by the new
                # rule, given the cached prefix, with label 1
                num_captured_correct = num_captured_ones
            else:
                # the predictions of prefix are those of the cached prefix
                # appended by the prediction that the data captured by the new
                # rule have label 0
                prediction = cached_prediction + (0,)

                # num_captured_correct is the number of data captured by the new
                # rule, given the cached prefix, with label 0
                num_captured_correct = num_captured - num_captured_ones

            # compute the default rule on the not captured data
            (default_rule, num_default_correct) = \
                                          compute_default(rule.rule_vand(ones, not_captured)[0], num_not_captured)

            # the data correctly predicted by prefix are either correctly
            # predicted by cached_prefix, captured and correctly predicted by
            # new_rule, or are not captured by prefix and correctly predicted by
            # the default rule
            accuracy = float(num_already_correct + num_captured_correct +
                             num_default_correct) / ndata
            assert accuracy <= 1

            # the upper bound on the accuracy of a rule list starting with
            # prefix is like the accuracy computation, except we assume that all
            # data not captured by prefix are correctly predicted
            upper_bound = float(num_already_correct + num_captured_correct +
                                num_not_captured) / ndata

            # if the upper bound of prefix exceeds max_accuracy, then create a
            # cache entry for prefix
            if (upper_bound <= max_accuracy):
                dead_prefix[i] += 1
                if not quiet:
                    print i, prefix, len(cache), 'ub<=max', \
                          '%1.3f %1.3f %1.3f' % (accuracy, upper_bound, max_accuracy)
            else:
                # if prefix is the new best known prefix, update max_accuracy
                # and best_prefix
                if (accuracy > max_accuracy):
                    max_accuracy = accuracy
                    best_prefix = prefix

                # the data captured by prefix are either captured by the cached
                # prefix or captured by the new rule
                new_num_captured = num_already_captured + num_captured

                # num_correct is the number of data captured by prefix and
                # correctly predicted
                num_correct = num_already_correct + num_captured_correct

                # num_incorrect is the number of data captured by prefix and
                # incorrectly predicted
                num_incorrect = new_num_captured - num_correct

                # curiosity = prefix misclassification
                curiosity = float(num_incorrect) / new_num_captured

                # to do garbage collection, we keep look for prefixes that are
                # equivalent up to permutation
                if garbage_collect:

                    # sorted_prefix lists the prefix's indices in sorted order
                    sorted_prefix = tuple(np.sort(prefix))

                    if sorted_prefix in pdict:
                        (equiv_prefix, equiv_accuracy) = pdict[sorted_prefix]
                        inferior[i] += 1
                        if (accuracy > equiv_accuracy):
                            # equiv_prefix is inferior to prefix
                            cache.pop(equiv_prefix)
                            pdict[sorted_prefix] = (prefix, accuracy)
                        else:
                            # prefix is inferior to the stored equiv_prefix
                            continue
                    else:
                        pdict[sorted_prefix] = (prefix, accuracy)

                # make a cache entry for prefix
                cache[prefix] = CacheEntry(prefix=prefix, prediction=prediction,
                                           default_rule=default_rule,
                                           accuracy=accuracy,
                                           upper_bound=upper_bound,
                                           num_captured=new_num_captured,
                                           num_captured_correct=num_correct,
                                           not_captured=not_captured,
                                           curiosity=curiosity)

                if not quiet:
                    print i, prefix, len(cache), 'ub>max', \
                         '%1.3f %1.3f %1.3f' % (accuracy, upper_bound, max_accuracy)

    cache_size[i] = len(cache) - cache_size[:i].sum()
    seconds[i] = time.time() - tic

    assert ((cache_size[i] + captured_zero[i] + dead_prefix[i] + inferior[i])
            == ((nrules - i + 1) * (cache_size[i-1] - dead_prefix_start[i] - stunted_prefix[i])))

    print 'max accuracy:', max_accuracy
    print 'cache size:', cache_size.tolist()
    print 'dead prefix start:', dead_prefix_start.tolist()
    print 'caputed zero:', captured_zero.tolist()
    print 'stunted prefix:', stunted_prefix.tolist()
    print 'dead prefix:', dead_prefix.tolist()
    print 'inferior:', inferior.tolist()
    print 'seconds:', [float('%1.2f' % s) for s in seconds.tolist()]

metadata = ('%s-serial_gc-max_accuracy=%1.3f-max_length=%d' %
            (froot, max_accuracy, max_prefix_length))
fname = os.path.join(dout, '%s.txt' % metadata)
cache.to_file(fname=fname, delimiter=delimiter)
x = tb.tabarray(SVfile=fname, delimiter=delimiter)
x.sort(order=['length', 'first'])
x.saveSV(fname, delimiter=delimiter)

bp = x['prefix'][x['accuracy'] == x['accuracy'].max()][0]
c = cache[tuple([int(j) for j in [k for k in bp.split(',') if k]])]
print_rule_list(c.prefix, c.prediction, c.default_rule, rule_names)

print c

dfigs = os.path.join('..', 'figs')
if not os.path.exists(dfigs):
    os.mkdir(dfigs)

figs.make_figure(metadata=metadata, din=dout, dout=dfigs,
                 max_accuracy=max_accuracy, max_length=max_prefix_length)
