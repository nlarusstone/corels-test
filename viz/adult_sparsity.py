import matplotlib.patches as mp
import matplotlib.pyplot as plt
import numpy as np
import tabular as tb

with_training = True

plt.ion()

z = tb.tabarray(SVfile='../eval/adult_sparsity.csv')
b = tb.tabarray(SVfile='../eval/adult_sparsity-sbrl.csv', names=list(z.dtype.names) + ['nclauses'], namesinheader=False,
                linefixer=lambda x: x + ',2')
b1 = tb.tabarray(SVfile='../eval/1adult_sparsity-sbrl.csv', names=list(z.dtype.names) + ['nclauses'], namesinheader=False,
                 linefixer=lambda x: x + ',1')
#y = tb.tabarray(SVfile='../eval/adult_sparsity-CORELS.csv', names=z.dtype.names, namesinheader=False)

x = z[(z['Method'] != 'CORELS') & (z['Method'] != 'SBRL')].rowstack(b).rowstack(b1)#.rowstack(y)

m = x.aggregate(On=['Method', 'C', 'cp', 'R', 'nclauses'], AggFuncDict={'accuracy': np.mean, 'leaves': np.mean, 'train_accuracy': np.mean})
s = x.aggregate(On=['Method', 'C', 'cp', 'R', 'nclauses'], AggFuncDict={'accuracy': np.std, 'leaves': np.std, 'train_accuracy': np.std})

fig = plt.figure(1, figsize=(8, 3.5))
plt.clf()
ax = plt.subplot2grid((20, 1), (0, 1), colspan=1, rowspan=19)

m.sort(order=['Method', 'C', 'cp', 'R'])
s.sort(order=['Method', 'C', 'cp', 'R'])

ind = range(10, 13) + range(5, 10)[1:] + range(5)[:-1]
m = m[ind].copy()
s = s[ind].copy()

data = zip(m['Method'], m['leaves'], m['accuracy'],  s['leaves'], s['accuracy'], m['train_accuracy'], s['train_accuracy'])

ms = 5
cdict = {'CORELS': 'r', 'C4.5': 'c', 'CART': 'gray', 'RIPPER': 'mediumblue', 'SBRL': 'purple'}
mdict = {'CORELS': 's', 'C4.5': '^', 'CART': 'd', 'RIPPER': 'v', 'SBRL': 'o'}
msdict = {'CORELS': 10, 'C4.5': ms, 'CART': ms, 'RIPPER': ms*2, 'SBRL': ms*2}
mfcdict = {'CORELS': 'coral', 'C4.5': 'paleturquoise', 'CART': 'white', 'RIPPER': 'skyblue', 'SBRL': 'plum'}
msvec = np.array([11, 9, 8, 10, 10, 10, 9, 8, 7, 7, 8, 7, 6, 5, 4]) * 2
msvec = np.array([9, 7, 9, 10, 9, 8, 7, 7, 6, 5, 4]) * 2
mew = 2

plt.errorbar(5, 0.8376, yerr=0.0045, color='r', linewidth=0, marker='s', markersize=20, markeredgewidth=2, markeredgecolor='r', markerfacecolor='coral', capsize=4, elinewidth=2)

i = 0
for (method, xx, yy, w, h, ty, th) in data:
    mfc = mfcdict[method]
    if (w == 0):
        plt.plot(xx, yy, color=cdict[method], linewidth=0, marker=mdict[method], markersize=msvec[i], markeredgewidth=mew, markeredgecolor=cdict[method], markerfacecolor=mfc)
    else:
        plt.errorbar(xx, yy, xerr=w, color=cdict[method], linewidth=0, marker=mdict[method], markersize=msvec[i], markeredgewidth=mew, markeredgecolor=cdict[method], markerfacecolor=mfc, capsize=4, elinewidth=2)
    i += 1

i = 0
for (method, xx, yy, w, h, ty, th) in data:
    mfc = mfcdict[method]
    plt.errorbar(xx, yy, yerr=h, color=cdict[method], linewidth=0, marker=mdict[method], markersize=msvec[i], markeredgewidth=mew, markeredgecolor=cdict[method], markerfacecolor=mfc, capsize=4, elinewidth=2)
    i += 1


if (with_training):
    i = 0
    for (method, xx, yy, w, h, ty, th) in data:
        if (i == 8):
            mfc = 'None'
        else:
            mfc = mfcdict[method]
        if ty:
            plt.plot(xx, ty, 'o', markersize=5, color='white', markeredgewidth=2, markeredgecolor='k')
        i += 1

legend = ['CORELS (.01)']
for r in m:
    descr = r['Method']
    if r['C']:
        descr += ' (%s)' % ('%1.5f' % r['C']).strip('0')
    elif r['cp']:
        descr += ' (%s)' % ('%1.5f' % r['cp']).strip('0')
    elif r['R']:
        descr += ' (%s)' % ('%1.5f' % r['R']).strip('0')
    elif r['nclauses']:
        if (r['nclauses'] == 1):
            descr += ' (%d clause)' % r['nclauses']
        else:
            descr += ' (%d clauses)' % r['nclauses']
    legend += [descr]

fs = 14
plt.xticks(fontsize=fs)
plt.yticks(np.arange(0.80, 0.87, 0.01), fontsize=fs)
plt.xlabel('Model size', fontsize=fs)
plt.ylabel('Accuracy', fontsize=fs)
plt.legend(legend, loc='lower left', fontsize=fs-3, numpoints=1, ncol=3, labelspacing=0.5, borderpad=.5, columnspacing=0.1, markerscale=0.6)
plt.title('Income prediction (adult dataset)', fontsize=fs)

ax.set_xlim(0, 35)

if (with_training):
    ax.set_ylim(0.8, 0.852)
    plt.show()
    plt.savefig('../figs/adult-sparsity-training.pdf')
else:
    ax.set_ylim(0.81, 0.86)
    plt.show()
    plt.savefig('../figs/adult-sparsity.pdf')
