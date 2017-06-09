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

fig = plt.figure(2, figsize=(8, 3.5))
plt.clf()
ax = plt.subplot2grid((20, 1), (0, 1), colspan=1, rowspan=18)

m.sort(order=['Method', 'C', 'cp', 'R'])
s.sort(order=['Method', 'C', 'cp', 'R'])

ind = [-4, -3, -2] + [-1] + [5, 6, 7, 9] #+ [0, 1, 4]
m = m[ind].copy()
s = s[ind].copy()

data = zip(m['Method'], m['leaves'], m['accuracy'], s['leaves'], s['accuracy'], m['train_accuracy'], s['train_accuracy'])

ms = 5
cdict = {'CORELS': 'k', 'C4.5': 'k', 'CART': 'k', 'RIPPER': 'k', 'SBRL': 'k'}
mdict = {'CORELS': 's', 'C4.5': 'o', 'CART': 'd', 'RIPPER': '^', 'SBRL': 'v'}
msdict = {'CORELS': 10, 'C4.5': ms, 'CART': ms, 'RIPPER': ms*2, 'SBRL': ms*2}
mfcdict = {'CORELS': 'm', 'C4.5': 'c', 'CART': 'white', 'RIPPER': 'gray', 'SBRL': 'k'}
msvec = np.array([6, 8, 10, 6, 1, 3, 5, 9, 4, 8, 12]) + 6
mew = 1

i = 0
for (method, xx, yy, w, h, ty, th) in data:
    mfc = mfcdict[method]
    if (method == 'C4.5'):
        w = 0
    plt.plot(xx, yy, color=cdict[method], linewidth=0, marker=mdict[method], markersize=msvec[i], markeredgewidth=mew, markeredgecolor=cdict[method], markerfacecolor=mfc)
    i += 1

i = 0
for (method, xx, yy, w, h, ty, th) in data:
    mfc = mfcdict[method]
    if log2:
        xx = np.log2(xx)
    plt.errorbar(xx, yy, xerr=w, yerr=h, color=cdict[method], linewidth=0, marker=mdict[method], markersize=msvec[i], markeredgewidth=mew, markeredgecolor=cdict[method], markerfacecolor=mfc, capsize=0, elinewidth=1)
    i += 1

if (with_training):
    i = 0
    for (method, xx, yy, w, h, ty, th) in data:
        print method, xx, yy, ty
        if (i == 8):
            mfc = 'None'
        else:
            mfc = mfcdict[method]
        if (ty):
            if log2:
                xx = np.log2(xx)
            if (np.abs(ty - yy) > 0.01):
                plt.plot([xx, xx], [ty, yy+h], ':', color=cdict[method], linewidth=2)
            plt.plot(xx, ty, 'o', markersize=5, color='white', markeredgewidth=mew, markeredgecolor='k')
        i += 1

legend = []
for r in m:
    descr = r['Method']
    if r['C']:
        descr += ' (%s)' % ('%1.3f' % r['C']).strip('0')
    elif r['cp']:
        descr += ' (%s)' % ('%1.3f' % r['cp']).strip('0').replace('.01', '.01, .03')
    elif r['R']:
        descr += ' (%s)' % ('%1.4f' % r['R']).strip('0')
    legend += [descr]

fs = 14
plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)
plt.ylabel('Accuracy', fontsize=fs)
plt.legend(legend, loc='lower right', fontsize=fs-3, numpoints=1, ncol=2, labelspacing=0.5, borderpad=0, columnspacing=0.1, markerscale=0.8, frameon=False)
plt.title('Weapon prediction (NYCLU stop-and-frisk dataset)', fontsize=fs)

if log2:
    ax.set_xlim(0, 11)
    plt.xlabel('log2(Model size)', fontsize=fs)
else:
    ax.set_xlim(0, 56)
    plt.xlabel('Model size', fontsize=fs)

if (with_training):
    plt.xticks(range(0, 56, 5), fontsize=fs)
    plt.yticks(np.arange(0.63, 0.76, 0.02), fontsize=fs)
    ax.set_ylim(0.64, 0.75)
    plt.show()
    plt.savefig('../figs/frisk-sparsity-training.pdf')
else:
    ax.set_ylim(0.64, 0.74)
    plt.show()
    plt.savefig('../figs/frisk-sparsity.pdf')
