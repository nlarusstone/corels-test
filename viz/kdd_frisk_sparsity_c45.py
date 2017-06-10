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
z = z[z['Method'] != 'C4.5']
q = tb.tabarray(SVfile='../eval/frisk_sparsity-c45.csv')
z = z.rowstack(q)
b = tb.tabarray(SVfile='../eval/frisk_sparsity-sbrl.csv', names=z.dtype.names, namesinheader=False)
y = tb.tabarray(SVfile='../eval/frisk_sparsity-CORELS.csv', names=z.dtype.names, namesinheader=False)
p = tb.tabarray(SVfile='../eval/frisk_sparsity-sbrl-eta=500-lambda=5.csv', names=list(z.dtype.names) + ['eta', 'lambda'], namesinheader=False)

x = z[(z['Method'] != 'CORELS') & (z['Method'] != 'SBRL')].rowstack(b).rowstack(y).rowstack(p)
x['eta'][(x['Method'] == 'SBRL') & (x['eta'] == 0)] = 3
x['lambda'][(x['Method'] == 'SBRL') & (x['lambda'] == 0)] = 9

m = x.aggregate(On=['Method', 'C', 'cp', 'R', 'eta', 'lambda'], AggFuncDict={'accuracy': np.mean, 'leaves': np.mean, 'train_accuracy': np.mean})
s = x.aggregate(On=['Method', 'C', 'cp', 'R', 'eta', 'lambda'], AggFuncDict={'accuracy': np.std, 'leaves': np.std, 'train_accuracy': np.std})

fig = plt.figure(2, figsize=(8, 3))
plt.clf()

m.sort(order=['Method', 'C', 'cp', 'R', 'eta', 'lambda'])
s.sort(order=['Method', 'C', 'cp', 'R', 'eta', 'lambda'])

ind = [-5, -4, -3] + [-2, -1] + [4, 5, 6, 8] + [0, 1, 3]
m = m[ind].copy()
s = s[ind].copy()

data = zip(m['Method'], m['leaves'], m['accuracy'], s['leaves'], s['accuracy'], m['train_accuracy'], s['train_accuracy'])

ms = 5
cdict = {'CORELS': 'k', 'C4.5': 'k', 'CART': 'k', 'RIPPER': 'k', 'SBRL': 'k'}
mdict = {'CORELS': 's', 'C4.5': 'o', 'CART': 'd', 'RIPPER': '^', 'SBRL': 'D'}
msdict = {'CORELS': 10, 'C4.5': ms, 'CART': ms, 'RIPPER': ms*2, 'SBRL': ms*2}
mfcdict = {'CORELS': 'm', 'C4.5': 'c', 'CART': 'white', 'RIPPER': 'gray', 'SBRL': 'k'}
msvec = np.array([3, 5, 7, 3, 8, 1, 3, 5, 9, 0, 2, 4]) + 6
mew = 1

fs = 14
ax1 = plt.subplot2grid((20, 60), (0, 1), colspan=48, rowspan=18)
plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)
plt.xlabel('Model size', fontsize=fs)
plt.ylabel('Accuracy', fontsize=fs)
ax1.set_xlim(0, 56)
#ax2.set_ylim(0.64, 0.74)
ax1.set_ylim(0.64, 0.87)

ax2 = plt.subplot2grid((20, 60), (0, 50), colspan=10, rowspan=18)
plt.xticks([400, 700], fontsize=fs)
plt.yticks((), ())
#plt.ylabel('Accuracy', fontsize=fs)
ax2.set_xlim(320, 780)
ax2.set_ylim(0.64, 0.87)

i = 0
for (method, xx, yy, w, h, ty, th) in data:
    mfc = mfcdict[method]
    if (method == 'C4.5'):
        w = 0
        ax = ax2
    else:
        ax = ax1
    ax.plot(xx, yy, color=cdict[method], linewidth=0, marker=mdict[method], markersize=msvec[i], markeredgewidth=mew, markeredgecolor=cdict[method], markerfacecolor=mfc)
    i += 1

legend = []
for r in m[:-3]:
    descr = r['Method']
    if r['cp']:
        descr += ' (%s)' % ('%1.3f' % r['cp']).strip('0').replace('.01', '.01, .03')
    elif r['R']:
        descr += ' (%s)' % ('%1.4f' % r['R']).strip('0')
    elif r['eta']:
        if r['eta'] == 3:
            descr += ' (%d, %d, 1000)' % (r['eta'], r['lambda'])
        else:
            descr += ' (%d, %d, 10000)' % (r['eta'], r['lambda'])
    legend += [descr]
ax1.legend(legend, loc='upper left', fontsize=fs-3.6, numpoints=1, ncol=2, labelspacing=0.5, borderpad=0, columnspacing=0., markerscale=0.8, frameon=False)

legend = []
for r in m[-3:]:
    descr = r['Method']
    descr += ' (%s)' % ('%1.5f' % r['C']).strip('0')
    legend += [descr]
ax2.legend(legend, loc=(-1.55, 0.715), fontsize=fs-3.6, numpoints=1, ncol=1, labelspacing=0.5, borderpad=0, markerscale=0.8, frameon=False)

i = 0
for (method, xx, yy, w, h, ty, th) in data:
    mfc = mfcdict[method]
    if (method == 'C4.5'):
        ax = ax2
    else:
        ax = ax1
    if log2:
        xx = np.log2(xx)
    ax.errorbar(xx, yy, xerr=w, yerr=h, color=cdict[method], linewidth=0, marker=mdict[method], markersize=msvec[i], markeredgewidth=mew, markeredgecolor=cdict[method], markerfacecolor=mfc, capsize=0, elinewidth=1)
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
            ax.plot(xx, ty, 'o', markersize=5, color='white', markeredgewidth=mew, markeredgecolor='k')
        i += 1

plt.suptitle('Weapon prediction (NYCLU stop-and-frisk dataset)', fontsize=fs)

if (with_training):
    plt.show()
    plt.savefig('../figs/frisk-sparsity-training-c45.pdf')
else:
    plt.show()
    plt.savefig('../figs/frisk-sparsity-c45.pdf')
