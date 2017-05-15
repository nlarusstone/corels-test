"""
For NIPS Figure 5.  See also `kdd_compas_ablation.py`

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

import utils


froot = 'compas'
data_dir = '../data/CrossValidation/'
log_dir = '../logs/'
lw = 2  # linewidth
ms = 9  # markersize
fs = 15 # fontsize

num_folds = 1
make_figure = True

# log files generated on beepboop
# no-minor execution using just under 400GB RAM when halted
log_dir = '../logs/keep/'
log_root_list = ['for-%s-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=1000000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-bfs-with_prefix_perm_map-minor-removed=none-max_num_nodes=1000000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-minor-removed=support-max_num_nodes=1000000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-minor-removed=lookahead-max_num_nodes=1000000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-no_pmap-minor-removed=none-max_num_nodes=1000000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-no_minor-removed=none-max_num_nodes=800000000-c=0.0050000-v=1-f=1000.txt']
labels = ['CORELS', 'No priority queue (BFS)', 'No support bounds', 'No lookahead bound',  'No symmetry-aware map', 'No equivalent points bound']
ftag = "nips_compas_ablation"

log_root_list = log_root_list[:1] + log_root_list[-3:]
labels = labels[:1] + labels[-3:]
pylab.ion()
pylab.figure(5, figsize=(16, 3))

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
        if (fold == 0):
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

        color_vec = ['r', 'r', 'orange', 'y', 'g', 'c', 'b', 'purple', 'm', 'violet', 'pink', 'gray', 'k']#[:(max_length + 1)][::-1]
        color_vec = ['k', 'violet', 'm', 'purple', 'b', 'c', 'g', 'yellowgreen', 'y', 'orange', 'r', 'brown']
        #color_vec = ['purple', 'b', 'c', 'm', 'gray', 'k'][::-1]

        if (ncomp == 0):
            pylab.clf()

        pylab.subplot2grid((10, 80), (0, ncomp * 20), colspan=16, rowspan=9)

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

        pylab.xlabel('Time (s)', fontsize=fs)
        if (ncomp == 0):
            pylab.ylabel('Count', fontsize=fs)
        (ymin, ymax) = (10**-0.1, 10**8.3)
        t_corels = int(np.round(t_comp[-1]))
        tmax = np.round(tt[-1])
        xloc = 10**-3.6
        if (ncomp == 0):
            pylab.plot([t_corels, t_corels], [ymin, ymax], 'k--', linewidth=lw)
            pylab.text(xloc, 10**7.4, 'T $\\equiv$ %d s' % t_corels, fontsize=fs)
        else:
            if (tmax / t_corels) < 10:
                descr = '%d s $\\approx$ %1.1f T' % (np.round(tmax), tmax / t_corels)
            else:
                descr = '%d s $\\approx$ %d T' % (np.round(tmax), np.round(tmax / t_corels))
            if (ncomp == (ntot - 1)):
                descr = '> %s' % descr
            else:
                pylab.plot([tmax, tmax], [ymin, ymax], 'k--', linewidth=lw)
            pylab.text(xloc, 10**7.4, descr, fontsize=fs)
        pylab.title(labels[ncomp], fontsize=fs-2)
        pylab.xticks(10.**np.array([-3, -1, 1, 3]), fontsize=fs)
        pylab.yticks(10.**np.array([0, 2, 4, 6, 8]), fontsize=fs)
        #pylab.loglog([1, 1], [10**-0.1, 10**8.3], 'k--')
        ax = [10**-4, 10**4, ymin, ymax]
        pylab.axis(ax)
        pylab.draw()
        if (ncomp + 1 == ntot):
            pylab.legend(['%d' % ii for ii in range(1, 10)], bbox_to_anchor=(1., 1.04), loc=2, fontsize=fs-2, labelspacing=0.3)
            #pylab.suptitle('Execution traces of queue contents (ProPublica dataset)', fontsize=fs+2)
            pylab.savefig('../figs/%s-queue.pdf' % ftag)
