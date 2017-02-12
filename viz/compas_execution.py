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

log_root_list = ['for-%s-curious_lb-with_prefix_perm_map-minor-max_num_nodes=10000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-no_minor-max_num_nodes=700000000-c=0.0050000-v=1-f=1000.txt']
ftag = 'compas_execution'

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

opt = x['tree_min_objective'][-1]
imin = np.nonzero(x['tree_min_objective'] == opt)[0][0]
tmin = x['total_time'][imin]

pylab.figure(1, figsize=(12, 8))

pylab.clf()
ax1 = pylab.subplot2grid((12, 20), (0, 1), colspan=19, rowspan=6)

ii = (x['current_lower_bound'] < x['tree_min_objective'][-1]).nonzero()[0][-1]

ax1.semilogx(x['total_time'][2:ii], x['tree_min_objective'][2:ii], 'c-', linewidth=lw)
ax1.semilogx(x['total_time'][2:ii], x['current_lower_bound'][2:ii], 'b-', linewidth=lw*2)
ax1.semilogx(y['total_time'][2:], y['current_lower_bound'][2:], 'm--', linewidth=lw*2)
ax1.semilogx(x['total_time'][2:ii], x['tree_min_objective'][2:ii], 'c-', linewidth=lw)
ax1.semilogx([tmin, tmin], [0, 0.5], 'k:', linewidth=lw)

ip = (x['tree_prefix_length'][1:] != x['tree_prefix_length'][:-1]).nonzero()[0] + 1
for jj in ip:
    pl = x['tree_prefix_length'][jj]
    (tt, oo) = (x['total_time'][jj], x['tree_min_objective'][jj])
    ax1.semilogx(tt, oo, 'ko')#, color='gray')
    ax1.text(tt, oo + 0.015, str(pl), fontsize=fs)

pylab.xticks(fontsize=fs)
pylab.ylabel('value\n', fontsize=fs)
pylab.title('execution progress', fontsize=fs)
pylab.xticks(fontsize=fs)
pylab.yticks(np.arange(0, 0.50, 0.05), fontsize=fs)
pylab.axis([10**-4, 10**4, 0, 0.48])
pylab.legend(['objective (CORELS)', 'lower bound (CORELS)', 'lower bound (w/o  equivalent points bound)'], loc=(10**-1.9, 0.15), fontsize=fs)

ax2 = pylab.subplot2grid((12, 20), (7, 1), colspan=19, rowspan=4)

yremaining = y['log_remaining_space_size'].copy()
yremaining[yremaining > yremaining[0]] = yremaining[0]
ax2.semilogx(y['total_time'][2:], yremaining[2:], 'm--', linewidth=lw*2)

xremaining = x['log_remaining_space_size'].copy()
xremaining[xremaining > xremaining[0]] = xremaining[0]
ax2.semilogx(x['total_time'][2:ii+1], xremaining[2:ii+1], 'b-', linewidth=lw*2)

pylab.title('remaining search space', fontsize=fs)
pylab.xlabel('time (s)', fontsize=fs)
pylab.ylabel('log10(size)', fontsize=fs)
pylab.xticks(fontsize=fs)
pylab.yticks(range(0, 170, 20), fontsize=fs)
pylab.legend(['w/o equivalent point bound', 'CORELS'], loc='center right', fontsize=fs)
pylab.axis([10**-4, 10**4, 0, 160])
pylab.draw()
pylab.savefig('../figs/%s-remaining-space.pdf' % ftag)
