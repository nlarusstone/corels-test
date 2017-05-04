"""
For KDD 2017 Figure 4.  See also `kdd_compas_ablation.py`


"""
import os

import gmpy2
import numpy as np
import pylab
import tabular as tb


froot = 'compas'
data_dir = '../data/CrossValidation/'
num_folds = 1
lw = 2  # linewidth
ms = 9  # markersize
fs = 16 # fontsize

# log files generated on beepboop
# no-minor execution using just under 400GB RAM when halted
log_dir = '../logs/keep/'
log_root_list = ['for-%s-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=1000000000-c=0.0050000-v=1-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-no_minor-removed=none-max_num_nodes=800000000-c=0.0050000-v=1-f=1000.txt']
fold = 1

large = True

if large:
    ftag = 'compas_execution_large'
    fs_legend = fs
    legend_xloc = 10**-1.2
    wo = 'Without'
else:
    ftag = 'compas_execution'
    fs_legend = fs - 2
    legend_xloc = 10**-0.6
    wo = 'w/o'

ntot = len(log_root_list)

pylab.ion()

tname = 'compas_%d_train.out' % fold
log_fname_x = log_root_list[0] % tname
log_fname_y = log_root_list[-1] % tname
fname = os.path.join(data_dir, tname)

c = float(log_fname_x.split('c=')[1].split('-')[0])
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

if large:
    pylab.figure(1, figsize=(9, 9))
else:
    pylab.figure(1, figsize=(9, 6))

pylab.clf()
if large:
    ax1 = pylab.subplot2grid((30, 20), (0, 1), colspan=19, rowspan=12)
else:
    ax1 = pylab.subplot2grid((24, 20), (0, 1), colspan=19, rowspan=10)

ii = (x['current_lower_bound'] < x['tree_min_objective'][-1]).nonzero()[0][-1]

ax1.semilogx(x['total_time'][2:ii], x['tree_min_objective'][2:ii], '-', color='gray', linewidth=lw)
ax1.semilogx(x['total_time'][2:ii], x['current_lower_bound'][2:ii], '-', color='coral', linewidth=lw*2)
ax1.semilogx(y['total_time'][1:], y['current_lower_bound'][1:], '--', color='mediumblue', linewidth=lw*2)
ax1.semilogx(x['total_time'][2:ii], x['tree_min_objective'][2:ii], '-', color='gray', linewidth=lw)
ax1.semilogx(tmin, opt + 0.035, 'k*', markersize=10)
ax1.semilogx(tmin, opt, 'k|', markeredgewidth=lw)

ip = (x['tree_prefix_length'][1:] != x['tree_prefix_length'][:-1]).nonzero()[0] + 1
for jj in ip:
    pl = x['tree_prefix_length'][jj]
    (tt, oo) = (x['total_time'][jj], x['tree_min_objective'][jj])
    ax1.semilogx(tt, oo, 'k|', markeredgewidth=lw)
    ax1.text(tt, oo + 0.015, str(pl), fontsize=fs)

pylab.xticks(fontsize=fs)
pylab.ylabel('Value', fontsize=fs)
pylab.title('Execution progress (ProPublica dataset)', fontsize=fs)
pylab.xticks(fontsize=fs)
pylab.yticks(np.arange(0, 0.55, 0.1), fontsize=fs)
pylab.axis([x['total_time'][2], 10**4, 0, 0.52])
pylab.legend(['Objective (CORELS)', 'Lower bound (CORELS)', 'Lower bound (%s equivalent points bound)' % wo], loc=(legend_xloc, 0.15), fontsize=fs_legend, frameon=False)

if large:
    ax2 = pylab.subplot2grid((30, 20), (15, 1), colspan=19, rowspan=12)
else:
    ax2 = pylab.subplot2grid((24, 20), (13, 1), colspan=19, rowspan=8)

yremaining = y['log_remaining_space_size'].copy()
yremaining[yremaining > yremaining[0]] = yremaining[0]
ax2.semilogx(y['total_time'][1:], yremaining[1:], '--', linewidth=lw*2, color='mediumblue')

xremaining = x['log_remaining_space_size'].copy()
xremaining[xremaining > xremaining[0]] = xremaining[0]
ax2.semilogx(x['total_time'][2:ii+1], xremaining[2:ii+1], '-', color='coral', linewidth=lw*2)

yremaining = y['log_remaining_space_size'].copy()
yremaining[yremaining > yremaining[0]] = yremaining[0]
ax2.semilogx(y['total_time'][1:], yremaining[1:], '--', linewidth=lw*2, color='mediumblue')

pylab.title('Size of remaining search space', fontsize=fs)
pylab.xlabel('Time (s)', fontsize=fs)
pylab.ylabel('log10(Size)', fontsize=fs)
pylab.xticks(fontsize=fs)
if large:
    pylab.yticks(range(0, 180, 25), fontsize=fs)
else:
    pylab.yticks(range(0, 160, 50), fontsize=fs)

pylab.legend(['%s equivalent points bound' % wo, 'CORELS'], loc='center right', fontsize=fs_legend, frameon=False)
pylab.axis([x['total_time'][2], 10**4, 0, 170])
pylab.draw()
pylab.savefig('../figs/%s-remaining-space.pdf' % ftag)
