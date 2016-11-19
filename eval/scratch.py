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
ms = 9  # markersize
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
pylab.plot(x['total_time'][1], default_objective, 'co', markersize=ms)
pylab.plot(x['total_time'][imin], x['tree_min_objective'][imin], 'ms', markersize=ms)
ax = list(pylab.axis())
ax[0] = -0.04
#ax[2] = -0.01
#ax[3] = 0.51
pylab.axis(ax)
#pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('objective', fontsize=fs)
pylab.title('current best objective during execution', fontsize=fs)
pylab.xticks(fontsize=(fs-2))
pylab.yticks(fontsize=(fs-2))
pylab.legend(['complete execution'])

pylab.subplot(2, 1, 2)
pylab.plot(x['total_time'][:(imin+1)], x['tree_min_objective'][:(imin+1)], 'b-', linewidth=lw)
pylab.plot(x['total_time'][1], default_objective, 'co', markersize=ms)
pylab.plot(x['total_time'][imin], x['tree_min_objective'][imin], 'ms', markersize=ms)
ax = list(pylab.axis())
ax[0] = -0.00005
ax[1] = 0.0165
#ax[2] = -0.01
#ax[3] = 0.51
pylab.axis(ax)
pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('objective', fontsize=fs)
#pylab.title('current best objective during execution', fontsize=fs)
pylab.xticks(fontsize=(fs-2))
pylab.yticks(fontsize=(fs-2))
pylab.legend(['optimization phase'])
pylab.savefig('../figs/ela-objective.png')
pylab.draw()

pylab.figure(2)
pylab.clf()
pylab.subplot2grid((10, 1), (0, 0), rowspan=6)
pylab.plot(x['total_time'], x['tree_num_nodes'], 'k-', linewidth=lw)
pylab.plot(x['total_time'], x['queue_size'], ':', color='gray', linewidth=lw)
pylab.plot(x['total_time'], prefix_sums, 'b-', linewidth=lw)
#pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('size', fontsize=fs)
pylab.title('data structure size', fontsize=fs)
pylab.xticks(fontsize=(fs-2))
pylab.yticks(fontsize=(fs-2))
ax = list(pylab.axis())
ax[3] = 7100
pylab.axis(ax)
pylab.legend(['cache', 'physical queue', 'logical queue'], fontsize=(fs-1))

pylab.subplot2grid((10, 1), (7, 0), rowspan=3)
pylab.plot(x['total_time'], x['tree_insertion_num'], 'b-', linewidth=lw)
pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('count', fontsize=fs)
pylab.title('cumulative number of cache (= queue) insertions', fontsize=fs)
pylab.xticks(fontsize=(fs-2))
pylab.yticks(fontsize=(fs-2))
pylab.draw()
pylab.savefig('../figs/ela-queue-cache-size-insertions.png')

total_space_size = space.state_space_size(nrules=nrules, min_objective=default_objective, c=c)
remaining_space_size = [space.remaining_search_space(nrules=nrules, min_objective=current_objective, c=c, prefix_lengths=parse_prefix_lengths(pl)) for (current_objective, pl) in x[['tree_min_objective', 'prefix_lengths']]]
remaining_space_size[0] = total_space_size
log10_total = float(gmpy2.log10(total_space_size))
log10_remaining = [float(gmpy2.log10(r)) if r else 1 for r in remaining_space_size]

# need to handle entries where remaining state space = 0

pylab.figure(3)
pylab.clf()
pylab.subplot(3, 1, 1)
pylab.plot(x['total_time'], log10_remaining, 'b-', linewidth=lw)
#pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('log10(size)', fontsize=fs)
pylab.title('log10(size of remaining search space)', fontsize=fs)
pylab.xticks(fontsize=(fs-2))
pylab.yticks(fontsize=(fs-2))
pylab.legend(['complete execution'])

pylab.subplot(3, 1, 2)
pylab.plot(x['total_time'][:(imin+1)], log10_remaining[:(imin+1)], 'b-', linewidth=lw)
pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('log10(size)', fontsize=fs)
pylab.xticks(fontsize=(fs-2))
pylab.yticks(fontsize=(fs-2))
pylab.legend(['optimization phase'])

pylab.subplot(3, 1, 3)
pylab.plot(x['total_time'][imin:], log10_remaining[imin:], 'b-', linewidth=lw)
pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('log10(size)', fontsize=fs)
pylab.xticks(fontsize=(fs-2))
pylab.yticks(fontsize=(fs-2))
pylab.legend(['verification phase'], loc='lower left')
pylab.savefig('../figs/ela-remaining-space.png')
pylab.draw()

evaluate_time = x['evaluate_children_time'] - x['tree_insertion_time'] - x['permutation_map_insertion_time']

y = np.array([evaluate_time, x['permutation_map_insertion_time'], x['tree_insertion_time'], x['node_select_time']][::-1]).cumsum(axis=0)[::-1]

pylab.figure(4)
pylab.clf()
pylab.plot(x['total_time'], x['tree_insertion_num'], 'b-', linewidth=lw)
pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('count', fontsize=fs)
pylab.title('cumulative number of cache (= queue) insertions', fontsize=fs)
pylab.xticks(fontsize=(fs-2))
pylab.yticks(fontsize=(fs-2))
pylab.savefig('../figs/ela-cumulative-insertions.png')
pylab.draw()

pylab.figure(5)
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
pylab.draw()

print 'total time:', x['total_time'][-1]
print 'prefix + rule list evaluation time:', y[0][-1]
print 'permutation operations time:', y[1][-1]
print 'cache insertion time:', y[2][-1]
print 'node selection time:', y[3][-1]
