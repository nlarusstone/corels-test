import os

#import numpy as np
import gmpy2
from gmpy2 import mpz
import tabular as tb
import rule


class PrefixCache(dict):
    def to_file(self, fname, delimiter='\t'):
        header = ['prefix', 'length', 'first', 'prediction', 'default',
                  'accuracy', 'upper_bound', 'num_captured',
                  'num_captured_correct', 'num_not_captured']
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
                 num_captured_correct=None, not_captured=None):
        self.prefix = prefix
        self.prediction = prediction
        self.default_rule = default_rule
        self.accuracy = accuracy
        self.upper_bound = upper_bound
        self.num_captured = num_captured
        self.num_captured_correct = num_captured_correct
        self.not_captured = not_captured

    def __repr__(self):
        s = '\n'.join(('prefix: %s' % self.prefix.__repr__(),
                       'prediction: %s' % self.prediction.__repr__(),
                       'accuracy: %1.3f' % self.accuracy,
                       'upper_bound: %1.3f' % self.upper_bound,
                       'num_captured: %d' % self.num_captured,
                       'num_captured_correct: %d' % self.num_captured_correct,
                       'sum(not_captured): %d' % rule.count_ones(self.not_captured)))
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
               ('num_not_captured', self.num_not_captured()))
        return kvp

    def to_record(self):
        return (self.prefix.__repr__().strip('()'), len(self.prefix),
                self.first_rule(), self.prediction.__repr__().strip('()'),
                self.default_rule, self.accuracy, self.upper_bound,
                self.num_captured, self.num_captured_correct,
                self.num_not_captured())

    def to_string(self):
        rec = (self.prefix.__repr__().strip('()'), str(len(self.prefix)),
               str(self.first_rule()), self.prediction.__repr__().strip('()'),
               str(self.default_rule), str(self.accuracy),
               str(self.upper_bound), str(self.num_captured),
               str(self.num_captured_correct), str(self.num_not_captured()))
        return '\t'.join(rec)

def print_rule_list(prefix, prediction, default_rule, rule_names):
    e = ''
    for (i, label) in zip(prefix, prediction):
        print '%sif %s then predict %d' % (e, rule_names[i], label)
        e = 'else '
    print 'else predict %d' % default_rule

def file_to_dict(fname):
    """
    Utility that constructs a dictionary from a file.

    Map each line in the file to a (key, value) pair where the key is a string
    equal to the first word in the file and the value is an integer numpy.array
    constructed from the remaining words, which are each assumed to be 0 or 1.

    Used to read in the input files, label_file and out_file.

    """
    line_vec = [line.split() for line in
                open(fname, 'rU').read().strip().split('\n')]
    d = {}
    for line in line_vec:
        truthtable = "".join(line[1:])
        # to prevent clearing of leading zeroes
        truthtable = '1' + truthtable
        bitstring = mpz(truthtable, 2)
        d[line[0]] = bitstring
    return d

def compute_default(ones, uncaptured):
    """
    Computes default rule given an mpz representation of uncaptured samples

    Given an mpz representation of the uncaptured sampels and the number of 
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
        total_captured += [y['num_captured']]
        total_correct += [(ones[captured[id]] == y['prediction']).sum()]
        prefix += (id,)
        predicted_labels += (y['prediction'],)
        ind = (rules[id] == 0).nonzero()[0]
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
               best_prefix):

    if not os.path.exists(dout):
        os.mkdir(dout)

    # label_dict maps each label to a binary integer vector of length ndata
    label_dict = file_to_dict(os.path.join(din, label_file))
    digits = label_dict['{label=1}'].num_digits(2) - 1
    assert(rule.count_ones(label_dict['{label=1}']) == (digits - rule.count_ones(label_dict['{label=0}'])))

    # rule_dict maps each rule to a binary integer vector of length ndata
    rule_dict = file_to_dict(os.path.join(din, out_file))

    # ones a binary integer vector of length ndata
    # ones[j] = 1 iff label(data[j]) = 1
    ones = label_dict['{label=1}']

    # rules is an (nrules x ndata) binary integer matrix indicating
    # rules[i, j] = 1 iff data[j] obeys the ith rule
    #rules = np.cast[int](np.array(rule_dict.values()))
    nrules = len(rule_dict)
    ndata = digits
    rule.lead_one = mpz(pow(2, ndata))

    # rule_set is a set of all rule indices
    rule_set = set(range(nrules))

    # rule_names is an list of string descriptions of rules
    rule_names = list(rule_dict.keys())

    # for the empty prefix, compute the default rule and number of data it
    # correctly predicts
    (empty_default, empty_num_correct) = compute_default(ones, 639)
    empty_accuracy = float(empty_num_correct) / ndata

    # max_accuracy is the accuracy of the best_prefix observed so far
    # if not already defined, either use a greedy algorithm to compute a warm
    # start or start cold with an empty prefix
    if (max_accuracy is None):
        if warm_start:
            # compute warm start rule list using a greedy algorithm
            (best_prefix, greedy_prediction, greedy_default, max_accuracy,
             greedy_upper_bound) = greedy_rule_list(ones, rules, max_length=8)
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
                           not_captured=rule.make_all_ones(ndata + 1))

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

    return (nrules, ndata, ones, list(rule_dict.values()), rule_set, rule_names, max_accuracy,
            best_prefix, cache)
