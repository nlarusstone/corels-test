import os

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

from branch_bound import initialize
import utils


din = os.path.join('..', 'data')
dout = os.path.join('..', 'cache')
warm_start = False
best_prefix = None
delimiter = '\t'
quiet = True
garbage_collect = False
froot = 'adult_R'
max_accuracy = 0
seed = None
sample = None

label_file = '%s.label' % froot
out_file = '%s.out' % froot

(nrules, ndata, ones, rules, rule_set, rule_names, max_accuracy, best_prefix, cache) = \
    initialize(din, dout, label_file, out_file, warm_start, max_accuracy, best_prefix, seed, sample)

x = utils.rules_to_array(rules)
commuting_pairs = utils.find_commuting_pairs(x)
G = utils.make_graph(range(nrules), commuting_pairs)
cliques = list(nx.find_cliques(G))
for i in range(len(cliques)):
    cliques[i].sort()
    cliques[i] = tuple(cliques[i])
assert len(cliques) == len(set(cliques))

clique_lengths = [len(c) for c in cliques]
scl = set(clique_lengths)
plt.ion()
plt.figure(1)
plt.clf()
(count, length, patch) = plt.hist(clique_lengths, range(min(scl), max(scl) + 1))
print zip(length, np.cast[int](count))