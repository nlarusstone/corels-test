import os

import numpy as np
import gmpy2
from gmpy2 import mpz
import tabular as tb

import rule


class PrefixCache(dict):
    def to_file(self, fname, delimiter='\t'):
        header = ['prefix', 'length', 'first', 'prediction', 'default',
                  'accuracy', 'upper_bound', 'num_captured',
                  'num_captured_correct', 'num_not_captured', 'curiosity']
        lines = []
        for c in self.values():
            lines.append('%s' % c.to_string())
        f = open(fname, 'w')
        f.write('%s\n' % delimiter.join(header))
        f.write('\n'.join(lines))
        f.close()

class CacheEntry:
    def __init__(self, prefix=None, prediction=None, default_rule=None,
                 accuracy=None, upper_bound=None, num_captured=None,
                 num_captured_correct=None, not_captured=None, curiosity=None):
        self.prefix = prefix
        self.prediction = prediction
        self.default_rule = default_rule
        self.accuracy = accuracy
        self.upper_bound = upper_bound
        self.num_captured = num_captured
        self.num_captured_correct = num_captured_correct
        self.not_captured = not_captured
        self.curiosity = curiosity

    def __repr__(self):
        s = '\n'.join(('prefix: %s' % self.prefix.__repr__(),
                       'prediction: %s' % self.prediction.__repr__(),
                       'accuracy: %1.10f' % self.accuracy,
                       'upper_bound: %1.10f' % self.upper_bound,
                       'num_captured: %d' % self.num_captured,
                       'num_captured_correct: %d' % self.num_captured_correct,
                       'sum(not_captured): %d' % rule.count_ones(self.not_captured),
                       'curiosity: %1.3f' % self.curiosity))
        return s

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
               ('upper_bound', self.upper_bound),
               ('num_captured', self.num_captured),
               ('num_captured_correct', self.num_captured_correct),
               ('num_not_captured', self.num_not_captured()),
               ('curiosity', self.curiosity))
        return kvp

    def to_record(self):
        return (self.prefix.__repr__().strip('()'), len(self.prefix),
                self.first_rule(), self.prediction.__repr__().strip('()'),
                self.default_rule, self.accuracy, self.upper_bound,
                self.num_captured, self.num_captured_correct,
                self.num_not_captured(), self.curiosity)

    def to_string(self):
        rec = (self.prefix.__repr__().strip('()'), str(len(self.prefix)),
               str(self.first_rule()), self.prediction.__repr__().strip('()'),
               str(self.default_rule), str(self.accuracy),
               str(self.upper_bound), str(self.num_captured),
               str(self.num_captured_correct), str(self.num_not_captured()),
               str(self.curiosity))
        return '\t'.join(rec)

def print_rule_list(prefix, prediction, default_rule, rule_names):
    e = ''
    for (i, label) in zip(prefix, prediction):
        print '%sif %s then predict %d' % (e, rule_names[i], label)
        e = 'else '
    print 'else predict %d' % default_rule

def incremental(cache, prefix, rules, ones, ndata, num_already_captured,
                num_already_correct, not_yet_captured, cached_prediction,
                max_accuracy=0, best_prefix=None, garbage_collect=False,
                pdict=None, quiet=True):
    """
    Compute cache entry for prefix via incremental computation.

    Add to cache if relevant.

    """
    captured_zero = 0
    dead_prefix = 0
    inferior = 0

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
        captured_zero = 1
        if not quiet:
            print i, prefix, len(cache), 'num_captured=0', \
                  '%d %d %d' % (-1, -1, -1)
        return (max_accuracy, best_prefix, captured_zero, dead_prefix, inferior)

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
        dead_prefix = 1
        if not quiet:
            print i, prefix, len(cache), 'ub<=max', \
                  '%1.3f %1.3f %1.3f' % (accuracy, upper_bound, max_accuracy)
        return (max_accuracy, best_prefix, captured_zero, dead_prefix, inferior)
    else:
        # if prefix is the new best known prefix, update max_accuracy
        # and best_prefix
        if (accuracy > max_accuracy):
            print 'max:', max_accuracy, '->', accuracy
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
                inferior = True
                if (accuracy > equiv_accuracy):
                    # equiv_prefix is inferior to prefix
                    cache.pop(equiv_prefix)
                    pdict[sorted_prefix] = (prefix, accuracy)
                else:
                    # prefix is inferior to the stored equiv_prefix
                    inferior = 1
                    return (max_accuracy, best_prefix, captured_zero, dead_prefix, inferior)
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
    return (max_accuracy, best_prefix, captured_zero, dead_prefix, inferior)

def given_prefix(full_prefix, cache, rules, ones, ndata, max_accuracy=0, best_prefix=None):
    """
    Compute accuracy of a given prefix via incremental computation.

    """
    for i in range(len(full_prefix)):
        prefix_start = full_prefix[:i]

        # cached_prefix is the cached data about a previously evaluated prefix
        cached_prefix = cache[prefix_start]

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

        prefix = prefix_start + (full_prefix[i],)

        (max_accuracy, best_prefix, cz, dp, ir) = \
            incremental(cache, prefix, rules, ones, ndata, num_already_captured,
                        num_already_correct, not_yet_captured, cached_prediction,
                        max_accuracy=max_accuracy, best_prefix=best_prefix)
        return

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

def compute_default(ones, uncaptured):
    """
    Computes default rule given an mpz representation of uncaptured samples.

    Given an mpz representation of the uncaptured samples and the number of
    samples, returns a default rule.

    """
    n1 = rule.count_ones(ones)
    n0 = uncaptured - n1
    if (n1 > n0):
        default_rule = 1
        num_default_correct = n1
    else:
        default_rule = 0
        num_default_correct = n0
    return (default_rule, num_default_correct)

## the greedy algorithm should be modified to work with mpz
def greedy_rule_list(ones, rules, max_length):
    """
    Grow the rule list greedily.

    This can provide a good warm start solution for another algorithm.

    """
    (nrules, ndata) = rules.shape
    prefix = ()
    predicted_labels = ()
    total_captured = []
    total_correct = []
    accuracy = 0.

    for i in range(max_length):
        captured = [r.nonzero()[0] for r in rules]
        num_captured = np.array([len(c) for c in captured])
        captured_labels = [ones[c] for c in captured]
        dist_from_half = np.array([c.mean() - 0.5 if (len(c) > 0) else 0.
                                   for c in captured_labels])
        prediction = np.cast[int](dist_from_half > 0)
        magnitude = np.abs(dist_from_half)
        x = tb.tabarray(columns=[np.arange(nrules), num_captured, prediction,
                                 magnitude],
                        names=['id', 'num_captured', 'prediction', 'magnitude'])
        x.sort(order=['magnitude', 'num_captured'])
        y = x[x['magnitude'] == x['magnitude'].max()][0]
        id = y['id']
        ind = (rules[id] == 0).nonzero()[0]
        (default_rule, num_default_correct) = compute_default(ones[ind])
        num_captured_correct = sum(total_captured) + y['num_captured']
        new_accuracy = float(num_captured_correct + num_default_correct) / ndata
        if (new_accuracy <= accuracy):
            print 'greedy algorithm stopping', new_accuracy, accuracy
            break
        accuracy = new_accuracy
        total_captured += [y['num_captured']]
        total_correct += [(ones[captured[id]] == y['prediction']).sum()]
        prefix += (id,)
        predicted_labels += (y['prediction'],)
        ones = ones[ind]
        rules = rules[:, ind]
        rules[id] = 0
        if (len(ones) == 0):
            break

    (default_rule, num_default_correct) = compute_default(ones, 639 - sum(total_captured))
    num_captured_correct = sum(total_correct)
    accuracy = float(num_captured_correct + num_default_correct) / ndata
    upper_bound = float(num_captured_correct + len(ones)) / ndata
    return (prefix, predicted_labels, default_rule, accuracy, upper_bound)

def initialize(din, dout, label_file, out_file, warm_start, max_accuracy,
               best_prefix, seed=None, sample=None, max_greedy_length=8):

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
    # rules = np.cast[int](np.array(rule_dict.values()))
    nrules = len(rule_names)
    rule.lead_one = mpz(pow(2, ndata))

    # rule_set is a set of all rule indices
    rule_set = set(range(nrules))

    # for the empty prefix, compute the default rule and number of data it
    # correctly predicts
    (empty_default, empty_num_correct) = compute_default(ones, ndata)
    empty_accuracy = float(empty_num_correct) / ndata

    # max_accuracy is the accuracy of the best_prefix observed so far
    # if not already defined, either use a greedy algorithm to compute a warm
    # start or start cold with an empty prefix
    if (max_accuracy is None):
        if warm_start:
            # compute warm start rule list using a greedy algorithm
            ## this is currently broken (hasn't been modified to work for mpz)
            (best_prefix, greedy_prediction, greedy_default, max_accuracy,
             greedy_upper_bound) = greedy_rule_list(ones, rules, max_length=max_greedy_length)
            print 'greedy solution:'
            print_rule_list(best_prefix, greedy_prediction, greedy_default, rule_names)
        else:
            best_prefix = ()
            max_accuracy = empty_accuracy

    # cache is a PrefixCache object, which is a dictionary that stores
    # prefix-related computations, where each key-value pair maps a prefix
    # tuples to a CacheEntry object
    cache = PrefixCache()

    # initialize the cache with a single entry for the empty rule list
    cache[()] = CacheEntry(prefix=(), prediction=(), default_rule=empty_default,
                           accuracy=empty_accuracy, upper_bound=1.,
                           num_captured=0, num_captured_correct=0,
                           not_captured=rule.make_all_ones(ndata + 1),
                           curiosity=0.)

    if warm_start:
        """
        cache[best_prefix] = CacheEntry(prefix=best_prefix,
                                        prediction=greedy_prediction,
                                        default_rule=greedy_default,
                                        accuracy=max_accuracy,
                                        upper_bound=greedy_upper_bound,
                                        num_captured=None,
                                        num_captured_correct=None,
                                        not_captured=None)
        """
        pass

    return (nrules, ndata, ones, rules, rule_set, rule_names, max_accuracy,
            best_prefix, cache)
