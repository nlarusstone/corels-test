import itertools

import numpy as np

def list_to_csv_record(x):
    return x.__repr__().strip('[]').replace(' ', '')

def expand_names(name, m):
    return ['%s_%d' % (name, i) for i in range(m)]

def format_float_list(x):
    return [float('%2.3f' % y) for y in x].__repr__()

class Metrics:
    def __init__(self, m):
        self.cache_size = [0] * m
        self.dead_prefix_start = [0] * m
        self.captured_zero = [0] * m
        self.stunted_prefix = [0] * m
        self.commutes = [0] * m
        self.dead_prefix = [0] * m
        self.inferior = [0] * m
        self.seconds = 0.
        self.priority_queue_length = 0

    def __repr__(self):
        return '\n'.join(('cache size: %s' % self.cache_size.__repr__(),
                    'dead prefix start: %s' % self.dead_prefix_start.__repr__(),
                    'caputed zero: %s' % self.captured_zero.__repr__(),
                    'stunted prefix: %s' % self.stunted_prefix.__repr__(),
                    'commutes: %s' % self.commutes.__repr__(),
                    'dead prefix: %s' % self.dead_prefix.__repr__(),
                    'inferior: %s' % self.inferior.__repr__(),
                    'seconds: %2.3f' % self.seconds,
                    'growth: %s' % format_float_list(self.growth())))

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
                 self.dead_prefix[i] + self.inferior[i])
             == ((nrules - (i - 1)) * (self.cache_size[i - 1] -
                 self.dead_prefix_start[i - 1] - self.stunted_prefix[i - 1])))

    def aggregate(self):
        return [sum(self.cache_size), sum(self.dead_prefix_start),
                sum(self.captured_zero), sum(self.stunted_prefix),
                sum(self.commutes), sum(self.dead_prefix), sum(self.inferior)]

    def to_string(self):
        s1 = '%2.3f,%d' % (self.seconds, self.priority_queue_length)
        s2 = list_to_csv_record(self.aggregate())
        s3 = ','.join([list_to_csv_record(x) for x in
                       [self.cache_size, self.dead_prefix_start,
                        self.captured_zero, self.stunted_prefix, self.commutes,
                        self.dead_prefix, self.inferior]])
        return ','.join([s1, s2, s3])

    def names_to_string(self):
        names = ['cache_size', 'dead_prefix_start', 'captured_zero',
                 'stunted_prefix', 'commutes', 'dead_prefix', 'inferior']
        m = len(self.cache_size)
        e_names = [expand_names(x, m) for x in names]
        return ','.join(['seconds', 'priority_queue_length'] + names +
                        list(itertools.chain(*e_names)))

def mpz_to_string(x):
    # skip leading 1
    return "{0}".format(x.digits(2))[1:]

def mpz_to_array(x):
    return np.cast['uint8']([i for i in mpz_to_string(x)])

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
