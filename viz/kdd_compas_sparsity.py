"""
For KDD 2017 Figure 3.

"""
import matplotlib.patches as mp
import matplotlib.pyplot as plt
import numpy as np
import tabular as tb

with_training = True

plt.ion()

z = tb.tabarray(SVfile='../eval/compas_sparsity-train.csv')
b = tb.tabarray(SVfile='../eval/compas_sparsity-sbrl.csv', names=z.dtype.names, namesinheader=False)
y = tb.tabarray(SVfile='../eval/compas_sparsity-CORELS.csv', names=z.dtype.names, namesinheader=False)

x = z[(z['Method'] != 'CORELS') & (z['Method'] != 'SBRL')].rowstack(b).rowstack(y)

m = x.aggregate(On=['Method', 'C', 'cp', 'R'], AggFuncDict={'accuracy': np.mean, 'leaves': np.mean, 'train_accuracy': np.mean})
s = x.aggregate(On=['Method', 'C', 'cp', 'R'], AggFuncDict={'accuracy': np.std, 'leaves': np.std, 'train_accuracy': np.std})

fig = plt.figure(1, figsize=(8, 3.5))
plt.clf()
ax = plt.subplot2grid((20, 1), (0, 1), colspan=1, rowspan=19)

m.sort(order=['Method', 'C', 'cp', 'R'])
s.sort(order=['Method', 'C', 'cp', 'R'])

ind = range(10, 15) + range(5, 10) + range(4)
m = m[ind].copy()
s = s[ind].copy()

data = zip(m['Method'], m['leaves'], m['accuracy'],  s['leaves'], s['accuracy'], m['train_accuracy'], s['train_accuracy'])

ms = 5
cdict = {'CORELS': 'k', 'C4.5': 'k', 'CART': 'k', 'RIPPER': 'k', 'SBRL': 'k'}
mdict = {'CORELS': 's', 'C4.5': 'o', 'CART': 'd', 'RIPPER': '^', 'SBRL': 'v'}
msdict = {'CORELS': 10, 'C4.5': ms, 'CART': ms, 'RIPPER': ms*2, 'SBRL': ms*2}
mfcdict = {'CORELS': 'm', 'C4.5': 'c', 'CART': 'white', 'RIPPER': 'gray', 'SBRL': 'k'}
#msvec = np.array([11, 9, 8, 10, 10, 10, 9, 8, 7, 7, 8, 7, 6, 5, 4]) * 2
msvec = np.array([4, 7, 10, 6, 6, 1, 3, 5, 7, 9, 3, 5, 7, 9, 11]) + 6
mew = 1

i = 0
for (method, xx, yy, w, h, ty, th) in data:
    mfc = mfcdict[method]
    plt.plot(xx, yy, color=cdict[method], linewidth=0, marker=mdict[method], markersize=msvec[i], markeredgewidth=mew, markeredgecolor=cdict[method], markerfacecolor=mfc)
    i += 1

i = 0
for (method, xx, yy, w, h, ty, th) in data:
    mfc = mfcdict[method]
    plt.errorbar(xx, yy, xerr=w, yerr=h, color=cdict[method], linewidth=0, marker=mdict[method], markersize=msvec[i], markeredgewidth=mew, markeredgecolor=cdict[method], markerfacecolor=mfc, capsize=0, elinewidth=1)
    i += 1

if (with_training):
    i = 0
    for (method, xx, yy, w, h, ty, th) in data:
        if (i == 8):
            mfc = 'None'
        else:
            mfc = mfcdict[method]
        if ty:
            plt.plot(xx, ty, 'o', markersize=4, color='white', markeredgewidth=mew, markeredgecolor='k')
        i += 1

legend = []
for r in m:
    descr = r['Method']
    if r['C']:
        descr += ' (%s)' % ('%1.3f' % r['C']).strip('0')
    elif r['cp']:
        descr += ' (%s)' % ('%1.3f' % r['cp']).strip('0')
    elif r['R']:
        descr += ' (%s)' % ('%1.3f' % r['R']).strip('0')
    legend += [descr]

fs = 14
plt.xticks(fontsize=fs)
plt.yticks(np.arange(0.60, 0.71, 0.02), fontsize=fs)
plt.xlabel('Model size', fontsize=fs)
plt.ylabel('Accuracy', fontsize=fs)
plt.legend(legend, loc='lower right', fontsize=fs-3, numpoints=1, ncol=3, labelspacing=0.5, borderpad=0, columnspacing=0.1, markerscale=0.8, frameon=False)
plt.title('Two-year recidivism prediction (ProPublica dataset)', fontsize=fs)

ax.set_xlim(0, 31)

if (with_training):
    ax.set_ylim(0.615, 0.7)
    plt.show()
    plt.savefig('../figs/compas-sparsity-training.pdf')
else:
    ax.set_ylim(0.61, 0.7)
    plt.show()
    plt.savefig('../figs/compas-sparsity.pdf')
