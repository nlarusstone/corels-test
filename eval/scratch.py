"""
Something Elaine could generate quickly

Not necessarily meant for future use

"""
import os

import gmpy2
import numpy as np
import pylab
import tabular as tb

import space


def parse_prefix_lengths(p):
    ij = [q.split(':') for q in p.split(';') if q]
    return np.array([(int(i), int(j)) for (i, j) in ij])

def parse_prefix_sums(p):
    return np.sum([int(q.split(':')[1]) for q in p.split(';') if q])

# Command run:  ./bbcache -c -p 1 ../data/tdata_R.out ../data/tdata_R.label

log_dir = '../logs/'
log_fname = 'for-tdata_R.out-curiosity-with_prefix_perm_map-max_num_nodes=100000-c=0.0010000-v=1.txt'

lw = 2  # linewidth
ms = 7  # markersize
fs = 16 # fontsize

c = float(log_fname.split('c=')[1].split('-')[0])
nrules = 377    # should have a way to get this automatically

log_fname = os.path.join(log_dir, log_fname)
x = tb.tabarray(SVfile=log_fname)
x = x[:-1]  # ignore last log record because it measures the time to delete the queue

default_objective = x['tree_min_objective'][1]
imin = np.nonzero(x['tree_min_objective'] == x['tree_min_objective'][-1])[0][0]
tmin = x['total_time'][imin]

prefix_sums = np.array([parse_prefix_sums(p) for p in x['prefix_lengths']])

print "num records:", len(x)
print "time to achieve optimum:", tmin
print "time to verify optimum:", x['total_time'][-1]

pylab.ion()
pylab.figure(1)
pylab.clf()
pylab.subplot(2, 1, 1)
pylab.plot(x['total_time'], x['tree_min_objective'], 'b-', linewidth=lw)
pylab.plot(x['total_time'][1], default_objective, 'ro', markersize=ms)
pylab.plot(x['total_time'][imin], x['tree_min_objective'][imin], 'y*', markersize=(ms*2))
ax = list(pylab.axis())
ax[0] = -0.05
ax[3] = 0.51
pylab.axis(ax)
#pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('objective', fontsize=fs)
pylab.title('current best objective during execution', fontsize=fs)
pylab.xticks(fontsize=(fs-2))
pylab.yticks(fontsize=(fs-2))

pylab.subplot(2, 1, 2)
pylab.plot(x['total_time'][:(imin+1)], x['tree_min_objective'][:(imin+1)], 'b-', linewidth=lw)
pylab.plot(x['total_time'][1], default_objective, 'ro', markersize=ms)
pylab.plot(x['total_time'][imin], x['tree_min_objective'][imin], 'y*', markersize=(ms*2))
ax = list(pylab.axis())
ax[0] = -0.0001
ax[3] = 0.51
pylab.axis(ax)
pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('objective', fontsize=fs)
#pylab.title('current best objective during execution', fontsize=fs)
pylab.xticks(fontsize=(fs-2))
pylab.yticks(fontsize=(fs-2))
pylab.savefig('../figs/ela-objective.png')

pylab.figure(2)
pylab.clf()
pylab.plot(x['total_time'], x['tree_num_nodes'], 'k-', linewidth=lw)
pylab.plot(x['total_time'], x['queue_size'], ':', color='gray', linewidth=lw)
pylab.plot(x['total_time'], prefix_sums, 'b-', linewidth=lw)
pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('data structure size', fontsize=fs)
pylab.xticks(fontsize=(fs-2))
pylab.yticks(fontsize=(fs-2))
pylab.legend(['cache', 'physical queue', 'logical queue'], loc='upper left')
pylab.savefig('../figs/ela-data-structures.png')

total_space_size = space.state_space_size(nrules=nrules, min_objective=default_objective, c=c)
remaining_space_size = [space.remaining_search_space(nrules=nrules, min_objective=current_objective, c=c, prefix_lengths=parse_prefix_lengths(pl)) for (current_objective, pl) in x[['tree_min_objective', 'prefix_lengths']]]
log10_total = float(gmpy2.log10(total_space_size))
log10_remaining = [float(gmpy2.log10(r)) for r in remaining_space_size]

# need to handle entries where remaining state space = 0

pylab.figure(3)
pylab.clf()
pylab.subplot(2, 1, 1)
pylab.plot(x['total_time'][1:-4], log10_remaining[1:-4], 'b-', linewidth=lw)
#pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('log10(remaining', fontsize=fs)
pylab.title('log10(size of remaining search space)', fontsize=fs)
pylab.xticks(fontsize=(fs-2))
pylab.yticks(fontsize=(fs-2))

pylab.subplot(2, 1, 2)
pylab.plot(x['total_time'][1:(imin+1)], log10_remaining[1:(imin+1)], 'b-', linewidth=lw)
pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('log10(remaining', fontsize=fs)
pylab.xticks(fontsize=(fs-2))
pylab.yticks(fontsize=(fs-2))
pylab.savefig('../figs/ela-remaining-space.png')

evaluate_time = x['evaluate_children_time'] - x['tree_insertion_time'] - x['permutation_map_insertion_time']

y = np.array([evaluate_time, x['permutation_map_insertion_time'], x['tree_insertion_time'], x['node_select_time']][::-1]).cumsum(axis=0)[::-1]

pylab.figure(4)
pylab.clf()
pylab.plot(x['total_time'], x['total_time'], 'm--', linewidth=lw)
#pylab.plot(x['total_time'], x['node_select_time'] + x['evaluate_children_time'], 'r--', linewidth=lw)
#pylab.plot(x['total_time'], x['node_select_time'], 'b-', linewidth=lw)
pylab.plot(x['total_time'], y[0], 'k:', linewidth=lw) # prefix + rule list evaluation
pylab.plot(x['total_time'], y[1], 'b-', linewidth=lw) # permutation map
pylab.plot(x['total_time'], y[2], 'c--', linewidth=lw) # cache insertion
pylab.plot(x['total_time'], y[3], ':', color='gray', linewidth=lw) # node selection
pylab.legend(['total', 'prefix + rule list evaluation', 'permutation map', 'cache insertion', 'node selection'], loc='upper left')
pylab.savefig('../figs/ela-time.png')

print 'total time:', x['total_time'][-1]
print 'prefix + rule list evaluation time:', y[0][-1]
print 'permutation operations time:', y[1][-1]
print 'cache insertion time:', y[2][-1]
print 'node selection time:', y[3][-1]
