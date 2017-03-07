import os

import gmpy2
import numpy as np
import pylab
import tabular as tb


froot = 'compas'
data_dir = '../data/CrossValidation/'
num_folds = 1
lw = 2  # linewidth
ms = 9  # markersize
fs = 16 # fontsize

# log files generated on beepboop
log_dir = '../logs/keep/'
log_root_list = ['for-%s-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=1000000000-c=0.0050000-v=1-f=1000.txt']
fold = 1
ftag = 'compas_logs'

pylab.ion()

tname = 'compas_%d_train.out' % fold
log_fname = log_root_list[0] % tname
fname = os.path.join(data_dir, tname)

c = float(log_fname.split('c=')[1].split('-')[0])
nrules = len(open(fname, 'rU').read().strip().split('\n'))
print 'num rules:', nrules

log_fname = os.path.join(log_dir, log_fname)
x = tb.tabarray(SVfile=log_fname)

pylab.figure(1)


# total time = wall clock time
# evaluate_children_time = time in evaluate_children()
# node_select_time = time in queue_select()

time_names = ['total_time', 'evaluate_children_time', 'node_select_time', 'rule_evaluation_time', 'lower_bound_time', 'objective_time', 'tree_insertion_time', 'permutation_map_insertion_time']

(total, evaluate_children, node_select, rule_evaluation, lower_bound, objective,
 tree_insertion, permutation_map_insertion) =  x[-1:][time_names][0]

print
print 'fraction of time in evaluate_children(): %2.3f' % (evaluate_children / total)
print 'fraction of time in node_select(): %2.3f' % (node_select / total)
print 'fraction of time accounted for: %2.3f' % ((evaluate_children + node_select) / total)
print 'want to verify: remaining time spent in garbage_collect() ?'
print 'TODO: add timing measurement around garbage_collect'

print
print 'fraction of time doing "real work" in evaluate_children(): %2.3f' % (rule_evaluation / evaluate_children)
print 'fraction of "real work" time computing objective (does not include lower bound or support bound checks): %2.3f' % (objective / rule_evaluation)
print 'fraction of "real work" time in permutation_insert(): %2.3f' % (permutation_map_insertion / rule_evaluation)
print 'fraction of "real work" time in tree->insert(): %2.3f' % (tree_insertion / rule_evaluation)
print 'want to verify: remaining "real work" time spent computing lower bound + support bound checks + identical points bound (minority)?'
print 'TODO: modify logger.setLowerBoundTime(time_diff(t1)) to report cumulative time measurements'
print 'TODO: add timing measurement around identical points bound'

"""
fraction of time in evaluate_children(): 0.975
fraction of time in node_select(): 0.017
fraction of time accounted for: 0.993
want to verify: remaining time spent in garbage_collect() ?
TODO: add timing measurement around garbage_collect

fraction of time doing "real work" in evaluate_children(): 0.990
fraction of "real work" time computing objective (does not include lower bound or support bound checks): 0.426
fraction of "real work" time in permutation_insert(): 0.012
fraction of "real work" time in tree->insert(): 0.001
want to verify: remaining "real work" time spent computing lower bound + support bound checks + identical points bound (minority)?
TODO: modify logger.setLowerBoundTime(time_diff(t1)) to report cumulative time measurements
TODO: add timing measurement for identical points bound
"""
