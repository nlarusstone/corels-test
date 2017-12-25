"""
./bbcache -c 2 -n 1000000000 -p 1 -r 0.005 ../data/CrossValidation/compas_1_train.out ../data/CrossValidation/compas_1_train.label ../data/CrossValidation/compas_1_train.minor

"""
import os

import gmpy2
import numpy as np
import pylab
import tabular as tb

import utils


froot = 'compas'
data_dir = '../data/CrossValidation/'
num_folds = 1
lw = 2  # linewidth
ms = 9  # markersize
fs = 16 # fontsize

# log files generated on beepboop for KDD ablation experiments
#log_dir = '../logs/keep/'
log_dir = '../logs/'
log_root_list = ['for-%s-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=100000000-c=0.0050000-v=1-f=1000.txt']
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
print 'fraction of "real work" time accounted for: %2.3f' % ((objective + permutation_map_insertion + tree_insertion) / rule_evaluation)
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
fraction of "real work" time accounted for: 0.439
want to verify: remaining "real work" time spent computing lower bound + support bound checks + identical points bound (minority)?
TODO: modify logger.setLowerBoundTime(time_diff(t1)) to report cumulative time measurements
TODO: add timing measurement for identical points bound
"""

pylab.figure(1, figsize=(6, 5.5))
pylab.clf()

total_time = x['total_time']
evaluate_children_time = x['evaluate_children_time']
node_select_time = x['node_select_time']
rule_evaluation_time = x['rule_evaluation_time']
objective_time = x['objective_time']
permutation_map_insertion_time = x['permutation_map_insertion_time']
tree_insertion_time = x['tree_insertion_time']

pylab.plot(total_time, total_time, '-', color='k', linewidth=lw)
pylab.plot(total_time, evaluate_children_time, '--', color='k', linewidth=lw)
pylab.plot(total_time, objective_time + permutation_map_insertion_time + tree_insertion_time, '-', color='gray', linewidth=lw)
pylab.plot(total_time, objective_time, '--', color='gray', linewidth=lw)
pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('time (s)', fontsize=fs)
pylab.axis([0, 150, 0, 150])
pylab.legend(['total wall clock time', 'time in evaluate_children(.)', 'obj + (pmap + cache insertion)', 'objective after lower bound'], fontsize=fs-4, loc='upper left')
pylab.xticks(fontsize=fs)
pylab.yticks(fontsize=fs)
pylab.savefig('../figs/%s-timing.pdf' % ftag)

pylab.figure(2, figsize=(12.5, 5))
pylab.clf()

lower_bound_num = x['lower_bound_num']
objective_num = x['objective_num']
tree_insertion_num = x['tree_insertion_num']
permutation_map_insertion_num = x['permutation_map_insertion_num']
evaluate_children_num = x['evaluate_children_num']
tree_num_evaluated = x['tree_num_evaluated']

tree_num_nodes = x['tree_num_nodes']
physical_queue = x['queue_size']
logical_queue = np.array([utils.parse_prefix_sums(p) for p in x['prefix_lengths']])
pmap_size = x['pmap_size']
pmap_null_num = x['pmap_null_num']
pmap_discard_num = x['pmap_discard_num']

pylab.subplot2grid((20, 20), (0, 0), colspan=9, rowspan=19)
#pylab.subplot(1, 2, 1)
pylab.semilogy(total_time, lower_bound_num, '-', color='b', linewidth=lw+2)
#pylab.semilogy(total_time, objective_num, '--', color='b', linewidth=lw+2)
pylab.semilogy(total_time, permutation_map_insertion_num, '-', color='gray', linewidth=lw+2)
pylab.semilogy(total_time, tree_insertion_num, '--', color='r', linewidth=lw+2)
pylab.semilogy(total_time, pmap_size, '-', color='gray', linewidth=lw)
pylab.semilogy(total_time, pmap_null_num, '--', color='gray', linewidth=lw+2)
pylab.semilogy(total_time, evaluate_children_num, '-', color='b', linewidth=lw)
pylab.semilogy(total_time, tree_num_evaluated, '--', color='b', linewidth=lw)
#pylab.semilogy(total_time, pmap_discard_num, '--', color='gray', linewidth=lw+2)
pylab.xlabel('Time (s)', fontsize=fs)
pylab.ylabel('Count', fontsize=fs)
pylab.axis([0, 150, 0, 10**8])
pylab.legend(['Lower bound evaluations', 'Permutation map lookups', 'Cache insertions',
              'Permutation map size', 'Permutation map new insertions', 'Prefixes we try to extend',
              'Prefixes that insert children'], fontsize=fs-2, loc='lower right')
pylab.xticks(fontsize=fs-1)
pylab.yticks(fontsize=fs-1)

pylab.subplot2grid((20, 20), (0, 10), colspan=9, rowspan=19)
#pylab.subplot(1, 2, 2)
pylab.semilogy(total_time, tree_num_nodes, '-', color='r', linewidth=lw+4)
pylab.semilogy(total_time, physical_queue, '--', color='k', linewidth=lw)
pylab.semilogy(total_time, logical_queue, '-', color='k', linewidth=lw)
pylab.xlabel('Time (s)', fontsize=fs)
#pylab.ylabel('Count', fontsize=fs)
pylab.axis([0, 150, 0, 10**8])
pylab.legend(['Cache size', 'Physical queue size', 'Logical queue size'], fontsize=fs-2, loc='lower left')
pylab.xticks(fontsize=fs-1)
pylab.yticks(fontsize=fs-1)

pylab.suptitle('Operations performed and data structure sizes', fontsize=fs)
pylab.savefig('../figs/%s-operations-semilogy.pdf' % ftag)

pylab.figure(3, figsize=(12.5, 5))
pylab.clf()

pylab.subplot2grid((20, 20), (0, 0), colspan=9, rowspan=19)
#pylab.subplot(1, 2, 1)
scale = 10.**6
#pylab.plot(total_time, lower_bound_num, linewidth=lw)
pylab.plot(total_time, permutation_map_insertion_num / scale, '-', color='gray', linewidth=lw+2)
pylab.plot(total_time, tree_insertion_num / scale, '--', color='r', linewidth=lw+2)
pylab.plot(total_time, pmap_size / scale, '-', color='gray', linewidth=lw)
pylab.plot(total_time, pmap_null_num / scale, '--', color='gray', linewidth=lw+2)
pylab.plot(total_time, evaluate_children_num / scale, '-', color='b', linewidth=lw)
pylab.plot(total_time, tree_num_evaluated / scale, '--', color='b', linewidth=lw)
#pylab.plot(total_time, pmap_discard_num)
pylab.xlabel('Time (s)', fontsize=fs)
pylab.ylabel('Count (millions)', fontsize=fs)
pylab.axis([0, 150, 0, 2])
pylab.legend(['Permutation map lookups', 'Cache insertions', 'Permutation map size',
              'Permutation map new insertions', 'Prefixes we try to extend',
              'Prefixes that insert children'], fontsize=fs-2.5, loc=(0.12, 0.47))
#pylab.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
pylab.xticks(fontsize=fs)
pylab.yticks(np.arange(0, 2.1, 0.4), fontsize=fs)

pylab.subplot2grid((20, 20), (0, 10), colspan=9, rowspan=19)
#pylab.subplot(1, 2, 2)
pylab.plot(total_time, tree_num_nodes / scale, '-', color='r', linewidth=lw+4)
pylab.plot(total_time, physical_queue / scale, '--', color='k', linewidth=lw)
pylab.plot(total_time, logical_queue / scale, '-', color='k', linewidth=lw)
pylab.xlabel('Time (s)', fontsize=fs)
#pylab.ylabel('Count (millions)', fontsize=fs)
pylab.axis([0, 150, 0, 2])
pylab.legend(['Cache size', 'Physical queue size', 'Logical queue size'], fontsize=fs-2.5, loc='upper right')
#pylab.ticklabel_format(style='sci', axis='y', scilimits=(0,0))
pylab.xticks(fontsize=fs)
pylab.yticks(np.arange(0, 2.1, 0.4), fontsize=fs)

pylab.suptitle('Operations performed and data structure sizes', fontsize=fs)
pylab.savefig('../figs/%s-operations-plot.pdf' % ftag)

pylab.figure(4, figsize=(12.5, 5))
pylab.clf()

pylab.subplot2grid((20, 20), (0, 0), colspan=9, rowspan=19)
#pylab.subplot(1, 2, 1)
scale = 10.**6
pylab.loglog(total_time, lower_bound_num, 'b', linewidth=lw+2)
#pylab.loglog(total_time, objective_num, '--', color='b', linewidth=lw+2)
pylab.loglog(total_time, permutation_map_insertion_num, '-', color='gray', linewidth=lw+2)
pylab.loglog(total_time, tree_insertion_num, '--', color='r', linewidth=lw+2)
pylab.loglog(total_time, pmap_size, '-', color='gray', linewidth=lw)
pylab.loglog(total_time, pmap_null_num, '--', color='gray', linewidth=lw+2)
pylab.loglog(total_time, evaluate_children_num, '-', color='b', linewidth=lw)
pylab.loglog(total_time, tree_num_evaluated, '--', color='b', linewidth=lw)
pylab.loglog(total_time, pmap_discard_num, '--', color='gray', linewidth=lw)
pylab.xlabel('Time (s)', fontsize=fs)
pylab.ylabel('Count', fontsize=fs)
pylab.axis([10**-4.5, 150, 0, 10**8])
pylab.legend(['Lower bound evaluations', 'Permutation map lookups', 'Cache insertions',
              'Permutation map size', 'Pmap new insertions', 'Prefixes we try to extend',
              'Prefixes that insert children', 'Discards triggered by pmap'],
              fontsize=fs-4.5, loc='upper left', labelspacing=0.2)
pylab.xticks(fontsize=fs)
pylab.yticks(fontsize=fs)

pylab.subplot2grid((20, 20), (0, 10), colspan=9, rowspan=19)
#pylab.subplot(1, 2, 2)
pylab.loglog(total_time, tree_num_nodes, '-', color='r', linewidth=lw+4)
pylab.loglog(total_time, physical_queue, '--', color='k', linewidth=lw)
pylab.loglog(total_time, logical_queue, '-', color='k', linewidth=lw)
pylab.xlabel('Time (s)', fontsize=fs)
#pylab.ylabel('Count', fontsize=fs)
pylab.axis([10**-4.5, 150, 0, 10**8])
pylab.legend(['Cache size', 'Physical queue size', 'Logical queue size'], fontsize=fs-4.5, loc='upper left')
pylab.xticks(fontsize=fs-2)
pylab.yticks(fontsize=fs-2)

pylab.suptitle('Operations performed and data structure sizes', fontsize=fs)
pylab.savefig('../figs/%s-operations-loglog.pdf' % ftag)

pylab.figure(5, figsize=(6, 3.5))
pylab.clf()
pylab.subplot2grid((10, 10), (0, 0), colspan=10, rowspan=9)

ii = evaluate_children_num.nonzero()[0][0]
s = np.cast[float](evaluate_children_num[ii:]) * 155
tt =  total_time[ii:]
pylab.plot(tt, 1. - tree_insertion_num[ii:] / s, 'r--', linewidth=lw+1)
pylab.plot(tt, 1. - permutation_map_insertion_num[ii:] / s, '-', color='gray', linewidth=lw+1)
pylab.plot(tt, 1. - objective_num[ii:] / s, 'b--', linewidth=lw+1)
pylab.plot(tt, 1. - lower_bound_num[ii:] / s, 'b', linewidth=lw+1)
pylab.axis([0, 150, 0, 1.])
pylab.title('Cumulative eliminated children', fontsize=fs)
pylab.legend(['Permutation bound', 'Equivalent points bound', 'Lower + lookahead bounds', 'Support bounds'],
             loc='center right', fontsize=fs-1)
pylab.xticks(fontsize=fs)
pylab.yticks(fontsize=fs)
pylab.xlabel('Time (s)', fontsize=fs)
pylab.ylabel('Normalized fraction', fontsize=fs)
pylab.savefig('../figs/%s-eliminated.pdf' % ftag)

pylab.figure(6, figsize=(6, 3.5))
pylab.clf()
pylab.subplot2grid((10, 10), (0, 0), colspan=10, rowspan=9)

pylab.plot(tt,  lower_bound_num[ii:] / s, 'b', linewidth=lw+1)
pylab.plot(tt,  objective_num[ii:] / s, 'b--', linewidth=lw+1)
pylab.plot(tt,  permutation_map_insertion_num[ii:] / s, '-', color='gray', linewidth=lw+1)
pylab.plot(tt,  tree_insertion_num[ii:] / s, 'r--', linewidth=lw+1)
pylab.axis([0, 150, 0, 1.])
pylab.title('Normalized operations', fontsize=fs)
#pylab.title('Counts normalized by\n(# rules) x (# prefixes we try to extend)')
pylab.legend(['Lower bound evaluations', 'Objective evaluations', 'Permutation map lookups', 'Cache insertions',],
             loc='center right', fontsize=fs-1)
pylab.xticks(fontsize=fs)
pylab.yticks(fontsize=fs)
pylab.xlabel('Time (s)', fontsize=fs)
pylab.ylabel('Normalized fraction', fontsize=fs)
pylab.savefig('../figs/%s-normalized.pdf' % ftag)
