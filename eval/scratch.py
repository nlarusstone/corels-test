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

# Command run:  ./bbcache -c -p 1 -r 0.001 -f 100 ../data/tdata_R.out ../data/tdata_R.label
# Yields log file with 739 records

log_dir = '../logs/'
log_fname = 'for-tdata_R.out-curiosity-with_prefix_perm_map-max_num_nodes=100000-c=0.0010000-v=1-f=100.txt'

lw = 2  # linewidth
ms = 9  # markersize
fs = 16 # fontsize

c = float(log_fname.split('c=')[1].split('-')[0])
nrules = 377    # should have a way to get this automatically, e.g., via `wc -l ../data/tdata_R.out`

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

max_length = max(set([int(lc.split(':')[0]) for lc in ''.join(x['prefix_lengths']).split(';') if lc]))
split_hist = [[lc.split(':') for lc in lh.strip(';').split(';')] for lh in x['prefix_lengths']]
kvp = [[(lc[0], int(lc[1])) for lc in lh if (len(lc) == 2)] for lh in split_hist]
z = tb.tabarray(kvpairs=kvp)
assert ([int(name) for name in z.dtype.names] == range(max_length + 1))
zc = z.extract()[:, ::-1].cumsum(axis=1)[:, ::-1]
color_vec = ['r', 'orange', 'y', 'g', 'c', 'b', 'purple', 'violet', 'm', 'gray', 'k']

pylab.figure(6)
pylab.clf()
for length in range(max_length + 1):
    pylab.plot(x['total_time'], zc[:, length], color=color_vec[length])
pylab.legend([str(length) for length in range(max_length + 1)])
pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('count', fontsize=fs)
pylab.title('logical queue size broken down by prefix length')
pylab.xticks(fontsize=(fs-2))
pylab.yticks(fontsize=(fs-2))
pylab.draw()
pylab.savefig('../figs/ela-queue.png')

pylab.figure(7)
pylab.clf()
pylab.subplot(2, 1, 1)
pylab.plot(x['total_time'], x['tree_prefix_length'], 'b-', linewidth=lw)
#pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('length', fontsize=fs)
pylab.title('length of rule list with current best objective', fontsize=fs)
pylab.xticks(fontsize=(fs-2))
pylab.yticks(fontsize=(fs-2))
ax = list(pylab.axis())
ax[3] = ax[3] + 0.2
pylab.axis(ax)
pylab.legend(['complete execution'], loc='lower right')

pylab.subplot(2, 1, 2)
pylab.plot(x['total_time'][:(imin+1)], x['tree_prefix_length'][:(imin+1)], 'b-', linewidth=lw)
pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('length', fontsize=fs)
#pylab.title('length of rule list with current best objective', fontsize=fs)
pylab.xticks(fontsize=(fs-2))
pylab.yticks(fontsize=(fs-2))
ax = list(pylab.axis())
ax[3] = ax[3] + 0.2
pylab.axis(ax)
pylab.legend(['optimization phase'], loc='lower right')
pylab.draw()
pylab.savefig('../figs/ela-prefix-length.png')

max_len_check = x['tree_min_objective'] / c
max_len_check[max_len_check > nrules] = nrules
max_len_check[x['tree_min_objective'] % c == 0] -= 1
max_len_check = np.cast[int](max_len_check)

pylab.figure(8)
pylab.clf()
pylab.subplot(2, 1, 1)
pylab.plot(x['total_time'], max_len_check, 'b-', linewidth=lw)
#pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('length', fontsize=fs)
pylab.title('upper bound on prefix length in remaining search space', fontsize=fs)
pylab.xticks(fontsize=(fs-2))
pylab.yticks(fontsize=(fs-2))
pylab.legend(['complete execution'])

pylab.subplot(2, 1, 2)
pylab.plot(x['total_time'][:(imin+1)], max_len_check[:(imin+1)], 'b-', linewidth=lw)
pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('length', fontsize=fs)
#pylab.title('length of rule list with current best objective', fontsize=fs)
pylab.xticks(fontsize=(fs-2))
pylab.yticks(fontsize=(fs-2))
pylab.legend(['optimization phase'])
pylab.draw()
pylab.savefig('../figs/ela-max-length-check.png')

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
pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('time (s)', fontsize=fs)
pylab.legend(['total', 'prefix + rule list evaluation', 'permutation map', 'cache insertion', 'node selection'], loc='upper left')
pylab.savefig('../figs/ela-time.png')
pylab.draw()

"""
Notes on timing measurements:
Nicholas's timing measurements, as function of wall clock time.
We wouldn't include it in the paper, but it's useful for us to look at.
The lines are different timing measurements corresponding to different
pieces of our algorithm, stacked on top of each other.
They add up to the (separately measured) total time, which verifies that
we're properly measuring things.
That the lines are straight means that, at least for this experiment,
the proportional time spent in different parts of the algorithm stays constant.
If I'm interpreting the timing measurements correctly then our computation time
is dominated by prefix and rule list evaluation (rather than other stuff,
like scheduling, cache insertions, or permutation map operations).

What about other stuff, like deleting from the cache?
Note that the permutation map insertion function can trigger
cache deletions.

"""

print 'total time:', x['total_time'][-1]
print 'prefix + rule list evaluation time:', y[0][-1]
print 'permutation operations time:', y[1][-1]
print 'cache insertion time:', y[2][-1]
print 'node selection time:', y[3][-1]
