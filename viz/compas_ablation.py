"""
For KDD 2017 Table 1.  See also `compas_compare.py`

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
lw = 2  # linewidth
ms = 9  # markersize
fs = 16 # fontsize

num_folds = 10
make_figure = False

num_folds = 2
make_figure = True
make_small = False

# log files generated on beepboop
# no-minor execution using just under 400GB RAM when halted
log_dir = '../logs/keep/'
log_root_list = ['for-%s-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=1000000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-bfs-with_prefix_perm_map-minor-removed=none-max_num_nodes=1000000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-minor-removed=support-max_num_nodes=1000000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-no_pmap-minor-removed=none-max_num_nodes=1000000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-minor-removed=lookahead-max_num_nodes=1000000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-no_minor-removed=none-max_num_nodes=800000000-c=0.0050000-v=1-f=1000.txt']
labels = ['CORELS', 'No priority queue', 'No support bounds', 'No symmetry-aware map', 'No lookahead bound', 'No equivalent points bound']
ftag = "kdd_compas_ablation"

if make_small:
    log_root_list = log_root_list[:1] + log_root_list[-3:]
    labels = labels[:1] + labels[-3:]
    ftag += '_small'
    if (make_figure):
        pylab.figure(5, figsize=(12, 8))
else:
    if (make_figure):
        pylab.figure(6, figsize=(16, 9))

"""
# deprecated log files
log_root_list = ['for-%s-curious_lb-with_prefix_perm_map-minor-max_num_nodes=10000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-bfs-with_prefix_perm_map-minor-max_num_nodes=10000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-minor-max_num_nodes=10000001-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-no_pmap-minor-max_num_nodes=100000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-minor-max_num_nodes=100000001-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-no_minor-max_num_nodes=700000000-c=0.0050000-v=1-f=1000.txt']
labels = ['none', 'no priority queue', 'no support bounds', 'no permutation map', 'no lookahead bound', 'no identical points bound']
ftag = 'kdd_compas_ablation'

# deprecated log files
log_root_list = ['for-%s-curious_lb-with_prefix_perm_map-minor-max_num_nodes=10000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-no_pmap-minor-max_num_nodes=100000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-minor-max_num_nodes=100000001-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-no_minor-max_num_nodes=700000000-c=0.0050000-v=1-f=1000.txt']
labels = ['none', 'no permutation map', 'no lookahead bound', 'no identical points bound']
ftag = 'kdd_compas_ablation_small'
"""

ntot = len(log_root_list)
pylab.ion()

num_rules = np.zeros(num_folds, int)

t_tot = np.zeros((ntot, num_folds))
t_opt = np.zeros((ntot, num_folds))
max_prefix_length = np.zeros((ntot, num_folds), int)
num_insertions = np.zeros((ntot, num_folds), int)
max_queue = np.zeros((ntot, num_folds), int)
min_obj = np.zeros((ntot, num_folds))
ablation_names = ['none (CORELS)', 'priority queue', 'support bounds',
                  'symmetry-aware map', 'lookahead bound', 'equiv. pts. bound']

for (ncomp, log_root) in enumerate(log_root_list):
    for fold in range(num_folds):
        if (fold == 1):
            make_figure = True
        else:
            make_figure = False
        tname = 'compas_%d_train.out' % fold
        log_fname = log_root % tname
        print log_fname
        fname = os.path.join(data_dir, tname)

        c = float(log_fname.split('c=')[1].split('-')[0])
        nrules = len(open(fname, 'rU').read().strip().split('\n'))
        if (ncomp == 0):
            num_rules[fold] = nrules
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

        min_obj[ncomp, fold] = x['tree_min_objective'].min()
        default_objective = x['tree_min_objective'][1]
        imin = np.nonzero(x['tree_min_objective'] == x['tree_min_objective'][-1])[0][0]
        tmin = x['total_time'][imin]
        tmax = x['total_time'][-1]

        prefix_sums = np.array([parse_prefix_sums(p) for p in x['prefix_lengths']])
        n_ins = x['tree_insertion_num'][-1]

        print "num records:", len(x)
        t_opt[ncomp, fold] = tmin
        print "time to achieve optimum:", tmin
        t_tot[ncomp, fold] = tmax
        print "time to verify optimum:", tmax
        num_insertions[ncomp, fold] = n_ins
        print "num insertions (millions): ", n_ins / 10**6.

        prefix_lengths = list(x['prefix_lengths'])
        if ('bfs' in log_fname):
            prefix_lengths = ['1:1;2:8721;3:4243;' if (pl == '2:8721;3:4243;') else pl for pl in prefix_lengths]

        max_length = max(set([int(lc.split(':')[0]) for lc in ''.join(prefix_lengths).split(';') if lc]))
        max_prefix_length[ncomp, fold] = max_length
        print "max prefix length:", max_length
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
        
        max_q = zc.sum(axis=1).max()
        max_queue[ncomp, fold] = max_q
        print "max queue size (millions): ", max_q / 10**6.

        if (make_figure):
            color_vec = ['r', 'r', 'orange', 'y', 'g', 'c', 'b', 'purple', 'm', 'violet', 'pink', 'gray', 'k']#[:(max_length + 1)][::-1]
            color_vec = ['k', 'violet', 'm', 'purple', 'b', 'c', 'g', 'y', 'orange', 'r']
            #color_vec = ['purple', 'b', 'c', 'm', 'gray', 'k'][::-1]

            if (ncomp == 0):
                pylab.clf()
                #pylab.subplot2grid((10, 20), (0, 1), colspan=19, rowspan=9)

            if (len(log_root_list) == 6):
                pylab.subplot(2, 3, ncomp+1)
            else:
                pylab.subplot(2, 2, ncomp+1)

            for length in range(1, max_length + 1)[::-1]:
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

            for length in range(1, max_length + 1):
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
                tx = 10**(np.log10(tt[0] + 0.1 * (np.log10(tt[-1] - np.log10(tt[0])))))
                ix = np.nonzero(tt < tx)[0][-1]
                if (length == 1):
                    txt = pylab.text(tt[0] * 0.47, 1.5, '%d ' % length, fontsize=fs+4)
                else:
                    txt = pylab.text(tt[0] * 0.4, 1.5, '%d ' % length, fontsize=fs+4)
            if (ncomp > ntot/2 - 1):
                pylab.xlabel('Time (s)', fontsize=fs+2)
            if (ncomp in [0, ntot/2]):
                pylab.ylabel('Count', fontsize=fs+2)
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

max_prefix_length += 1
print 'num rules:', num_rules
print 't_tot:', t_tot
print 't_opt:', t_opt
print 'K_max:', max_prefix_length
print 'i_total:', num_insertions
print 'max_Q:', max_queue
print 'min_obj:', min_obj

#tt_m = np.cast[int](np.round(t_tot.mean(axis=1)))
#tt_s = np.cast[int](np.round(t_tot.std(axis=1)))
tt_m = t_tot.mean(axis=1) / 60.
tt_s = t_tot.std(axis=1) / 60.
to_m = np.cast[int](np.round(t_opt.mean(axis=1)))
to_s = np.cast[int](np.round(t_opt.std(axis=1)))
km_m = np.cast[int](max_prefix_length.mean(axis=1))
km_s = max_prefix_length.std(axis=1)
km_min = max_prefix_length.min(axis=1)
km_max = max_prefix_length.max(axis=1)
it_m = num_insertions.mean(axis=1) / 10**6
it_s = num_insertions.std(axis=1) / 10**6
mq_m = max_queue.mean(axis=1) / 10**6
mq_s = max_queue.std(axis=1) / 10**6

for rec in zip(ablation_names, tt_m, tt_s, to_m, to_s, it_m, it_s, mq_m, mq_s, km_min, km_max):
    print '%s & %1.1f (%1.1f) & %d (%d) & %1.1f (%1.1f) & %1.1f (%1.1f) & %d-%d \\\\' % rec

print 'last row:'
print t_tot[-1:].min() / 60
print ((min_obj[-1] - min_obj[0]) < 10**-6).sum()
print t_opt[((min_obj[-1] - min_obj[0]) < 10**-6)].min()
print max_queue[-1].min() / 10**6
