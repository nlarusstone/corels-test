"""
See also `kdd_compas_execution.py`

#!/bin/bash

# ./ablation.sh weapon 1000000000 none 0.01
# ./ablation.sh weapon 1000000000 priority 0.01
# ./ablation.sh weapon 1000000000 support 0.01
# ./ablation.sh weapon 1000000000 pmap 0.01
# ./ablation.sh weapon 1000000000 lookahead 0.01
# ./ablation.sh weapon 800000000 identical 0.01

args=("$@")
dataset=${args[0]}
n=${args[1]}
ablation=${args[2]}
r=${args[3]}

for i in `seq 0 9`;
do
    bbcache=./../src/bbcache
    out=../data/CrossValidation/${dataset}_${i}_train.out
    label=../data/CrossValidation/${dataset}_${i}_train.label
    minor=../data/CrossValidation/${dataset}_${i}_train.minor
    if [ "$ablation" = "none" ];
    then
        $bbcache -n ${n} -c 2 -r $r -p 1 $out $label $minor &
    elif [ "$ablation" = "priority" ];
    then
        $bbcache -n ${n} -b -r $r -p 1 $out $label $minor &
    elif [ "$ablation" = "support" ];
    then
        $bbcache -n ${n} -c 2 -r $r -p 1 -a 1 $out $label $minor &
    elif [ "$ablation" = "pmap" ];
    then
        $bbcache -n ${n} -c 2 -r $r $out $label $minor &
    elif [ "$ablation" = "lookahead" ];
    then
        $bbcache -n ${n} -c 2 -r $r -p 1 -a 2 $out $label $minor &
    elif [ "$ablation" = "identical" ];
    then
        $bbcache -n ${n} -c 2 -r $r -p 1 $out $label
    fi
done

"""
import os

import gmpy2
import numpy as np
import pylab
import tabular as tb

import utils


froot = 'weapon'
data_dir = '../data/CrossValidation/'
log_dir = '../logs/'
lw = 2  # linewidth
ms = 9  # markersize
fs = 16 # fontsize

num_folds = 10
make_figure = False

#num_folds = 2
#figure_fold = 1
#make_small = False

# log files generated on beepboop
log_dir = '/Users/elaine/Dropbox/bbcache/logs/keep/'
log_root_list = ['for-%s-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=1000000000-c=0.0100000-v=1-f=1000.txt',
'for-%s-bfs-with_prefix_perm_map-minor-removed=none-max_num_nodes=1000000000-c=0.0100000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-minor-removed=support-max_num_nodes=1000000000-c=0.0100000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-minor-removed=lookahead-max_num_nodes=1000000000-c=0.0100000-v=1-f=1000.txt',
'for-%s-curious_lb-no_pmap-minor-removed=none-max_num_nodes=1000000000-c=0.0100000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-no_minor-removed=none-max_num_nodes=1000000000-c=0.0100000-v=1-f=1000.txt']
labels = ['CORELS', 'No priority queue (BFS)', 'No support bounds', 'No lookahead bound', 'No symmetry-aware map', 'No equivalent points bound']
ftag = "weapon_ablation"

if make_small:
    log_root_list = log_root_list[:1] + log_root_list[-3:]
    labels = labels[:1] + labels[-3:]
    ftag += '_small'
    if (make_figure):
        pylab.ion()
        pylab.figure(5, figsize=(12, 8))
else:
    if (make_figure):
        pylab.ion()
        pylab.figure(6, figsize=(11, 13))

ntot = len(log_root_list)

num_rules = np.zeros(num_folds, int)

t_tot = np.zeros((ntot, num_folds))
t_opt = np.zeros((ntot, num_folds))
max_prefix_length = np.zeros((ntot, num_folds), int)
num_insertions = np.zeros((ntot, num_folds), int)
max_queue = np.zeros((ntot, num_folds), int)
min_obj = np.zeros((ntot, num_folds))
lower_bound_num = np.zeros((ntot, num_folds), int)
ablation_names = ['none (CORELS)', 'priority queue', 'support bounds',
                  'symmetry-aware map', 'lookahead bound', 'equiv. pts. bound']

for (ncomp, log_root) in enumerate(log_root_list):
    for fold in range(num_folds):
        #if (make_figure) and (fold == 1):
        #    make_figure = True
        #else:
        #    make_figure = False
        if (fold == figure_fold):
            make_figure = True
        else:
            make_figure = False
        tname = 'weapon_%d_train.out' % fold
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

        prefix_sums = np.array([utils.parse_prefix_sums(p) for p in x['prefix_lengths']])
        n_ins = x['tree_insertion_num'][-1]
        lower_bound_num[ncomp, fold] = x['lower_bound_num'][-1]

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
            color_vec = ['k', 'violet', 'm', 'purple', 'b', 'c', 'green', 'yellowgreen', 'y', 'orange', 'r', 'brown']
            #color_vec = ['purple', 'b', 'c', 'm', 'gray', 'k'][::-1]

            if (ncomp == 0):
                pylab.clf()

            if (len(log_root_list) == 6):
                pylab.subplot(3, 2, ncomp+1)
            else:
                pylab.subplot(2, 2, ncomp+1)

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
                if make_small:
                    if (length == 1):
                        txt = pylab.text(tt[0] * 0.47, 1.5, '%d ' % length, fontsize=fs+4)
                    else:
                        txt = pylab.text(tt[0] * 0.4, 1.5, '%d ' % length, fontsize=fs+4)
            if (ncomp > ntot - 3):
                pylab.xlabel('Time (s)', fontsize=fs+2)
            if (ncomp % 2 == 0):
                pylab.ylabel('Count', fontsize=fs+2)
            (ymin, ymax) = (10**-0.1, 10**8)
            t_corels = int(np.round(t_comp[-1]))
            tmax = np.round(tt[-1])
            if (make_small):
                xloc = tmax / 5000
            else:
                xloc = tmax / 10000
            if (ncomp == 0):
                pylab.plot([t_corels, t_corels], [ymin, ymax], 'k--', linewidth=lw)
                if (make_small):
                    xloc = 0.4
                else:
                    xloc = 0.1
                pylab.text(xloc, 10**7, 'T $\\equiv$ %d s' % t_corels, fontsize=fs)
            else:
                if (tmax / t_corels) < 10:
                    descr = '%d s $\\approx$ %1.1f T' % (np.round(tmax), tmax / t_corels)
                else:
                    descr = '%d s $\\approx$ %d T' % (np.round(tmax), np.round(tmax / t_corels))
                if (ncomp == 4):
                    xloc = 0.02
                else:
                    descr = (14 - (len(descr.split('$')[0] + descr.split('$')[-1]) + 1)) * ' ' + descr
                pylab.plot([tmax, tmax], [ymin, ymax], 'k--', linewidth=lw)
                pylab.text(xloc, 10**7, descr, fontsize=fs)
            #pylab.suptitle('lengths of prefixes in the logical queue\n', fontsize=fs)
            pylab.title(labels[ncomp], fontsize=fs+2)
            pylab.xticks(fontsize=fs-2)
            pylab.yticks(fontsize=fs-2)
            #pylab.loglog([1, 1], [10**-0.1, 10**8.3], 'k--')
            ax = [10**-4, 10**4.9, ymin, ymax]
            pylab.axis(ax)
            pylab.draw()
            if (ncomp + 1 == ntot):
                if not (make_small):
                    pylab.legend(['%d' % ii for ii in range(1, max_length + 1)], bbox_to_anchor=(1., 2.3), loc=2)
                    pylab.suptitle('\nExecution traces of queue contents (NYCLU stop-and-frisk dataset)', fontsize=fs+2)
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
to_m = t_opt.mean(axis=1) * 10**3
to_s = t_opt.std(axis=1) * 10**3
km_m = np.cast[int](max_prefix_length.mean(axis=1))
km_s = max_prefix_length.std(axis=1)
km_min = max_prefix_length.min(axis=1)
km_max = max_prefix_length.max(axis=1)
it_m = num_insertions.mean(axis=1) / 10**5
it_s = num_insertions.std(axis=1) / 10**5
mq_m = max_queue.mean(axis=1) / 10**5
mq_s = max_queue.std(axis=1) / 10**5

for rec in zip(ablation_names, tt_m, tt_s, to_m, to_s, it_m, it_s, mq_m, mq_s, km_min, km_max):
    print '%s & %1.1f (%1.1f) & %d (%d) & %1.1f (%1.1f) & %1.1f (%1.1f) & %d-%d \\\\' % rec

slow_m = (t_tot / t_tot[0]).mean(axis=1) # slowdown
lb_m = lower_bound_num.mean(axis=1) / 10**6
lb_s = lower_bound_num.std(axis=1) / 10**6

print '& Total time & Slow- & Time to & Max evaluated \\\\'
print 'Algorithm variant & (min) & down & optimum ($\mu$s) & prefix length \\\\'
for rec in zip(labels, tt_m, tt_s, slow_m, to_m, to_s, km_min, km_max):
    print '%s & %1.2f (%1.1f) & %1.2f$\\times$ & %1.2f (%1.1f) & %d-%d \\\\' % rec

print '& Lower bound & Total queue &  Max queue~~~~ \\\\'
print 'Algorithm variant & computations ($\\times 10^6$) & insertions ($\\times 10^5$) & size ($\\times 10^5$) \\\\'
for rec in zip(labels, lb_m, lb_s, it_m, it_s, mq_m, mq_s):
    print '%s & %1.2f (%1.1f) & %1.2f (%1.1f) & %1.2f (%1.1f) \\\\' % rec
