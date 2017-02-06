"""
for-compas_0_train.out-curious_lb-with_prefix_perm_map-minor-max_num_nodes=10000000-c=0.0050000-v=1-f=1000.txt
num rules: 155
num records: 1652
time to achieve optimum: 7.2291680791
time to verify optimum: 336.063088079

for-compas_0_train.out-bfs-with_prefix_perm_map-minor-max_num_nodes=10000000-c=0.0050000-v=1-f=1000.txt
num rules: 155
num records: 1971
time to achieve optimum: 3.6754978271
time to verify optimum: 452.650077827

for-compas_0_train.out-curious_lb-no_pmap-minor-max_num_nodes=100000000-c=0.0050000-v=1-f=1000.txt
num rules: 155
num records: 15023
time to achieve optimum: 18.6063890327
time to verify optimum: 3633.52008903

for-compas_0_train.out-curious_lb-with_prefix_perm_map-minor-max_num_nodes=10000001-c=0.0050000-v=1-f=1000.txt
num rules: 155
num records: 2426
time to achieve optimum: 10.7684899864
time to verify optimum: 580.760089986

for-compas_0_train.out-curious_lb-with_prefix_perm_map-minor-max_num_nodes=100000001-c=0.0050000-v=1-f=1000.txt
num rules: 155
num records: 19578
time to achieve optimum: 7.560236887
time to verify optimum: 4401.11008689

for-compas_0_train.out-curious_lb-with_prefix_perm_map-no_minor-max_num_nodes=700000000-c=0.0050000-v=1-f=1000.txt
num rules: 155
num records: 4174
time to achieve optimum: 48.0518921322
time to verify optimum: 1893.80009213

"""
import os

import gmpy2
import numpy as np
import pylab
import tabular as tb


def parse_prefix_lengths(p):
    ij = [q.split(':') for q in p.split(';') if q]
    return np.array([(int(i), int(j)) for (i, j) in ij])

def parse_prefix_sums(p):
    return np.sum([int(q.split(':')[1]) for q in p.split(';') if q])

# priority queue
# ./bbcache -c 2 -p 1 -r 0.005 -n 10000000 ../data/CrossValidation/compas_0_train.out ../data/CrossValidation/compas_0_train.label ../data/CrossValidation/compas_0_train.minor 

# BFS
# ./bbcache -b -p 1 -r 0.005 -n 10000000 ../data/CrossValidation/compas_0_train.out ../data/CrossValidation/compas_0_train.label ../data/CrossValidation/compas_0_train.minor 

# no permutation map
# ./bbcache -c 2 -r 0.005 -n 100000000 ../data/CrossValidation/compas_0_train.out ../data/CrossValidation/compas_0_train.label ../data/CrossValidation/compas_0_train.minor 

# no captures bounds
# ./bbcache -c 2 -p 1 -r 0.005 -n 10000001 ../data/CrossValidation/compas_0_train.out ../data/CrossValidation/compas_0_train.label ../data/CrossValidation/compas_0_train.minor

# no lookahead bound
# ./bbcache -c 2 -p 1 -r 0.005 -n 100000001 ../data/CrossValidation/compas_0_train.out ../data/CrossValidation/compas_0_train.label ../data/CrossValidation/compas_0_train.minor

# no identical points bound
# ./bbcache -c 2 -p 1 -r 0.005 -n 700000000 ../data/CrossValidation/compas_0_train.out ../data/CrossValidation/compas_0_train.label

froot = 'compas'
data_dir = '../data/CrossValidation/'
log_dir = '../logs/'
log_root_list = ['for-%s-curious_lb-with_prefix_perm_map-minor-max_num_nodes=10000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-bfs-with_prefix_perm_map-minor-max_num_nodes=10000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-no_pmap-minor-max_num_nodes=100000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-minor-max_num_nodes=10000001-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-minor-max_num_nodes=100000001-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-no_minor-max_num_nodes=700000000-c=0.0050000-v=1-f=1000.txt']
ftag = 'ela_compas_compare'
num_folds = 1
lw = 2  # linewidth
ms = 9  # markersize
fs = 16 # fontsize
ntot = len(log_root_list)

labels = ['priority queue', 'BFS', 'no permutation map', 'no support bounds', 'no lookahead bound', 'no identical points bound']

pylab.ion()

fold = 0

tname = 'compas_%d_train.out' % fold

for (ncomp, log_root) in enumerate(log_root_list):
    log_fname = log_root % tname
    print log_fname
    fname = os.path.join(data_dir, tname)

    c = float(log_fname.split('c=')[1].split('-')[0])
    nrules = len(open(fname, 'rU').read().strip().split('\n'))
    print 'num rules:', nrules

    log_fname = os.path.join(log_dir, log_fname)
    print 'reading', log_fname
    x = tb.tabarray(SVfile=log_fname)
    #x = x[:-1]  # ignore last log record because it measures the time to delete the queue

    x['total_time'] = x['total_time'] - x['total_time'][0] + 10**-4

    if ('no_minor' in log_fname):
        x = x[x['tree_min_objective'] > 0]

    default_objective = x['tree_min_objective'][1]
    imin = np.nonzero(x['tree_min_objective'] == x['tree_min_objective'][-1])[0][0]
    tmin = x['total_time'][imin]

    prefix_sums = np.array([parse_prefix_sums(p) for p in x['prefix_lengths']])

    print "num records:", len(x)
    print "time to achieve optimum:", tmin
    print "time to verify optimum:", x['total_time'][-1]

    pylab.figure(1, figsize=(7, 5))
    if (ncomp == 0):
        pylab.clf()
        ax1 = pylab.subplot2grid((12, 20), (0, 1), colspan=19, rowspan=5)

    if ('curious_lb' in log_fname):
        ii = (x['current_lower_bound'] < x['tree_min_objective'][-1]).nonzero()[0][-1]
    else:
        ii = len(x)
    #ax1.semilogx(x['total_time'][2:ii], x['tree_min_objective'][2:ii], '-', color='b', linewidth=lw*2)
    if ('curious_lb' in log_fname):
        ax1.semilogx(x['total_time'][2:ii], x['current_lower_bound'][2:ii], '-', linewidth=lw)

    if (ncomp == 0):
        ax = list(pylab.axis())
        #ax[0] = x['total_time'][2]
        #ax[1] = 10**2.7
        #ax[2] = 0.3
        #ax[3] = 0.45
        #pylab.axis(ax)
        pylab.xticks(fontsize=fs)
        #pylab.yticks(np.arange(0.3, 0.5, 0.05), fontsize=fs)
        #pylab.xlabel('time (s)', fontsize=fs)
        pylab.ylabel('value\n', fontsize=fs)
        pylab.title('execution progress', fontsize=fs)
        pylab.xticks(fontsize=fs)
        pylab.yticks(fontsize=fs)
        #pylab.legend(['objective', 'lower bound'], loc='upper right', fontsize=fs)

    if (ncomp == 0):
        ax2 = pylab.subplot2grid((12, 20), (6, 1), colspan=19, rowspan=5)

    xremaining = x['log_remaining_space_size'].copy()
    xremaining[xremaining > xremaining[0]] = xremaining[0]
    ax2.semilogx(x['total_time'], xremaining, '-', linewidth=lw)
    
    if (ncomp == 0):
        pylab.xlabel('time (s)', fontsize=fs)
        pylab.ylabel('log10(size)', fontsize=fs)
        #pylab.legend(['remaining search space'], fontsize=fs, loc='upper right')
    
        #ax = list(pylab.axis())
        #ax[0] = x['total_time'][2]
        #ax[1] = 10**2.7
        #ax[3] = 30
        #pylab.axis(ax)
        pylab.xticks(fontsize=fs)
        #pylab.yticks(range(0, 35, 5), ['0', '5', '10', '15', '20', '25', '~159'], fontsize=fs)

    pylab.draw()
    if (ncomp + 1 == ntot):
        pylab.savefig('../figs/%s-remaining-space.pdf' % ftag)

    pylab.figure(2, figsize=(7, 5))
    if (ncomp == 0):
        pylab.clf()
    pylab.subplot2grid((10, 20), (0, 2), colspan=19, rowspan=9)
    pylab.plot(x['total_time'], x['tree_num_nodes'] / 10.**6, 'b-', linewidth=lw*2)
    pylab.plot(x['total_time'], x['queue_size'] / 10.**6, 'c--', linewidth=lw*2)
    pylab.plot(x['total_time'], prefix_sums / 10.**6, 'm-', linewidth=lw)
    pylab.xlabel('time (s)', fontsize=fs)
    pylab.ylabel('size (millions)', fontsize=fs)
    pylab.title('data structure size', fontsize=fs)
    pylab.xticks(fontsize=fs-1)
    pylab.yticks(fontsize=fs-1)
    pylab.legend(['cache', 'physical queue', 'logical queue'], fontsize=fs, loc='upper right')
    pylab.draw()
    if (ncomp + 1 == ntot):
        pylab.savefig('../figs/%s-queue-cache-size-insertions.pdf' % ftag)

    prefix_lengths = list(x['prefix_lengths'])
    if ('bfs' in log_fname):
        prefix_lengths = ['1:1;2:8721;3:4243;' if (pl == '2:8721;3:4243;') else pl for pl in prefix_lengths]

    max_length = max(set([int(lc.split(':')[0]) for lc in ''.join(prefix_lengths).split(';') if lc]))
    split_hist = [[lc.split(':') for lc in lh.strip(';').split(';')] for lh in prefix_lengths]
    kvp = [[(lc[0], int(lc[1])) for lc in lh if (len(lc) == 2)] for lh in split_hist]
    z = tb.tabarray(kvpairs=kvp)
    assert ([int(name) for name in z.dtype.names] == range(max_length + 1))
    #zc = z.extract()[:, ::-1].cumsum(axis=1)[:, ::-1]
    zc = z.extract()
    color_vec = ['r', 'orange', 'y', 'g', 'c', 'b', 'purple', 'm', 'violet', 'pink', 'gray', 'k']#[:(max_length + 1)][::-1]
    #color_vec = ['purple', 'b', 'c', 'm', 'gray', 'k'][::-1]

    pylab.figure(6, figsize=(14, 9))
    if (ncomp == 0):
        pylab.clf()
        #pylab.subplot2grid((10, 20), (0, 1), colspan=19, rowspan=9)
    pylab.subplot(2, 3, ncomp+1)

    for length in range(0, max_length + 1)[::-1]:
        jj = zc[:, length].nonzero()[0]
        tt = x['total_time'][jj]
        yy = zc[jj, length]
        if (ncomp < 3):
            yy = np.array([1] + list(yy) + [1])
            tt = np.array([tt[0]] + list(tt) + [tt[-1]])
        else:
            yy = np.array([1] + list(yy))
            tt = np.array([tt[0]] + list(tt))
        pylab.loglog(tt, yy, color=color_vec[length % len(color_vec)], linewidth=lw*2)

    if (ncomp + 1 < ntot):  
        pylab.fill_between([tmin, x['total_time'][-1]], [10**-0.1, 10**-0.1], [10**8, 10**8],  color='gray', alpha=0.3)
    else:
        pylab.fill_between([tmin, 10**4], [10**-0.1, 10**-0.1], [10**8, 10**8],  color='gray', alpha=0.3)

    for length in range(0, max_length + 1):
        jj = zc[:, length].nonzero()[0]
        tt = x['total_time'][jj]
        yy = zc[jj, length]
        if (ncomp < 5):
            yy = np.array([1] + list(yy) + [1])
            tt = np.array([tt[0]] + list(tt) + [tt[-1]])
        else:
            yy = np.array([1] + list(yy))
            tt = np.array([tt[0]] + list(tt))
        pylab.loglog(tt, yy, color=color_vec[length % len(color_vec)], linewidth=lw*2)
    if (ncomp + 1 == ntot):
        pylab.legend(['%d' % length for length in range(0, max_length + 1)[::-1]], loc='upper left', fontsize=fs-3)
    if (ncomp > 2):
        pylab.xlabel('time (s)', fontsize=fs+2)
    if (ncomp in [0, 3]):
        pylab.ylabel('count', fontsize=fs+2)
    #pylab.suptitle('lengths of prefixes in the logical queue\n', fontsize=fs)
    pylab.title(labels[ncomp], fontsize=fs+2)
    pylab.xticks(fontsize=fs-2)
    pylab.yticks(fontsize=fs-2)
    ax = [10**-4, 10**4, 10**-0.1, 10**8]
    pylab.axis(ax)
    pylab.draw()
    if (ncomp + 1 == ntot):
        pylab.savefig('../figs/%s-queue.pdf' % ftag)
