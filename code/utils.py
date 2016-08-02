import itertools

import numpy as np

def list_to_csv_record(x):
    return x.__repr__().split('array')[-1].strip('([])').replace('\n', '').replace(' ', '')

def expand_names(name, m):
    return ['%s_%d' % (name, i) for i in range(m)]

def format_float_list(x):
    return [float('%2.3f' % y) for y in x].__repr__()

class Metrics:
    def __init__(self, m):
        self.cache_size = np.zeros(m, int)
        self.inserts = np.zeros(m, int)
        self.dead_prefix_start = np.zeros(m, int)
        self.stunted_prefix = np.zeros(m, int)
        self.commutes = np.zeros(m, int)
        self.commutes_II = np.zeros(m, int)
        self.dominates = np.zeros(m, int)
        self.rejects = np.zeros(m, int)
        self.captured_zero = np.zeros(m, int)
        self.captured_all = np.zeros(m, int)
        self.captured_same = np.zeros(m, int)
        self.insufficient = np.zeros(m, int)
        self.dead_prefix = np.zeros(m, int)
        self.inferior = np.zeros(m, int)
        self.garbage_collect = np.zeros(m, int)
        self.prune_up = np.zeros(m, int)
        self.seconds = 0.
        self.priority_queue_length = 0
        self.pdict_length = 0
        self.min_objective = 0.
        self.accuracy = 0.
        self.priority = 0
        self.best_prefix = ()
        self.part_time = 0.

    def __repr__(self):
        return '\n'.join(('best prefix: %s' % self.best_prefix.__repr__(),
                    'min objective: %2.5f' % self.min_objective,
                    'accuracy: %2.5f' % self.accuracy,
                    'priority: %2.5f' % self.priority,
                    'priority queue length: %d' % self.priority_queue_length,
                    'pdict length: %d' % self.pdict_length,
                    'cache size: %s' % list(self.cache_size).__repr__(),
                    'inserts: %s' % list(self.inserts).__repr__(),
                    'dead prefix start: %s' % list(self.dead_prefix_start).__repr__(),
                    'stunted prefix: %s' % list(self.stunted_prefix).__repr__(),
                    'commutes: %s' % list(self.commutes).__repr__(),
                    'commutes II: %s' % list(self.commutes_II).__repr__(),
                    'dominates: %s' % list(self.dominates).__repr__(),
                    'rejects: %s' % list(self.rejects).__repr__(),
                    'caputed zero: %s' % list(self.captured_zero).__repr__(),
                    'captured all: %s' % list(self.captured_all).__repr__(),
                    'captured same: %s' % list(self.captured_same).__repr__(),
                    'insufficient: %s' % list(self.insufficient).__repr__(),
                    'dead prefix: %s' % list(self.dead_prefix).__repr__(),
                    'inferior: %s' % list(self.inferior).__repr__(),
                    'garbage collect: %s' % list(self.garbage_collect).__repr__(),
                    'prune up: %s' % list(self.prune_up).__repr__(),
                    'seconds: %2.5f' % self.seconds,
                    'growth: %s' % format_float_list(self.growth()),
                    'part time: %f' % self.part_time,
                    'total dead prefix: %d' % sum(list(self.dead_prefix)),
                    'dead prefix/part time: %f' % (float(self.dead_prefix.sum()) / float(self.part_time + 0.000001))))

    def growth(self):
        c = np.cast[float](self.cache_size)
        g = (c[1:] / c[:-1])
        g[np.isnan(g)] = 0.
        return g

    def check(self, i, nrules):
        """
        Should return True for breadth-first search after level i is complete.

        """
        return ((self.cache_size[i] + self.commutes[i] + self.captured_zero[i] +
                 self.insufficient[i] + self.dead_prefix[i] + self.inferior[i])
             == ((nrules - i + 1) * (self.cache_size[i - 1] -
                 self.dead_prefix_start[i - 1] - self.stunted_prefix[i - 1])))

    def aggregate(self):
        return [self.cache_size.sum(), self.inserts.sum(), self.dead_prefix_start.sum(),
                self.stunted_prefix.sum(), self.commutes.sum(),
                self.commutes_II.sum(), self.dominates.sum(), self.rejects.sum(),
                self.captured_zero.sum(), self.captured_all.sum(),
                self.captured_same.sum(), self.insufficient.sum(),
                self.dead_prefix.sum(), self.inferior.sum(), self.garbage_collect.sum(),
                self.prune_up.sum()]

    def print_summary(self):
        a = self.aggregate()
        print 'priority queue length:', self.priority_queue_length
        print 'cache size:', a[0]
        print 'inserts:', a[1]
        print 'dead prefix start:', a[2]
        print 'stunted prefix:', a[3]
        print 'commutes:', a[4]
        print 'commutes II:', a[5]
        print 'dominates:', a[6]
        print 'rejects:', a[7]
        print 'captured zero:', a[8]
        print 'captured all:', a[9]
        print 'captured same:', a[10]
        print 'insufficient:', a[11]
        print 'dead prefix:', a[12]
        print 'inferior:', a[13]
        print 'garbage collect:', a[14]
        print 'prune up:', a[15]
        return

    def best_prefix_repr(self):
        bp = self.best_prefix
        return bp.__repr__().strip('()').replace(' ', '').replace(',', ';')

    def to_string(self, granular=True):
        s1 = '%2.5f,%2.5f,%2.5f,%2.5f,%s,%d' % (self.seconds, self.min_objective,
                                          self.accuracy, self.priority,
                                          self.best_prefix_repr(),
                                          self.priority_queue_length)
        s2 = list_to_csv_record(self.aggregate())
        if granular:
            s3 = ','.join([list_to_csv_record(x) for x in [self.cache_size]])
                       #[self.cache_size, self.dead_prefix_start,
                       # self.stunted_prefix, self.commutes, self.commutes_II,
                       # self.dominates, self.rejects, self.captured_zero,
                       # self.captured_all, self.captured_same,
                       # self.insufficient, self.dead_prefix, self.inferior]])
            return ','.join([s1, s2, s3])
        else:
            return ','.join([s1, s2])

    def names_to_string(self, granular=True):
        names = ['cache_size', 'inserts', 'dead_prefix_start', 'stunted_prefix',
                 'commutes', 'commutes_II', 'dominates', 'rejects',
                 'captured_small', 'captured_all', 'captured_same',
                 'insufficient', 'dead_prefix', 'inferior', 'garbage_collect', 'prune_up']
        m = len(self.cache_size)
        e_names = [expand_names(x, m) for x in ['cache_size']]
        if granular:
            return ','.join(['seconds', 'min_objective', 'accuracy', 'priority',
                             'best_prefix', 'priority_queue_length'] + names +
                            list(itertools.chain(*e_names)))
        else:
            return ','.join(['seconds', 'min_objective', 'accuracy', 'priority',
                             'best_prefix', 'priority_queue_length'] + names)

def mpz_to_string(x):
    # skip leading 1
    return "{0}".format(x.digits(2))[1:]

def mpz_to_array(x):
    return np.cast['int']([i for i in mpz_to_string(x)])

def array_to_string(x):
    return ''.join(np.cast[str](x))

def rules_to_array(x):
    return np.array([mpz_to_array(r) for r in x])

def find_commuting_pairs(x):
    n = x.shape[0]
    num_pairs = (n * (n - 1)) / 2
    d = np.dot(x, x.T)
    num_commuting_pairs = (d == 0).sum() / 2
    print 'total pairs:', num_pairs, 'commuting pairs:', num_commuting_pairs
    mask = np.triu(np.ones(d.shape, int))
    mask = mask - np.identity(d.shape[0], int)
    commuting_pairs = np.array(((d == 0) & mask).nonzero()).T
    return commuting_pairs

def commuting_dict(commuting_pairs, n):
    d = dict(zip(range(n), [()] * n))
    for (a, b) in commuting_pairs:
        d[a] += (b,)
    return d

def dominates(x, not_captured, i):
    x = x[:, mpz_to_array(not_captured).nonzero()[0]]
    return ((x[i] - x) >= 0).all(axis=1).nonzero()[0]

def prefix_dominates(x, not_captured, prefix):
    return set(itertools.chain.from_iterable([set(dominates(x, not_captured, p)) for p in prefix]))

def relations_dict(x):
    n = len(x)
    r = dict(zip(range(n), [()] * n))
    for i in range(n):
        for j in range(n):
            if (i != j):
                if ((x[i] - x[j]) >= 0).all():
                    r[i] += (j,)
    return r

def all_relations(rdict, prefix):
    return set(itertools.chain.from_iterable([set(rdict[p]) for p in prefix]))

def make_graph(nodes, edges):
    import networkx as nx
    G = nx.Graph()
    for node in nodes:
        G.add_node(node)
    for edge in edges:
        (a, b) = edge
        G.add_edge(a, b)
    return G

def sublists(s, min_length=2):
    return set(itertools.chain.from_iterable(itertools.combinations(s, r) for r
                                             in range(min_length, len(s) + 1)))
