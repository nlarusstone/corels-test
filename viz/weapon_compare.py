import numpy as np
import pylab

# see:  http://phyletica.org/matplotlib-fonts/
pylab.rcParams['pdf.fonttype'] = 42
pylab.rcParams['ps.fonttype'] = 42

pylab.ion()
pylab.figure(1, figsize=(8.5, 3))
#pylab.figure(1, figsize=(5, 6))
pylab.clf()

labels = ['GLM', 'SVM', 'AdaBoost\n\n', 'CART', 'C4.5', 'RF', 'SBRL', 'CORELS']
names = [n.strip() for n in labels]
title = 'Weapon prediction (NYCLU stop-and-frisk dataset)'

x = tb.tabarray(SVfile='../eval/weapon_compare.csv')
y = tb.tabarray(SVfile='../eval/weapon_sparsity_jmlr-CORELS.csv')
z = tb.tabarray(SVfile='../eval/weapon_sparsity_jmlr-sbrl.csv')
x = x.rowstack(z[(z['eta'] == 3) & (z['lambda'] == 9)])
x = x.rowstack(y[y['R'] == 0.01])

ax1 = pylab.subplot2grid((40, 40), (3, 0), colspan=20, rowspan=30)
ax2 = pylab.subplot2grid((40, 40), (3, 21), colspan=20, rowspan=30)
#ax1 = pylab.subplot2grid((40, 40), (2, 5), colspan=35, rowspan=18)
#ax2 = pylab.subplot2grid((40, 40), (18, 5), colspan=35, rowspan=18)

fs=14
(nfolds, nmethods) = (10, len(labels))

color_vec = ['r', 'orange', 'y', 'g', 'c', 'b', 'purple', 'violet', 'm', 'gray']
ii = x[x['Method'] == 'GLM']['TPR'].argsort()[::-1]

m = x[['Method', 'TPR', 'FPR']].aggregate(On='Method', AggFunc=np.mean)
s = x[['Method', 'TPR', 'FPR']].aggregate(On='Method', AggFunc=np.std)

ind = [(m['Method'] == n).nonzero()[0][0] for n in names]
m = m[ind]
s = s[ind]

for (ax, pr) in [(ax1, 'TPR'), (ax2, 'FPR')]:
    ax.errorbar(range(nmethods), m[pr], s[pr], fmt=None, ecolor='k', elinewidth=2, capsize=8, capthick=2)
    for (i, color) in zip(ii, color_vec):
        y = x[x['Fold'] == ('weapon_%d' % i)][pr]
        ax.plot(range(nmethods), y, 'D', color=color, markeredgewidth=0, markersize=4.5)
    ax.plot(range(nmethods), m[pr], 's', markeredgecolor='k', markerfacecolor='white', markeredgewidth=2, markersize=7)
    ax.xaxis.set_ticks(range(nmethods))
    ax.xaxis.set_ticklabels(labels, fontsize=fs, rotation=40)
    ax.set_xlim(-0.5, nmethods - 0.5)

ax1.yaxis.set_label_text('TPR', fontsize=fs)
yt = np.arange(0.4, 0.75, 0.1)
ax1.yaxis.set_ticks(yt)
ax1.yaxis.set_ticklabels(yt, fontsize=fs)

ax2.yaxis.set_label_text('FPR', fontsize=fs)
yt = np.arange(0.1, 0.24, 0.04)
ax2.yaxis.set_ticks(yt)
ax2.yaxis.set_ticklabels(yt, fontsize=fs)

#pylab.axis(a)
pylab.tight_layout()
pylab.suptitle(title, fontsize=fs)

pylab.savefig('../figs/compare-weapon.pdf')
