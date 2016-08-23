import os

import numpy as np
import gmpy2
from gmpy2 import mpz
import tabular as tb

import rule
import utils


class PrefixCache(dict):
    def __init__(self, do_garbage_collection=False, metrics=None, c=0.):
        # pdict is a dictionary used for garbage collection that groups together
        # prefixes that are equivalent up to a permutation; its keys are tuples
        # of sorted prefix indices; each key maps to a list of prefix tuples in
        # the cache that are equivalent
        self.pdict = {}
        self.do_garbage_collection = do_garbage_collection
        self.metrics = metrics
        self.best = None
        self.c = c
        self.max_prefix_len_check = None

    def insert(self, prefix, cache_entry, is_warm=False):
        self[prefix] = cache_entry
        n = len(prefix)
        if (n > 0 and not is_warm):
            parent = self[prefix[:-1]]
            parent.children.add(prefix[-1])
            parent.num_children += 1
            assert (len(parent.children) == parent.num_children), prefix
        self.metrics.cache_size[n] += 1
        return

    def update_lower_bound(self, prefix, lower_bound, min_objective):
        for j in range(len(prefix), -1, -1):
            px = prefix[:j]
            c = self[px]
            if (j != len(prefix)):
                lower_bound = max([self[px + (child,)].lower_bound for child in
                                   c.children])
            if (lower_bound < c.lower_bound):
                c.lower_bound = lower_bound
                if (self[px].lower_bound > min_objective):
                    self.delete(px)
            else:
                break
        return

    def prune_up(self, prefix):
        size_before_pu = self.metrics.cache_size.copy()
        for j in range(len(prefix), -1, -1):
            px = prefix[:j]
            if (self[px].num_children == 0):
                self.delete(px)
            else:
                break
        self.metrics.prune_up += (size_before_pu - self.metrics.cache_size)
        return

    def prune_down(self, prefix):
        """
        Called by `delete`.

        """
        sorted_prefix = tuple(np.sort(prefix))
        self.pdict.pop(sorted_prefix)
        self.metrics.pdict_length -= 1
        self.metrics.cache_size[len(prefix)] -= 1
        for c in self.pop(prefix).children:
            child = prefix + (c,)
            self.prune_down(child)
        return

    def delete(self, prefix):
        self.prune_down(prefix)
        if (len(prefix) > 0):
            parent = self[prefix[:-1]]
            parent.children.remove(prefix[-1])
            parent.num_children -= 1
        return

    def garbage_collect(self, min_objective, prefix_list=[()]):
        for prefix in prefix_list:
            cache_entry = self[prefix]
            if ((cache_entry.lower_bound + self.c) >= min_objective):
                self.delete(prefix)
            else:
                plist = [prefix + (child,) for child in cache_entry.children]
                self.garbage_collect(min_objective, plist)
                # delete the prefixes encountered that have no children
                # (seems costly, not sure)
                #if ((not hasattr(cache_entry, 'prefix')) and
                #    (cache_entry.num_children == 0)):
                #    self.delete(prefix)
        return

    def to_file(self, fname, delimiter='\t'):
        header = ['prefix', 'length', 'first', 'prediction', 'default',
                  'objective', 'lower_bound', 'accuracy', 'upper_bound',
                  'num_captured', 'num_captured_correct', 'num_not_captured',
                  'curiosity']
        lines = []
        for prefix in self:
            if hasattr(self[prefix], 'prefix'):
                lines.append('%s' % self[prefix].to_string(delimiter=delimiter))
        f = open(fname, 'w')
        f.write('%s\n' % delimiter.join(header))
        f.write('\n'.join(lines))
        f.close()
        return

    def print_cache(self, max_prefix_len):
        prefix_lens = [[0,0] for i in range(max_prefix_len + 1)]
        for entry in self:
            length = len(self[entry].prefix)
            lower, higher = prefix_lens[length]
            lb = self[entry].lower_bound
            print lb
            prefix_lens[length][0] = min(lb, prefix_lens[length][0])
            prefix_lens[length][1] = max(lb, prefix_lens[length][1])
        print prefix_lens

class CacheEntry:
    def __init__(self, prefix=None, prediction=None, default_rule=None,
                 accuracy=None, upper_bound=None, objective=None,
                 lower_bound=None, num_captured=None, num_captured_correct=None,
                 not_captured=None, curiosity=None):
        self.prefix = prefix
        self.prediction = prediction
        self.default_rule = default_rule
        self.accuracy = accuracy
        self.upper_bound = upper_bound
        self.objective = objective
        self.lower_bound = lower_bound
        self.num_captured = num_captured
        self.num_captured_correct = num_captured_correct
        self.not_captured = not_captured
        self.curiosity = curiosity
        self.children = set([])
        self.num_children = 0
        self.reject_set = set()

    def __repr__(self):
        if hasattr(self, 'num_captured'):
            s = '\n'.join(('prefix: %s' % self.prefix.__repr__(),
                       'prediction: %s' % self.prediction.__repr__(),
                       'accuracy: %1.10f' % self.accuracy,
                       'upper_bound: %1.10f' % self.upper_bound,
                       'objective: %1.10f' % self.objective,
                       'lower_bound: %1.10f' % self.lower_bound,
                       'num_captured: %d' % self.num_captured,
                       'num_captured_correct: %d' % self.num_captured_correct,
                       'sum(not_captured): %d' % rule.count_ones(self.not_captured),
                       'curiosity: %1.10f' % self.curiosity,
                       'num_children: %d' % self.num_children,
                       'reject_set: %s' % list(self.reject_set).__repr__()))
        else:
            s = '\n'.join(('lower_bound: %1.10f' % self.lower_bound,
                           'num_children: %d' % self.num_children,
                           'reject_set: %s' % list(self.reject_set).__repr__()))
        return s

    def clear(self):
        del self.prefix
        del self.prediction
        del self.default_rule
        del self.accuracy
        del self.upper_bound
        del self.objective
        del self.num_captured
        del self.num_captured_correct
        del self.not_captured
        del self.curiosity
        return

    def get_not_captured(self):
        """
        Maps string representation of attribute `not_captured` to mpz object.

        Returns a mpz object.

        """
        return self.not_captured

    def num_not_captured(self):
        return rule.count_ones(self.get_not_captured())

    def print_not_captured(self):
        s = ''.join(['1' if (i == '\x01') else '0' for i in self.not_captured])
        return s

    def first_rule(self):
        if (len(self.prefix) > 0):
            return self.prefix[0]
        else:
            return -1

    def to_kvpairs(self):
        kvp = (('prefix', self.prefix.__repr__().strip('()')),
               ('length', len(self.prefix)), ('first', str(self.first_rule())),
               ('prediction', self.prediction.__repr__().strip('()')),
               ('default', self.default_rule), ('accuracy', self.accuracy),
               ('upper_bound', self.upper_bound), ('objective', self.objective),
               ('lower_bound', self.lower_bound), ('num_captured', self.num_captured),
               ('num_captured_correct', self.num_captured_correct),
               ('num_not_captured', self.num_not_captured()),
               ('curiosity', self.curiosity))
        return kvp

    def to_record(self):
        return (self.prefix.__repr__().strip('()'), len(self.prefix),
                self.first_rule(), self.prediction.__repr__().strip('()'),
                self.default_rule, self.accuracy, self.upper_bound, self.objective,
                self.lower_bound, self.num_captured, self.num_captured_correct,
                self.num_not_captured(), self.curiosity)

    def to_string(self, delimiter='\t'):
        rec = (self.prefix.__repr__().strip('()'), str(len(self.prefix)),
               str(self.first_rule()), self.prediction.__repr__().strip('()'),
               str(self.default_rule), str(self.objective),
               str(self.lower_bound), str(self.accuracy), str(self.upper_bound),
               str(self.num_captured), str(self.num_captured_correct),
               str(self.num_not_captured()), str(self.curiosity))
        return delimiter.join(rec)

def print_rule_list(prefix, prediction, default_rule, rule_names):
    e = ''
    lines = []
    for (i, label) in zip(prefix, prediction):
        s = '%sif %s then predict %d' % (e, rule_names[i], label)
        print s
        lines += [s]
        e = 'else '
    s = 'else predict %d' % default_rule
    print s
    lines += [s]
    return '\n'.join(lines)

def incremental(cache, prefix, rules, ones, ndata, cached_prefix, c=0.,
                rule_names=None, min_captured_correct=0., quiet=True, part=None):
    """
    Compute cache entry for prefix via incremental computation.

    Add to cache if relevant.

    """
    new_best = False

    # num_already_captured is the number of data captured by the cached prefix
    num_already_captured = cached_prefix.num_captured

    # num_already_correct is the number of data that are both captured by the
    # cached prefix and correctly predicted
    num_already_correct = cached_prefix.num_captured_correct

    # not_yet_captured is a binary vector of length ndata indicating which data
    # are not captured by the cached prefix
    not_yet_captured = cached_prefix.get_not_captured()

    # cached_prediction is the tuple of binary predictions associated with the
    # cached prefix
    cached_prediction = cached_prefix.prediction

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

    # the additional rule is rejected if it doesn't capture any data
    ## Part 1: Captured zero
    if (not part or part == 1) and (num_captured < 1):
        cache.metrics.captured_zero[len(prefix)] += 1
        cache[prefix[:-1]].reject_set.add(new_rule)
        return

    # the additional rule is rejected if it doesn't capture enough data
    ## Part 2: Captured too few
    if (not part or part == 2) and (num_captured < (min_captured_correct * ndata)):
        cache.metrics.captured_zero[len(prefix)] += 1
        cache[prefix[:-1]].reject_set.add(new_rule)
        return

    # the additional rule is rejected if it captures all remaining data
    # (equivalent to the default rule)
    ## Part 3: Equivalent to default
    if (not part or part == 3) and (num_captured == (ndata - num_already_captured)):
        cache.metrics.captured_all[len(prefix)] += 1
        cache[prefix[:-1]].reject_set.add(new_rule)
        return

    # not_captured is a binary vector of length ndata indicating those
    # data that are not captured by the current prefix, i.e., not
    # captured by the rule list given by the cached prefix appended with
    # the new rule
    not_cappd = rule.rule_vandnot(not_yet_captured, rules[new_rule])
    not_captured = not_cappd[0]
    assert not_yet_captured == (not_captured | captured_nz)

    # num_not_captured is the number of data not captured by prefix
    num_not_captured = not_cappd[1]

    # the data not captured by the cached prefix are either captured or
    # not captured by the new rule
    assert rule.count_ones(not_yet_captured) == (num_captured + num_not_captured)

    # num_captured_ones is the number of data captured by the new rule,
    # given the cached prefix, with label 1
    num_captured_ones = rule.rule_vand(captured_nz, ones)[1]

    # num_captured_zeros is the number of data captured by the new rule,
    # given the cached prefix, with label 0
    num_captured_zeros = num_captured - num_captured_ones

    if (num_captured_ones > num_captured_zeros):
        # new_prediction is the prediction of the new rule, given the
        # cached prefix
        new_prediction = 1

        # num_captured_correct is the number of data captured by the new
        # rule, given the cached prefix, with label 1
        num_captured_correct = num_captured_ones
    else:
        # new_prediction is the prediction of the new rule, given the
        # cached prefix
        new_prediction = 0

        # num_captured_correct is the number of data captured by the new
        # rule, given the cached prefix, with label 0
        num_captured_correct = num_captured_zeros

    # the additional rule is insufficient if it doesn't correctly capture enough
    # data
    ## Part 4: Doesn't correctly capture enough
    if (not part or part == 4) and (num_captured_correct < (min_captured_correct * ndata)):
        cache.metrics.insufficient[len(prefix)] += 1
        cache[prefix[:-1]].reject_set.add(new_rule)
        return

    # the data captured by prefix are either captured by the cached
    # prefix or captured by the new rule
    new_num_captured = num_already_captured + num_captured

    # num_correct is the number of data captured by prefix and
    # correctly predicted
    num_correct = num_already_correct + num_captured_correct

    # the number of data captured by prefix and incorrectly predicted
    num_incorrect = new_num_captured - num_correct

    # the lower bound on the objective is the sum of the lower bound on the
    # number of mistakes and a constant times the prefix size
    lower_bound = float(num_incorrect) / ndata + c * len(prefix)

    # if the lower bound of prefix is not less than min_objective, then we don't
    # create a cache entry for prefix
    ## Part 5: Lower bound > Min objective
    if (not part or part == 5) and (lower_bound >= cache.metrics.min_objective):
        cache.metrics.dead_prefix[len(prefix)] += 1
        return

    # compute the default rule on the not captured data
    (default_rule, num_default_correct) = \
        compute_default(rule.rule_vand(ones, not_captured)[0], num_not_captured)

    # the number of incorrect corrections made by the rule list (with default)
    num_mistakes = ndata - num_correct - num_default_correct

    # the objective is the sum of the fraction of mistakes and regularization
    objective = float(num_mistakes) / ndata + c * len(prefix)

    # new_best is True if prefix has the new best objective
    if (objective < cache.metrics.min_objective):
        new_best = True

    # if prefix's children are longer than than max_prefix_len_check,
    # then we don't create a cache entry for prefix
    ## Part 6: Children longer than max prefix len
    if (not part or part == 6) and ((len(prefix) + 1) > cache.max_prefix_len_check):
        cache.metrics.dead_prefix[len(prefix)] += 1
        if not new_best:
            return

    # if the lower bound of prefix's children is not less than min_objective,
    # then we don't create a cache entry for prefix
    ## Part 7: Lower bound of children > Min objective
    if (not part or part == 7) and ((lower_bound + c) >= cache.metrics.min_objective):
        cache.metrics.dead_prefix[len(prefix)] += 1
        if not new_best:
            return

    # to do garbage collection, we keep look for prefixes that are
    # equivalent up to permutation
    ## Part 8: Permutation garbage collection
    if (not part or part == 8) and cache.do_garbage_collection:
        # sorted_prefix lists the prefix's indices in sorted order
        sorted_prefix = tuple(np.sort(prefix))
        if sorted_prefix in cache.pdict:
            (equiv_prefix, equiv_objective) = cache.pdict[sorted_prefix]
            if (objective < equiv_objective):
                # equiv_prefix is inferior to prefix
                cache.delete(equiv_prefix)
                assert (cache[equiv_prefix[:-1]].num_children == len(cache[equiv_prefix[:-1]].children))
                # prune_up the from the deleted equiv_prefix
                # (seems costly, not sure)
                #if (cache[equiv_prefix[:-1]].num_children == 0):
                #    cache.prune_up(equiv_prefix[:-1])
                cache.metrics.inferior[len(prefix)] += 1
                cache.pdict[sorted_prefix] = (prefix, objective)
                cache.metrics.pdict_length += 1
            else:
                # prefix is inferior to the stored equiv_prefix
                cache.metrics.inferior[len(prefix)] += 1
                return
        else:
            cache.pdict[sorted_prefix] = (prefix, objective)
            cache.metrics.pdict_length += 1

    # the data correctly predicted by prefix are either correctly
    # predicted by cached_prefix, captured and correctly predicted by
    # new_rule, or are not captured by prefix and correctly predicted by
    # the default rule
    accuracy = float(num_correct + num_default_correct) / ndata

    # the upper bound on the accuracy of a rule list starting with
    # prefix is like the accuracy computation, except we assume that all
    # data not captured by prefix are correctly predicted
    upper_bound = float(num_correct + num_not_captured) / ndata

    # curiosity = prefix misclassification + regularization
    curiosity = (float(num_incorrect) / new_num_captured +
                 c * len(prefix) * ndata / new_num_captured)

    # the predictions of prefix are those of the cached prefix appended by
    # the prediction associated with data captured by the new rule
    prediction = cached_prediction + (new_prediction,)

    # make a cache entry for prefix
    cache_entry = CacheEntry(prefix=prefix, prediction=prediction,
                             default_rule=default_rule,
                             accuracy=accuracy, upper_bound=upper_bound,
                             objective=objective, lower_bound=lower_bound,
                             num_captured=new_num_captured,
                             num_captured_correct=num_correct,
                             not_captured=not_captured, curiosity=curiosity)

    # if prefix is the new best known prefix, update min_objective,
    # best_prefix, and accuracy
    if new_best:
        cache.metrics.accuracy = accuracy
        print 'min:', cache.metrics.min_objective, '->', objective
        cache.metrics.min_objective = objective
        cache.metrics.best_prefix = prefix
        cache.best = cache_entry
        cache.max_prefix_len_check = int(np.floor(objective / c))

    return cache_entry

def given_prefix(full_prefix, cache, rules, ones, ndata, c=0.,
                 min_captured_correct=None):
    """
    Compute accuracy of a given prefix via incremental computation.

    """
    for i in range(len(full_prefix)):
        prefix_start = full_prefix[:i]

        # cached_prefix is the cached data about a previously evaluated prefix
        cached_prefix = cache[prefix_start]

        prefix = prefix_start + (full_prefix[i],)

        cache_entry = \
            incremental(cache, prefix, rules, ones, ndata, cached_prefix, c=c,
                        min_captured_correct=min_captured_correct)
        if (cache_entry is not None):
            cache[prefix] = cache_entry

    return (cache.metrics.accuracy, cache.metrics.min_objective, cache.metrics.best_prefix)

def file_to_dict(fname, seed=None, sample=None):
    """
    Utility that constructs a dictionary from a file.

    Map each line in the file to a (key, value) pair where the key is a string
    equal to the first word in the file and the value is an integer numpy.array
    constructed from the remaining words, which are each assumed to be 0 or 1.

    Used to read in the input files, label_file and out_file.

    """
    line_vec = [line.split() for line in
                open(fname, 'rU').read().strip().split('\n')]

    if (sample is not None):
        ndata = len(line_vec[0][1:])
        nsample = int(sample * ndata)
        np.random.seed(seed)
        ind = np.random.permutation(ndata)[:nsample] + 1

    d = {}
    for line in line_vec:
        if sample is not None:
            truthtable = "".join([line[i] for i in ind])
        else:
            truthtable = "".join(line[1:])
        # to prevent clearing of leading zeroes
        truthtable = '1' + truthtable
        bitstring = mpz(truthtable, 2)
        d[line[0]] = bitstring
    return d

def read_data(fname, seed=None, sample=None):
    """
    Utility to read a `.out` data file.

    Map each line in the file to a (key, value) pair where the key is a string
    equal to the first word in the file and the value is an integer numpy.array
    constructed from the remaining words, which are each assumed to be 0 or 1.
    The keys and values are stored in two separate arrays whose indices
    correspond.

    """
    line_vec = [line.split() for line in
                open(fname, 'rU').read().strip().split('\n')]

    if (sample is not None):
        ndata = len(line_vec[0][1:])
        nsample = int(sample * ndata)
        np.random.seed(seed)
        ind = np.random.permutation(ndata)[:nsample] + 1

    rule_names = []
    rules = []
    for line in line_vec:
        if sample is not None:
            truthtable = "".join([line[i] for i in ind])
        else:
            truthtable = "".join(line[1:])
        # to prevent clearing of leading zeroes
        truthtable = '1' + truthtable
        bitstring = mpz(truthtable, 2)
        rule_names.append(line[0])
        rules.append(bitstring)
    return (rule_names, rules)

def compute_default(ones, num_uncaptured):
    """
    Computes default rule given an mpz representation of uncaptured samples.

    Given an mpz representation of the uncaptured samples and the number of
    samples, returns a default rule.

    """
    n1 = rule.count_ones(ones)
    n0 = num_uncaptured - n1
    if (n1 > n0):
        default_rule = 1
        num_default_correct = n1
    else:
        default_rule = 0
        num_default_correct = n0
    return (default_rule, num_default_correct)

def greedy_rule_list(ones, rules, c, max_length):
    """
    Grow the rule list greedily.

    This can provide a good warm start solution for another algorithm.

    """
    greedy_prefix = ()
    predicted_labels = ()
    nrules = len(rules)
    # Strip leading one
    ndata = rules[0].num_digits(2) - 1
    unseen = rule.make_all_ones(ndata + 1)
    not_captured = ndata
    num_captured_correct = 0

    for i in range(max_length):
        best = (0, 0, -1, None, None)
        for j in xrange(nrules):
            captured, num_cappd = rule.rule_vand(unseen, rules[j])
            if num_cappd == 0:
                continue
            captured_labels, num_captured_ones = rule.rule_vand(captured, ones)
            percent_ones = float(num_captured_ones) / num_cappd
            pred = 1 if percent_ones >= 0.5 else 0
            magnitude = abs(percent_ones - 0.5)
            if magnitude > best[0] or (magnitude == best[0] and num_cappd > best[1]):
                best = (magnitude, num_cappd, j, rules[j], pred)
        num_captured_correct += (2 * best[0] * best[1])
        not_captured -= best[1]
        unseen = rule.rule_vandnot(unseen, best[3])[0]
        greedy_prefix += (best[2],)
        predicted_labels += (best[4],)


    (default_rule, num_default_correct) = compute_default(unseen, not_captured)
    num_captured = ndata - not_captured
    num_incorrect = num_captured - num_captured_correct

    print 'Num cappd', num_captured
    print 'Num cappd corr', num_captured_correct
    print 'Not cappd', not_captured
    print 'Num incorr', num_incorrect
    print 'Default corr', num_default_correct

    accuracy = float(num_captured_correct + num_default_correct) / ndata
    upper_bound = float(num_captured_correct + not_captured) / ndata
    objective = float(num_incorrect) / ndata + c * len(greedy_prefix)
    lower_bound = float(ndata - num_captured_correct - num_default_correct) / ndata + c * len(greedy_prefix)
    curiosity = (float(num_incorrect) / num_captured +
                 c * len(greedy_prefix) * ndata / num_captured)

    greedy_prefix += (default_rule,)

    print 'Accuracy', accuracy
    print 'Upper bound', upper_bound
    print 'Objective', objective
    print 'Lower_bound', lower_bound
    print 'Curiosity', curiosity
    return (greedy_prefix, predicted_labels, default_rule, accuracy, upper_bound, objective,
            lower_bound, num_captured, num_captured_correct, unseen, curiosity)

def initialize(din, dout, label_file, out_file, warm_start, max_accuracy,
               min_objective, best_prefix, seed=None, sample=None,
               do_garbage_collection=False, max_greedy_length=8,
               max_prefix_length=20, c=0.):

    if not os.path.exists(dout):
        os.mkdir(dout)

    # label_dict maps each label to a binary integer vector of length ndata
    label_dict = file_to_dict(os.path.join(din, label_file), seed=seed, sample=sample)
    ndata = label_dict['{label=1}'].num_digits(2) - 1
    assert(rule.count_ones(label_dict['{label=1}']) == (ndata - rule.count_ones(label_dict['{label=0}'])))

    # rules[i] is a bitstring of length ndata with label given by rule_names[i]
    (rule_names, rules) = read_data(os.path.join(din, out_file), seed=seed, sample=sample)

    # ones a binary integer vector of length ndata
    # ones[j] = 1 iff label(data[j]) = 1
    ones = label_dict['{label=1}']

    # rules is an (nrules x ndata) binary integer matrix indicating
    # rules[i, j] = 1 iff data[j] obeys the ith rule
    nrules = len(rule_names)
    rule.lead_one = mpz(pow(2, ndata))

    # rule_set is a set of all rule indices
    rule_set = set(range(nrules))

    # for the empty prefix, compute the default rule and number of data it
    # correctly predicts
    (empty_default, empty_num_correct) = compute_default(ones, ndata)
    empty_accuracy = float(empty_num_correct) / ndata
    empty_objective = float(ndata - empty_num_correct) / ndata
    empty_lower_bound = 0.

    # max_accuracy is the accuracy of the best_prefix observed so far
    # if not already defined, either use a greedy algorithm to compute a warm
    # start or start cold with an empty prefix
    if (max_accuracy is None or max_accuracy == 0):
        if warm_start:
            # compute warm start rule list using a greedy algorithm
            (best_prefix, greedy_prediction, greedy_default,
             max_accuracy, greedy_upper_bound, min_objective, 
             greedy_lower_bound, greedy_num_captured, greedy_num_captured_correct,
             greedy_not_captured, greedy_curiosity) = \
                         greedy_rule_list(ones, rules, c, max_length=max_greedy_length)
            print 'greedy solution:'
            print_rule_list(best_prefix, greedy_prediction, greedy_default, rule_names)
        else:
            best_prefix = ()
            max_accuracy = empty_accuracy
            min_objective = empty_objective

    metrics = utils.Metrics(max_prefix_length + 1)
    metrics.cache_size[0] = 0
    metrics.priority_queue_length = 0
    metrics.best_prefix = best_prefix
    metrics.min_objective = min_objective
    metrics.accuracy = max_accuracy

    # cache is a PrefixCache object, which is a dictionary that stores
    # prefix-related computations, where each key-value pair maps a prefix
    # tuples to a CacheEntry object
    cache = PrefixCache(do_garbage_collection=do_garbage_collection,
                        metrics=metrics, c=c)

    if warm_start:
        cache_entry = CacheEntry(prefix=best_prefix, prediction=greedy_prediction,
                                        default_rule=greedy_default, accuracy=max_accuracy,
                                        upper_bound=greedy_upper_bound, objective=min_objective,
                                        lower_bound=greedy_lower_bound, num_captured=greedy_num_captured,
                                        num_captured_correct=greedy_num_captured_correct,
                                        not_captured=greedy_not_captured, curiosity=greedy_curiosity)
        cache.insert(best_prefix, cache_entry, is_warm=True)
    else:
        # initialize the cache with a single entry for the empty rule list
        cache_entry = CacheEntry(prefix=(), prediction=(),
                             default_rule=empty_default,
                             accuracy=empty_accuracy, upper_bound=1.,
                             objective=empty_objective,
                             lower_bound=empty_lower_bound,
                             num_captured=0, num_captured_correct=0,
                             not_captured=rule.make_all_ones(ndata + 1),
                             curiosity=0.)
        cache.insert((), cache_entry)

    cache.metrics.inserts[0] = 1
    cache.pdict[best_prefix] = (best_prefix, cache_entry.objective)
    cache.metrics.pdict_length += 1

    print cache
    return (nrules, ndata, ones, rules, rule_set, rule_names, max_accuracy,
            min_objective, best_prefix, cache)
