"""
Something Elaine could generate quickly

Not necessarily meant for future use

"""
import numpy as np
import pylab
import tabular as tb

def parse_prefix_lengths(p):
    ij = [q.split(':') for q in p.split(';') if q]
    return np.array([(int(i), int(j)) for (i, j) in ij])

def parse_prefix_sums(p):
    return np.sum([int(q.split(':')[1]) for q in p.split(';') if q])

# Command run:  ./bbcache -c -p 1 ../data/tdata_R.out ../data/tdata_R.label

log_fname = '../logs/for-tdata_R.out-curiosity-with_prefix_perm_map-max_num_nodes=100000-c=0.0010000-v=1.txt'
lw = 2  # linewidth
ms = 7  # markersize
fs = 16 # fontsize

x = tb.tabarray(SVfile=log_fname)
x = x[:-1]  # ignore last log record because it measures the time to delete the queue

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
pylab.plot(x['total_time'][0], x['tree_min_objective'][0], 'ro', markersize=ms)
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
pylab.plot(x['total_time'][0], x['tree_min_objective'][0], 'ro', markersize=ms)
pylab.plot(x['total_time'][ind[0]], x['tree_min_objective'][ind[0]], 'y*', markersize=(ms*2))
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
pylab.plot(x['total_time'], x['tree_num_nodes'], 'b-', linewidth=lw)
pylab.plot(x['total_time'], x['queue_size'], 'r:', linewidth=lw)
pylab.plot(x['total_time'], prefix_sums, 'k-', linewidth=lw)
pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('data structure size', fontsize=fs)
pylab.xticks(fontsize=(fs-2))
pylab.yticks(fontsize=(fs-2))
pylab.legend(['cache', 'physical queue', 'logical queue'])
pylab.savefig('../figs/ela-data-structures.png')

