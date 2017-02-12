"""
#!/bin/bash

# ./ablation.sh compas 1000000000 none
# ./ablation.sh compas 1000000000 priority
# ./ablation.sh compas 1000000000 support
# ./ablation.sh compas 1000000000 pmap
# ./ablation.sh compas 1000000000 lookahead
# ./ablation.sh compas 800000000 identical

args=("$@")
dataset=${args[0]}
n=${args[1]}
ablation=${args[2]}


for i in `seq 0 9`;
do
    bbcache=./../src/bbcache
    out=../data/CrossValidation/${dataset}_${i}_train.out
    label=../data/CrossValidation/${dataset}_${i}_train.label
    minor=../data/CrossValidation/${dataset}_${i}_train.minor
    if [ "$ablation" = "none" ];
    then
        $bbcache -n ${n} -c 2 -r 0.005 -p 1 $out $label $minor &
    elif [ "$ablation" = "priority" ];
    then
        $bbcache -n ${n} -b -r 0.005 -p 1 $out $label $minor &
    elif [ "$ablation" = "support" ];
    then
        $bbcache -n ${n} -c 2 -r 0.005 -p 1 -a 1 $out $label $minor &
    elif [ "$ablation" = "pmap" ];
    then
        $bbcache -n ${n} -c 2 -r 0.005 $out $label $minor &
    elif [ "$ablation" = "lookahead" ];
    then
        $bbcache -n ${n} -c 2 -r 0.005 -p 1 -a 2 $out $label $minor &
    elif [ "$ablation" = "identical" ];
    then
        $bbcache -n ${n} -c 2 -r 0.005 -p 1 $out $label
    fi
done


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


froot = 'compas'
data_dir = '../data/CrossValidation/'
log_dir = '../logs/'
num_folds = 1
lw = 2  # linewidth
ms = 9  # markersize
fs = 16 # fontsize

"""
log_root_list = ['for-%s-curious_lb-with_prefix_perm_map-minor-max_num_nodes=10000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-bfs-with_prefix_perm_map-minor-max_num_nodes=10000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-minor-max_num_nodes=10000001-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-no_pmap-minor-max_num_nodes=100000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-minor-max_num_nodes=100000001-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-no_minor-max_num_nodes=700000000-c=0.0050000-v=1-f=1000.txt']
labels = ['none', 'no priority queue', 'no support bounds', 'no permutation map', 'no lookahead bound', 'no identical points bound']
ftag = 'kdd_compas_compare'

"""
log_root_list = ['for-%s-curious_lb-with_prefix_perm_map-minor-max_num_nodes=10000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-no_pmap-minor-max_num_nodes=100000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-minor-max_num_nodes=100000001-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-no_minor-max_num_nodes=700000000-c=0.0050000-v=1-f=1000.txt']
labels = ['none', 'no permutation map', 'no lookahead bound', 'no identical points bound']
ftag = 'kdd_compas_compare_small'


ntot = len(log_root_list)

pylab.ion()

fold = 0
tname = 'compas_%d_train.out' % fold
log_fname_x = log_root_list[0] % tname
log_fname_y = log_root_list[-1] % tname

c = float(log_fname.split('c=')[1].split('-')[0])
nrules = len(open(fname, 'rU').read().strip().split('\n'))
print 'num rules:', nrules

log_fname_x = os.path.join(log_dir, log_fname_x)
log_fname_y = os.path.join(log_dir, log_fname_y)
x = tb.tabarray(SVfile=log_fname_x)
y = tb.tabarray(SVfile=log_fname_y)

x = x[x['tree_min_objective'] > 0]
y = y[y['tree_min_objective'] > 0]

imin = np.nonzero(x['tree_min_objective'] == x['tree_min_objective'][-1])[0][0]
tmin = x['total_time'][imin]

pylab.figure(1, figsize=(12, 8))

pylab.clf()
ax1 = pylab.subplot2grid((12, 20), (0, 1), colspan=19, rowspan=5)

ii = (x['current_lower_bound'] < x['tree_min_objective'][-1]).nonzero()[0][-1]

ax1.semilogx(x['total_time'][2:ii], x['tree_min_objective'][2:ii], 'c-', linewidth=lw)
ax1.semilogx(x['total_time'][2:ii], x['current_lower_bound'][2:ii], 'b-', linewidth=lw*2)
ax1.semilogx(y['total_time'][2:], y['current_lower_bound'][2:], 'm--', linewidth=lw*2)
ax1.semilogx(x['total_time'][2:ii], x['tree_min_objective'][2:ii], 'c-', linewidth=lw)
ax1.semilogx(tmin, x['tree_min_objective'][-1] + 0.02, 'k*', markersize=10)

pylab.xticks(fontsize=fs)
pylab.ylabel('value\n', fontsize=fs)
pylab.title('execution progress', fontsize=fs)
pylab.xticks(fontsize=fs)
pylab.yticks(fontsize=fs)
pylab.axis([10**-4, 10**4, 0, 0.45])
pylab.legend(['objective', 'lower bound', 'lower bound w/o  equiv. pts.'], loc=(10**-2, 0.15), fontsize=fs)
ax2 = pylab.subplot2grid((12, 20), (6, 1), colspan=19, rowspan=5)

xremaining = x['log_remaining_space_size'].copy()
xremaining[xremaining > xremaining[0]] = xremaining[0]
ax2.semilogx(x['total_time'][2:ii+1], xremaining[2:ii+1], 'b-', linewidth=lw*2)

yremaining = y['log_remaining_space_size'].copy()
yremaining[yremaining > yremaining[0]] = yremaining[0]
ax2.semilogx(y['total_time'][2:], yremaining[2:], 'm--', linewidth=lw*2)

pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('log10(size)', fontsize=fs)
pylab.xticks(fontsize=fs)
pylab.yticks(range(0, 170, 20), fontsize=fs)
#pylab.legend(['objective', 'lower bound', 'lb no id pts bd'], loc='upper right', fontsize=fs)
pylab.axis([10**-4, 10**4, 0, 160])
pylab.draw()
pylab.savefig('../figs/%s-remaining-space.pdf' % ftag)

for (ncomp, log_root) in enumerate(log_root_list):
    for fold in range(10):
        tname = 'compas_%d_train.out' % fold
        log_fname = log_root % tname
        print log_fname
        fname = os.path.join(data_dir, tname)

        c = float(log_fname.split('c=')[1].split('-')[0])
        nrules = len(open(fname, 'rU').read().strip().split('\n'))
        print 'num rules:', nrules

        log_fname = os.path.join(log_dir, log_fname)
        try:
            print 'reading', log_fname
            x = tb.tabarray(SVfile=log_fname)
        except:
            print 'skipping', log_fname
            continue

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
        print "num insertions (millions): ", x['tree_insertion_num'][-1] / 10**6.

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
        if (ncomp == 0):
            queue_comp = zc.sum(axis=1)
            ii = queue_comp.nonzero()[0]
            queue_comp = queue_comp[ii]
            t_comp = x['total_time'][ii]
        
        print "max queue size (millions): ", zc.sum(axis=1).max() / 10**6.
        color_vec = ['r', 'orange', 'y', 'g', 'c', 'b', 'purple', 'm', 'violet', 'pink', 'gray', 'k']#[:(max_length + 1)][::-1]
        #color_vec = ['purple', 'b', 'c', 'm', 'gray', 'k'][::-1]

        if (len(log_root_list) == 1):
            pylab.figure(6, figsize=(14, 9))
        else:
            pylab.figure(5, figsize=(12, 8))

        if (ncomp == 0):
            pylab.clf()
            #pylab.subplot2grid((10, 20), (0, 1), colspan=19, rowspan=9)

        if (len(log_root_list) == 6):
            pylab.subplot(2, 3, ncomp+1)
        else:
            pylab.subplot(2, 2, ncomp+1)

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

        """
        if (ncomp + 1 < ntot):  
            pylab.fill_between([tmin, x['total_time'][-1]], [10**-0.1, 10**-0.1], [10**8.3, 10**8.3],  color='gray', alpha=0.3)
        else:
            pylab.fill_between([tmin, 10**4], [10**-0.1, 10**-0.1], [10**8.3, 10**8.3],  color='gray', alpha=0.3)
        """
        pylab.fill_between(t_comp, 10**-0.1 * np.ones(len(t_comp)), queue_comp, color='gray', alpha=0.3)

        for length in range(0, max_length + 1):
            jj = zc[:, length].nonzero()[0]
            tt = x['total_time'][jj]
            yy = zc[jj, length]
            if (ncomp + 1 < ntot):
                yy = np.array([1] + list(yy) + [1])
                tt = np.array([tt[0]] + list(tt) + [tt[-1]])
            else:
                yy = np.array([1] + list(yy))
                tt = np.array([tt[0]] + list(tt))
            pylab.loglog(tt, yy, color=color_vec[length % len(color_vec)], linewidth=lw*2)
        if (ntot == 6):
            if (ncomp + 1 == ntot):
                pylab.legend(['%d' % length for length in range(0, max_length + 1)[::-1]], loc='upper left', fontsize=fs-3)
        else:
            pylab.legend(['%d' % length for length in range(0, max_length + 1)[::-1]], loc='upper left', fontsize=fs-3)
        if (ncomp > ntot/2 - 1):
            pylab.xlabel('time (s)', fontsize=fs+2)
        if (ncomp in [0, ntot/2]):
            pylab.ylabel('count', fontsize=fs+2)
        #pylab.suptitle('lengths of prefixes in the logical queue\n', fontsize=fs)
        pylab.title(labels[ncomp], fontsize=fs+2)
        pylab.xticks(fontsize=fs-2)
        pylab.yticks(fontsize=fs-2)
        #pylab.loglog([1, 1], [10**-0.1, 10**8.3], 'k--')
        ax = [10**-4, 10**4, 10**-0.1, 10**8.3]
        pylab.axis(ax)
        pylab.draw()
        if (ncomp + 1 == ntot):
            pylab.savefig('../figs/%s-queue.pdf' % ftag)
