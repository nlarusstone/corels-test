"""
For JMLR.  Replaces KDD 2017 Figure 3.

"""
import matplotlib.patches as mp
import matplotlib.pyplot as plt
import numpy as np
import tabular as tb

# see:  http://phyletica.org/matplotlib-fonts/
plt.rcParams['pdf.fonttype'] = 42
plt.rcParams['ps.fonttype'] = 42

plt.ion()
       
z = tb.tabarray(SVfile='../eval/weapon_sparsity_jmlr.csv')
y = tb.tabarray(SVfile='../eval/weapon_sparsity_jmlr-CORELS.csv')
q = tb.tabarray(SVfile='../eval/weapon_sparsity_jmlr-sbrl.csv')

x = z.rowstack(y).rowstack(q)

m = x.aggregate(On=['Method', 'C', 'cp', 'R', 'eta', 'lambda'], AggFuncDict={'accuracy': np.mean, 'leaves': np.mean, 'train_accuracy': np.mean, 'TPR': np.mean, 'FPR': np.mean})
s = x.aggregate(On=['Method', 'C', 'cp', 'R', 'eta', 'lambda'], AggFuncDict={'accuracy': np.std, 'leaves': np.std, 'train_accuracy': np.std, 'TPR': np.std, 'FPR': np.std})

fig = plt.figure(2, figsize=(9, 4))
plt.clf()

m.sort(order=['Method', 'C', 'cp', 'R', 'eta', 'lambda'])
s.sort(order=['Method', 'C', 'cp', 'R', 'eta', 'lambda'])

ind = [-5, -4, -3] + [-2, -1] + [3, 4, 5, 7] + [0, 1, 2]
m = m[ind].copy()
s = s[ind].copy()

data = zip(m['Method'], m['leaves'], m['accuracy'], m['TPR'], m['FPR'], s['leaves'], s['accuracy'], m['train_accuracy'], s['train_accuracy'], s['TPR'], s['FPR'])

ms = 5
cdict = {'CORELS': 'k', 'C4.5': 'k', 'CART': 'k', 'RIPPER': 'k', 'SBRL': 'k'}
mdict = {'CORELS': 's', 'C4.5': 'o', 'CART': 'd', 'RIPPER': '^', 'SBRL': 'D'}
msdict = {'CORELS': 10, 'C4.5': ms, 'CART': ms, 'RIPPER': ms*2, 'SBRL': ms*2}
mfcdict = {'CORELS': 'red', 'C4.5': 'c', 'CART': 'b', 'RIPPER': 'gray', 'SBRL': 'darkred'}
msvec = np.array([3, 5, 7, 3, 8, 1, 3, 5, 9, 0, 2, 4]) + 6
mew = 1

fs = 14
ax1 = plt.subplot2grid((20, 60), (0, 1), colspan=44, rowspan=18)
plt.xticks(fontsize=fs)
plt.yticks(np.arange(0, 0.71, 0.1), fontsize=fs)
plt.xlabel('                          Model size', fontsize=fs)
plt.ylabel('FPR (solid)       TPR (open)', fontsize=fs)
ax1.set_xlim(0, 56)
ax1.set_ylim(0, 0.7)

ax2 = plt.subplot2grid((20, 60), (0, 46), colspan=14, rowspan=18)
plt.xticks([400, 550, 700], fontsize=fs)
plt.yticks(np.arange(0, 0.71, 0.1), ())
#plt.ylabel('Accuracy', fontsize=fs)
ax2.set_xlim(320, 770)
ax2.set_ylim(0, 0.7)

i = 0
for (method, xx, yy, tpr, fpr, w, h, ty, th, tpre, fpre) in data:
    print (method, xx, yy, w, h, ty, th)
    mfc = mfcdict[method]
    if (method == 'C4.5'):
        w = 0
        ax = ax2
    else:
        ax = ax1
    ax.plot(xx, tpr, linewidth=0, marker=mdict[method], markersize=msvec[i], markeredgewidth=mew*2, markeredgecolor=mfc, markerfacecolor='white')
    i += 1

legend = []
for r in m[:-3]:
    descr = r['Method']
    if r['cp']:
        descr += ' (%s)' % ('%1.3f' % r['cp']).strip('0').replace('.01', '.01, .03')
    elif r['R']:
        descr += ' (%s)' % ('%1.4f' % r['R']).strip('0')
    elif r['eta']:
        descr += ' (%d, %d, %d)' % (r['eta'], r['lambda'], r['i'])
    legend += [descr]
ax1.legend(legend, loc=(0.43, 0.1), fontsize=fs-3.6, numpoints=1, ncol=1, labelspacing=0.5, borderpad=0.5, columnspacing=0., markerscale=0.8, frameon=False)

legend = []
for r in m[-3:]:
    descr = r['Method']
    descr += ' (%s)' % ('%1.5f' % r['C']).strip('0')
    legend += [descr]
#ax2.legend(legend, loc=(-1.55, 0.735), fontsize=fs-3.6, numpoints=1, ncol=1, labelspacing=0.5, borderpad=0, markerscale=0.8, frameon=False)
ax2.legend(legend, loc='center', fontsize=fs-3.6, numpoints=1, ncol=1, labelspacing=0.5, borderpad=0.5, markerscale=0.8, frameon=False)

i = 0
for (method, xx, yy, tpr, fpr, w, h, ty, th, tpre, fpre) in data:
    mfc = mfcdict[method]
    if (method == 'C4.5'):
        ax = ax2
    else:
        ax = ax1
    ax.errorbar(xx, tpr, xerr=w, yerr=tpre, color=cdict[method], linewidth=0, marker=mdict[method], markersize=msvec[i], markeredgewidth=mew*2, markeredgecolor=mfc, markerfacecolor='white', capsize=0, elinewidth=1)
    i += 1

####

i = 0
for (method, xx, yy, tpr, fpr, w, h, ty, th, tpre, fpre) in data:
    print (method, xx, yy, w, h, ty, th)
    mfc = mfcdict[method]
    if (method == 'C4.5'):
        w = 0
        ax = ax2
    else:
        ax = ax1
    ax.errorbar(xx, fpr, xerr=w, yerr=fpre, color=cdict[method], linewidth=0, marker=mdict[method], markersize=msvec[i], markeredgewidth=1,  markerfacecolor=mfc, capsize=0, elinewidth=1)
    i += 1


plt.suptitle('Weapon prediction (NYCLU stop-and-frisk dataset)', fontsize=fs)
plt.show()
plt.savefig('../figs/weapon-sparsity-jmlr.pdf')
