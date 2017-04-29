"""
For KDD 2017 Figure 3.

"""
import matplotlib.patches as mp
import matplotlib.pyplot as plt
import numpy as np
import tabular as tb

with_training = True
log2 = False

plt.ion()

z = tb.tabarray(SVfile='../eval/frisk_sparsity.csv')
b = tb.tabarray(SVfile='../eval/frisk_sparsity-sbrl.csv', names=z.dtype.names, namesinheader=False)
y = tb.tabarray(SVfile='../eval/frisk_sparsity-CORELS.csv', names=z.dtype.names, namesinheader=False)

x = z[(z['Method'] != 'CORELS') & (z['Method'] != 'SBRL')].rowstack(b).rowstack(y)

m = x.aggregate(On=['Method', 'C', 'cp', 'R'], AggFuncDict={'accuracy': np.mean, 'leaves': np.mean, 'train_accuracy': np.mean})
s = x.aggregate(On=['Method', 'C', 'cp', 'R'], AggFuncDict={'accuracy': np.std, 'leaves': np.std, 'train_accuracy': np.std})

#c45 = z[z['Method'] == 'C4.5']
#cm = c45.aggregate(On=['Method', 'C', 'cp', 'R'], AggFuncDict={'accuracy': np.mean, 'leaves': np.mean, 'train_accuracy': np.mean})
#cs = c45.aggregate(On=['Method', 'C', 'cp', 'R'], AggFuncDict={'accuracy': np.std, 'leaves': np.std, 'train_accuracy': np.std})

fig = plt.figure(2, figsize=(8, 3.6))
plt.clf()
#ax = plt.subplot2grid((20, 1), (0, 1), colspan=1, rowspan=18)

m.sort(order=['Method', 'C', 'cp', 'R'])
s.sort(order=['Method', 'C', 'cp', 'R'])

ind = [-4, -3, -2] + [-1] + [5, 6, 7, 9] + [0, 1, 4]
m = m[ind].copy()
s = s[ind].copy()

data = zip(m['Method'], m['leaves'], m['accuracy'], s['leaves'], s['accuracy'], m['train_accuracy'], s['train_accuracy'])

ms = 5
cdict = {'CORELS': 'r', 'C4.5': 'c', 'CART': 'gray', 'RIPPER': 'k', 'SBRL': 'purple'}
mdict = {'CORELS': 's', 'C4.5': '^', 'CART': 'd', 'RIPPER': 'v', 'SBRL': 'o'}
msdict = {'CORELS': 10, 'C4.5': ms, 'CART': ms, 'RIPPER': ms*2, 'SBRL': ms*2}
mfcdict = {'CORELS': 'coral', 'C4.5': 'paleturquoise', 'CART': 'white', 'RIPPER': 'lightgray', 'SBRL': 'plum'}
msvec = np.array([11, 9, 8, 10, 10, 9, 8, 7, 8, 6, 4]) * 2
mew = 2

ax1 = plt.subplot2grid((20, 60), (0, 1), colspan=44, rowspan=18)
plt.xticks(fontsize=fs)
ytplt.yticks(fontsize=fs)
plt.xlabel('Model size', fontsize=fs)
plt.ylabel('Accuracy', fontsize=fs)
ax1.set_xlim(0, 56)
#ax2.set_ylim(0.64, 0.74)
ax1.set_ylim(0.64, 0.92)

ax2 = plt.subplot2grid((20, 60), (0, 50), colspan=10, rowspan=18)
plt.xticks([1100, 1400], fontsize=fs)
plt.yticks(fontsize=fs)
#plt.ylabel('Accuracy', fontsize=fs)
ax2.set_xlim(1000, 1500)
ax2.set_ylim(0.64, 0.92)

i = 0
for (method, xx, yy, w, h, ty, th) in data:
    mfc = mfcdict[method]
    if (method == 'C4.5'):
        w = 0
        ax = ax2
    else:
        ax = ax1
    if (w == 0):
        if log2:
            xx = np.log2(xx)
        ax.plot(xx, yy, color=cdict[method], linewidth=0, marker=mdict[method], markersize=msvec[i], markeredgewidth=mew, markeredgecolor=cdict[method], markerfacecolor=mfc)
        if (ax == ax2):
            ax1.plot(xx, yy, color=cdict[method], linewidth=0, marker=mdict[method], markersize=msvec[i], markeredgewidth=mew, markeredgecolor=cdict[method], markerfacecolor=mfc)
    else:
        if log2:
            xerr = np.array([[np.log2(xx) - np.log2(xx-w)], [np.log2(xx+w) - np.log2(xx)]])
            xx = np.log2
        else:
            xerr = w
        ax.errorbar(xx, yy, xerr=xerr, color=cdict[method], linewidth=0, marker=mdict[method], markersize=msvec[i], markeredgewidth=mew, markeredgecolor=cdict[method], markerfacecolor=mfc, capsize=4, elinewidth=2)
    i += 1

i = 0
for (method, xx, yy, w, h, ty, th) in data:
    mfc = mfcdict[method]
    if (method == 'C4.5'):
        ax = ax2
    else:
        ax = ax1
    if log2:
        xx = np.log2(xx)
    ax.errorbar(xx, yy, yerr=h, color=cdict[method], linewidth=0, marker=mdict[method], markersize=msvec[i], markeredgewidth=mew, markeredgecolor=cdict[method], markerfacecolor=mfc, capsize=4, elinewidth=2)
    i += 1

if (with_training):
    i = 0
    for (method, xx, yy, w, h, ty, th) in data:
        print method, xx, yy, ty
        if (method == 'C4.5'):
            ax = ax2
        else:
            ax = ax1
        if (i == 8):
            mfc = 'None'
        else:
            mfc = mfcdict[method]
        if (ty):
            if log2:
                xx = np.log2(xx)
            if (np.abs(ty - yy) > 0.01):
                ax.plot([xx, xx], [ty, yy+h], ':', color=cdict[method], linewidth=2)
            ax.plot(xx, ty, 'o', markersize=5, color='white', markeredgewidth=2, markeredgecolor='k')
        i += 1

legend = []
for r in m:
    descr = r['Method']
    if r['C']:
        descr += ' (%s)' % ('%1.3f' % r['C']).strip('0')
    elif r['cp']:
        descr += ' (%s)' % ('%1.3f' % r['cp']).strip('0')
    elif r['R']:
        descr += ' (%s)' % ('%1.4f' % r['R']).strip('0')
    legend += [descr]

fs = 14

ax1.legend(legend, loc='upper left', fontsize=fs-2.5, numpoints=1, ncol=3, labelspacing=0.5, borderpad=.5, columnspacing=0.1, markerscale=0.6)

plt.suptitle('Weapon prediction (NYCLU stop-and-frisk dataset)', fontsize=fs)

if (with_training):
    plt.show()
    plt.savefig('../figs/frisk-sparsity-training-c45.pdf')
else:
    plt.show()
    plt.savefig('../figs/frisk-sparsity-c45.pdf')
