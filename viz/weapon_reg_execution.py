"""
See also `weapon_ablation.py`

"""
import os

import gmpy2
import numpy as np
import pylab
import tabular as tb

import utils


# see:  http://phyletica.org/matplotlib-fonts/
pylab.rcParams['pdf.fonttype'] = 42
pylab.rcParams['ps.fonttype'] = 42

#froot = 'frisk'
froot = 'weapon'
data_dir = '../data/CrossValidation/'
log_dir = '../logs/'
lw = 2  # linewidth
ms = 9  # markersize

num_folds = 10
figure_fold = -1
make_small = False

num_folds = 1
figure_fold = 1

# log files generated on beepboop
#log_dir = '/Users/elaine/Dropbox/bbcache/logs/keep/'
#log_dir = '/Users/elaine/Dropbox/bbcache/logs/corels/'
#log_dir = '/Users/elaine/Dropbox/bbcache/logs/arxiv/'
log_dir = '/Users/nlarusstone/Documents/Research/bbcache/jmlr'

log_root_list = ['for-%s-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=100000002-c=0.0400000-v=10-f=1000.txt',
    'for-%s-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=100000002-c=0.0100000-v=10-f=1000.txt',
    'for-%s-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=100000002-c=0.0025000-v=10-f=1000.txt']

labels = ['$\lambda$ = 0.04', '$\lambda$ = 0.01', '$\lambda$ = 0.0025']
ftag = "weapon_reg"

if make_small:
    fs = 16
    fs_legend = fs - 2
else:
    fs = 17
    fs_legend = fs - 3

pylab.ion()
if (make_small):
    pylab.figure(5, figsize=(12, 6.4))
    ftag = '%s_small' % ftag
    fs += 3
    fs_legend += 3
else:
    pylab.figure(6, figsize=(16, 5.8))
pylab.clf()

ntot = len(log_root_list)
c1 = ['pink', 'red', 'brown']
c1 = ['lightgray', 'gray', 'black']
#c1 = ['gray', 'coral', 'c']
c2 = ['skyblue', 'c', 'blue']
fold = 0

for (ncomp, log_root) in enumerate(log_root_list):
    tname = '%s_%d_train.out' % (froot, figure_fold)
    log_fname = log_root % tname
    print log_fname
    fname = os.path.join(data_dir, tname)

    c = float(log_fname.split('c=')[1].split('-')[0])

    log_fname = os.path.join(log_dir, log_fname)
    try:
        print 'reading', log_fname
        x = tb.tabarray(SVfile=log_fname)
    except:
        print 'skipping', log_fname
        continue

    x['total_time'] = x['total_time'] - x['total_time'][0] + 10**-4
    ii = (x['current_lower_bound'] < x['tree_min_objective'][-1]).nonzero()[0][-1]
    ii += 1

    opt = x['tree_min_objective'][-1]
    imin = np.nonzero(x['tree_min_objective'] == opt)[0][0]
    tmin = x['total_time'][imin]

    if (make_small):
        pylab.subplot(2, 2, ncomp + 1)
    else:
        pylab.subplot(2, 4, ncomp + 1)

    pylab.semilogx(x['total_time'][2:ii], x['tree_min_objective'][2:ii], '-', color='b', linewidth=lw)
    pylab.semilogx(x['total_time'][2:ii], x['current_lower_bound'][2:ii], '--', color='k', linewidth=lw)
    pylab.semilogx(tmin, opt, '*', markerfacecolor='white', markeredgecolor='k', markeredgewidth=2, markersize=20)

    ip = (x['tree_prefix_length'][1:] != x['tree_prefix_length'][:-1]).nonzero()[0] + 1
    for jj in ip:
        pl = x['tree_prefix_length'][jj]
        (tt, oo) = (x['total_time'][jj], x['tree_min_objective'][jj])
        pylab.semilogx(tt, oo, 'o', markerfacecolor='white', markeredgewidth=2, markersize=6, markeredgecolor='k')
        pylab.text(tt * 1.1, oo + 0.025, str(pl), fontsize=fs-2)

    pylab.xticks(10.**np.array([-2, 0, 2]), fontsize=fs-1)
    if (make_small):
        pylab.text(10**-1.2, 0.46, labels[ncomp], fontsize=fs)
    else:
        pylab.title(labels[ncomp], fontsize=fs)
    pylab.xticks(10.**np.array([-2, 0, 2]), fontsize=fs-2)
    pylab.yticks(np.arange(0, 0.59, 0.2), fontsize=fs)
    pylab.axis([x['total_time'][2], 10**3, 0, 0.55])
    if (ncomp % 3 == 0):
        pylab.ylabel('Value', fontsize=fs)
        pylab.legend(['Objective', 'Lower bound', 'Optimum'], loc='lower right', fontsize=fs_legend, numpoints=1, frameon=False)

    if (make_small):
        if (ncomp == 2):
            pylab.ylabel('Value', fontsize=fs)
            pylab.xticks(10.**np.array([-2, 0, 2]), fontsize=fs-1)
            pylab.xlabel('Time (s)', fontsize=fs)
        pylab.subplot(2, 2, 4)
    else:
        pylab.subplot(2, 4, 4)

    print 'Obj:', x['tree_min_objective'][2:ii]
    print 'LB:', x['current_lower_bound'][2:ii]
    pylab.semilogx(x['total_time'][2:ii], x['tree_min_objective'][2:ii], '-', color='b', linewidth=lw)
    pylab.semilogx(x['total_time'][2:ii], x['current_lower_bound'][2:ii], '--', color='k', linewidth=lw)
    #pylab.semilogx(tmin, opt, 'k*', markersize=18)
    pylab.xticks(10.**np.array([-2, 0, 2]), fontsize=fs-1)
    pylab.yticks(np.arange(0, 0.59, 0.2), fontsize=fs)
    pylab.axis([x['total_time'][2], 10**3, 0, 0.55])
    if (make_small):
        if (ncomp == 0):
            pylab.text(10**-1.5, 0.45, ' Overlay', fontsize=fs)
    else:
        pylab.title('Overlay', fontsize=fs)
    pylab.xticks(10.**np.array([-2, 0, 2]), fontsize=fs-1)

    if (make_small):
        pylab.xlabel('Time (s)', fontsize=fs)
    else:
        pylab.subplot(2, 4, ncomp + 5)
        xremaining = x['log_remaining_space_size'].copy()
        xremaining[xremaining > xremaining[0]] = xremaining[0]
        xtt = np.concatenate((x['total_time'][2:ii+1], x['total_time'][ii:ii+1]))
        xrr = np.concatenate((xremaining[2:ii+1], [1.]))
        pylab.semilogx(xtt, xrr, '-', color='c', linewidth=lw*2)
        if (ncomp % 3 == 0):
            pylab.ylabel('log10(Size)', fontsize=fs)
            pylab.legend(['Upper bound on\nsize of remaining\nsearch space'], fontsize=fs_legend, loc='best', frameon=False)
        pylab.xlabel('Time (s)', fontsize=fs)
        pylab.xticks(10.**np.array([-2, 0, 2]), fontsize=fs-1)
        pylab.yticks(range(0, 40, 10), fontsize=fs)
        pylab.axis([x['total_time'][2], 10**3, 0, 32])
        pylab.subplot(2, 4, 8)
        pylab.semilogx(xtt, xrr, '-', color='c', linewidth=lw*2)
        pylab.yticks(range(0, 40, 10), fontsize=fs)
        pylab.axis([x['total_time'][2], 10**3, 0, 32])
        pylab.xlabel('Time (s)', fontsize=fs)
        pylab.xticks(10.**np.array([-2, 0, 2]), fontsize=fs-1)

#pylab.suptitle('Execution progress for different regularization parameters (NYCLU dataset)\n', fontsize=fs+2)
pylab.savefig('../figs/%s-execution.pdf' % ftag)
