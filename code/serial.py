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

import numpy as np
import tabular as tb

from branch_bound import CacheEntry, initialize, compute_default


din = os.path.join('..', 'data')
dout = os.path.join('..', 'cache')
label_file = 'tdata_R.label'
out_file = 'tdata_R.out'
warm_start = True
max_accuracy = None
best_prefix = None
max_prefix_length = 2
delimiter = '\t'

(nrules, ndata, ones, rules, rule_set, rule_names,
 max_accuracy, best_prefix, cache) = initialize(din, dout, label_file, out_file,
                                          warm_start, max_accuracy, best_prefix)

# queue is a list of tuples encoding prefixes in the queue, where the ith entry
# in such a tuple is the (row) index of a rule in the rules matrix
# initialize the queue to include all rules of length 1
queue = [(r,) for r in range(len(rules))]

while(queue):
    # prefix the first prefix tuple in the queue
    prefix = queue.pop(0)

    # prefix is the concatenation of a previously seen prefix and a rule
    # cached_prefix is the cached data about this prefix
    # new_rule is the (row) index of this additional rule in the rules matrix
    cached_prefix = cache[prefix[:-1]]
    new_rule = prefix[-1]

    # don't need to evaluate prefix if it starts with a prefix whose
    # upper_bound is less than max_accuracy
    if (cached_prefix.upper_bound < max_accuracy):
        print (prefix,
               '(cached_prefix.upper_bound = %1.3f) < (max_accuracy = %1.3f)' %
               (cached_prefix.upper_bound, max_accuracy))
        continue

    # num_already_captured is the number of data captured by the cached prefix
    num_already_captured = cached_prefix.num_captured

    # num_already_correct is the number of data that are both captured by the
    # cached prefix and correctly predicted
    num_already_correct = cached_prefix.num_captured_correct

    # not_yet_captured is a binary vector of length ndata indicating which data
    # are not captured by the cached prefix
    not_yet_captured = cached_prefix.get_not_captured()

    # captured_nz is an array of indices of data captured by the additional
    # rule, given the cached prefix
    captured_nz = (not_yet_captured & rules[new_rule]).nonzero()[0]

    # num_captured is the number of data captured by the additional rule, given
    # the cached prefix
    num_captured = len(captured_nz)

    # the additional rule is useless if it doesn't capture any data
    if (num_captured == 0):
        print prefix, 'num_captured == 0'
        continue

    # not_captured is a binary vector of length ndata indicating those data that
    # are not captured by the current prefix, i.e., not captured by the rule
    # list given by the cached prefix appended with the additional rule
    not_captured = not_yet_captured & (1 - rules[new_rule])

    # not_captured_nz is an array of data indices not captured by prefix
    not_captured_nz = (not_captured).nonzero()[0]

    # num_not_captured is the number of data not captured by prefix
    num_not_captured = len(not_captured_nz)

    # the data not captured by the cached prefix are either captured or not
    # captured by the additional rule
    assert not_yet_captured.sum() == (num_captured + num_not_captured)

    # num_captured_ones is the number of data captured by the additional rule,
    # given the cached prefix, with label 1
    num_captured_ones = ones[captured_nz].sum()

    # fraction_captured_ones is the fraction of data captured by the additional
    # rule, given the cached prefix, with label 1
    fraction_captured_ones = float(num_captured_ones) / num_captured

    if (fraction_captured_ones >= 0.5):
        # the predictions of prefix are those of cached_prefix appended by the
        # prediction that the data captured by the additional rule have label 1
        prediction = cached_prefix.prediction + (1,)

        # num_captured_correct is the number of data captured by the additional
        # rule, given the cached prefix, with label 1
        num_captured_correct = num_captured_ones
    else:
        # the predictions of prefix are those of cached_prefix appended by the
        # prediction that the data captured by the additional rule have label 0
        prediction = cached_prefix.prediction + (0,)

        # num_captured_correct is the number of data captured by the additional
        # rule, given the cached prefix, with label 0
        num_captured_correct = num_captured - num_captured_ones

	# compute the default rule on the not captured data
	(default_rule, num_default_correct) = compute_default(ones[not_captured_nz])

	# the data correctly predicted by prefix are either correctly predicted
	# by cached_prefix, captured and correctly predicted by new_rule, or are not
	# captured by prefix and correctly predicted by the default rule
	accuracy = float(num_already_correct + num_captured_correct +
					 num_default_correct) / ndata

	# the upper bound on the accuracy of a rule list starting with prefix
	# is like the accuracy computation, except we assume that all data not
	# captured by prefix are correctly predicted
	upper_bound = float(num_already_correct + num_captured_correct +
						num_not_captured) / ndata

    # if prefix is the new best known prefix, update max_accuracy and
    # best_prefix
    if (accuracy > max_accuracy):
        max_accuracy = accuracy
        best_prefix = prefix

    # if the upper bound of prefix exceeds max_accuracy, then create a cache
    # entry for prefix and add to the queue new prefixes starting with prefix
    if (upper_bound > max_accuracy):

        # the data captured by prefix are either captured by the cached prefix
        # or captured by the additional rule
        new_num_captured = num_already_captured + num_captured

        # num_correct is the number of data captured by prefix and that are
        # correct
        num_correct = num_already_correct + num_captured_correct

        # make a cache entry for prefix
        cache[prefix] = CacheEntry(prefix=prefix, prediction=prediction,
                                   default_rule=default_rule, accuracy=accuracy,
                                   upper_bound=upper_bound,
                                   num_captured=new_num_captured,
                                   num_captured_correct=num_correct,
                                   not_captured=not_captured)

        # extend the queue with all prefixes starting with prefix and append
        # with one additional rule
        if (len(prefix) < max_prefix_length):
            queue.extend([prefix + (t,) for t in
                          list(rule_set.difference(set(prefix)))])

fname = os.path.join(dout, 'serial-max_accuracy=%1.3f-max_length=%d.txt' %
                           (max_accuracy, max_prefix_length))
cache.to_file(fname=fname, delimiter=delimiter)
x = tb.tabarray(SVfile=fname, delimiter=delimiter)
x.sort(order=['length', 'first'])
x.saveSV(fname, delimiter=delimiter)
