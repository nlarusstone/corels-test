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
# no-minor execution using ~350GB RAM when halted
#log_dir = '/Users/elaine/Dropbox/bbcache/logs/keep/'
log_dir = '/Users/elaine/Dropbox/bbcache/logs/corels/'
log_root_list = ['for-%s-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=999999999-c=0.0050000-v=10-f=1000.txt',
'for-%s-curious_lb-with_prefix_perm_map-no_minor-removed=none-max_num_nodes=999999999-c=0.0050000-v=10-f=1000.txt']
fold = 0

large = False

if large:
    ftag = 'compas_execution_large'
    fs_legend = fs - 1
    legend_xloc = 10**-1.2
    legend_yloc = 0.2
    wo = 'No'
else:
    ftag = 'compas_execution'
    fs_legend = fs - 1.5
    legend_xloc = 10**-2.2
    legend_yloc = 0.1
    wo = 'No'

ntot = len(log_root_list)

pylab.ion()

tname = 'compas_%d_train.out' % fold
log_fname_x = log_root_list[0] % tname
log_fname_y = log_root_list[1] % tname
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
y = y[(y['tree_min_objective'] > 0)]
y['current_lower_bound'][y['current_lower_bound'] > y['tree_min_objective']] = y['tree_min_objective'][-1]

opt = x['tree_min_objective'][-1]
imin = np.nonzero(x['tree_min_objective'] == opt)[0][0]
tmin = x['total_time'][imin]

if large:
    pylab.figure(1, figsize=(14, 7.5))
else:
    #pylab.figure(1, figsize=(9, 6))
    pylab.figure(1, figsize=(12, 5.5))

pylab.clf()
if large:
    ax1 = pylab.subplot2grid((24, 40), (0, 1), colspan=18, rowspan=11)
else:
    #ax1 = pylab.subplot2grid((24, 20), (0, 1), colspan=19, rowspan=10)
    #ax1 = pylab.subplot(2, 2, 1)
    ax1 = pylab.subplot2grid((24, 40), (0, 1), colspan=19, rowspan=11)

ii = (x['current_lower_bound'] < x['tree_min_objective'][-1]).nonzero()[0][-1]

ax1.semilogx(x['total_time'][2:ii], x['tree_min_objective'][2:ii], '-', color='k', linewidth=lw)
ax1.semilogx(x['total_time'][2:ii], x['current_lower_bound'][2:ii], '-', color='gray', linewidth=lw*2)
ax1.semilogx(y['total_time'][1:], y['current_lower_bound'][1:], '--', color='m', linewidth=lw*2)
ax1.semilogx(x['total_time'][2:ii], x['tree_min_objective'][2:ii], '-', color='k', linewidth=lw)
ax1.semilogx(tmin, opt, '*', markerfacecolor='white', markeredgecolor='k', markeredgewidth=2, markersize=18)

ip = (x['tree_prefix_length'][1:] != x['tree_prefix_length'][:-1]).nonzero()[0] + 1
for jj in ip:
    pl = x['tree_prefix_length'][jj]
    (tt, oo) = (x['total_time'][jj], x['tree_min_objective'][jj])
    ax1.semilogx(tt, oo, 'o', color='white', markersize=6, markeredgecolor='k', markeredgewidth=2)
    ax1.text(tt * 1.2, oo + 0.01, str(pl), fontsize=fs)

pylab.ylabel('Value', fontsize=fs)
if large:
    pylab.title('Execution progress (ProPublica dataset)', fontsize=fs)
else:
    pylab.title('Execution progress (ProPublica)', fontsize=fs)
pylab.xticks(fontsize=fs)
pylab.yticks(np.arange(0, 0.55, 0.1), fontsize=fs)
pylab.axis([x['total_time'][2], 10**3, 0, 0.50])
pylab.legend(['Objective (CORELS)', 'Lower bound (CORELS)', 'Lower bound (%s equiv. pts. bound)' % wo], loc=(legend_xloc, legend_yloc), fontsize=fs_legend, frameon=False)

if large:
    ax2 = pylab.subplot2grid((24, 40), (14, 1), colspan=18, rowspan=8)
else:
    #ax2 = pylab.subplot2grid((24, 20), (13, 1), colspan=19, rowspan=8)
    #ax2 = pylab.subplot(2, 2, 3)
    ax2 = pylab.subplot2grid((24, 40), (14, 1), colspan=19, rowspan=8)

yremaining = y['log_remaining_space_size'].copy()
yremaining[yremaining > yremaining[0]] = yremaining[0]
ax2.semilogx(y['total_time'][1:], yremaining[1:], '--', linewidth=lw*2, color='m')

xremaining = x['log_remaining_space_size'].copy()
xremaining[xremaining > xremaining[0]] = xremaining[0]
ax2.semilogx(x['total_time'][2:ii+1], xremaining[2:ii+1], '-', color='k', linewidth=lw)

yremaining = y['log_remaining_space_size'].copy()
yremaining[yremaining > yremaining[0]] = yremaining[0]
ax2.semilogx(y['total_time'][1:], yremaining[1:], '--', linewidth=lw*2, color='m')

pylab.title('Size of remaining search space', fontsize=fs)
pylab.xlabel('Time (s)', fontsize=fs)
pylab.ylabel('log10(Size)', fontsize=fs)
pylab.xticks(fontsize=fs)
if large:
    pylab.yticks(range(0, 160, 50), fontsize=fs)
else:
    pylab.yticks(range(0, 160, 50), fontsize=fs)

legend_text = '%s equivalent points bound' % wo
pylab.legend([legend_text, 'CORELS'], loc='center right', fontsize=fs_legend, frameon=False)
pylab.axis([x['total_time'][2], 10**3, 0, 170])
pylab.draw()
pylab.savefig('../figs/%s-remaining-space.pdf' % ftag)
