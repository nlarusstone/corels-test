import matplotlib.patches as mp
import matplotlib.pyplot as plt
import numpy as np
import tabular as tb


plt.ion()

z = tb.tabarray(SVfile='../eval/compas_sparsity.csv')
y = tb.tabarray(SVfile='../eval/compas_sparsity-CORELS.csv', names=z.dtype.names)

x = z[z['Method'] != 'CORELS'].rowstack(y[y['Method'] == 'CORELS'])

m = x.aggregate(On=['Method', 'C', 'cp', 'R'], AggFuncDict={'accuracy': np.mean, 'leaves': np.mean})
s = x.aggregate(On=['Method', 'C', 'cp', 'R'], AggFuncDict={'accuracy': np.std, 'leaves': np.std})

fig = plt.figure(1, figsize=(8, 3.5))
plt.clf()
ax = plt.subplot2grid((20, 1), (0, 1), colspan=1, rowspan=19)

#ax = fig.add_subplot(111)

#s['leaves'][s['leaves'] == 0.] = 0.1

m.sort(order=['Method', 'C', 'cp', 'R'])
s.sort(order=['Method', 'C', 'cp', 'R'])

m = m[m['Method'] == 'CORELS'].rowstack(m[m['Method'] != 'CORELS'])
s = s[s['Method'] == 'CORELS'].rowstack(s[s['Method'] != 'CORELS'])

data = zip(m['Method'], m['leaves'], m['accuracy'], s['leaves'], s['accuracy'])

#ells = [mp.Ellipse(xy=(xx, yy), width=(w * 2), height=(h * 2)) for (xx, yy, w, h) in data]

ms = 5
cdict = {'CORELS': 'r', 'C4.5': 'c', 'CART': 'gray', 'RIPPER': 'k', 'SBRL': 'purple'}
mdict = {'CORELS': 's', 'C4.5': '^', 'CART': 'd', 'RIPPER': 'v', 'SBRL': 'o'}
msdict = {'CORELS': 10, 'C4.5': ms, 'CART': ms, 'RIPPER': ms*2, 'SBRL': ms*2}
mfcdict = {'CORELS': 'coral', 'C4.5': 'paleturquoise', 'CART': 'white', 'RIPPER': 'lightgray', 'SBRL': 'plum'}
msvec = np.array([12, 10, 8, 12, 10, 8, 6, 4, 12, 10, 8, 6, 4, 10, 10])
mew = 2

i = 0
for (method, xx, yy, w, h) in data:
    if (i == 0):
        yy = 0.675589459085
    if (i == 8):
        mfc = 'None'
    else:
        mfc = mfcdict[method]
    if (w == 0):
        plt.plot(xx, yy, color=cdict[method], linewidth=0, marker=mdict[method], markersize=msvec[i], markeredgewidth=mew, markeredgecolor=cdict[method], markerfacecolor=mfc)
    else:
        plt.errorbar(xx, yy, xerr=w, color=cdict[method], linewidth=0, marker=mdict[method], markersize=msvec[i], markeredgewidth=mew, markeredgecolor=cdict[method], markerfacecolor=mfc, capsize=4, elinewidth=2)
    i += 1

fs = 14
plt.xticks(fontsize=fs)
plt.yticks(fontsize=fs)
plt.xlabel('Model size', fontsize=fs)
plt.ylabel('Accuracy', fontsize=fs)
plt.legend(legend, loc='lower right', fontsize=fs-3, numpoints=1, ncol=2)

ax.set_xlim(0, 25)
ax.set_ylim(0.635, 0.68)
plt.show()

plt.savefig('../figs/compas-sparsity.pdf')
