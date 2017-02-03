import numpy as np
import pylab


names = 'GLM, SVM, AdaBoost, CART, C4.5, RF, RIPPER'.split(', ') + ['SBRL', 'BBRL']

x = open('../compare/compas.txt', 'rU').read().strip().split('\n')

sbrl = [line.strip().split()[-1] for line in x if line.startswith('test accuracy')]
sbrl = np.array(sbrl)

other = [line.strip().split() for line in x if line.startswith('0')]
other = np.array(other)

bbrl = [line for line in x if line.startswith('Test accuracies')][0]
bbrl = np.array(bbrl.strip().split('[')[1].split(']')[0].split(','))

y = np.cast[float](np.vstack([other.T, sbrl, bbrl]).T)

pylab.ion()
pylab.figure(1, figsize=(7, 5))
pylab.clf()
pylab.subplot2grid((10, 20), (0, 1), colspan=19, rowspan=9)

(nfolds, nmethods) = y.shape

color_vec = ['r', 'orange', 'y', 'g', 'c', 'b', 'purple', 'violet', 'm', 'gray']
ii = y[:,-1].argsort()[::-1]

pylab.errorbar(range(nmethods), y.mean(axis=0), y.std(axis=0), fmt=None, ecolor='k', elinewidth=2, capsize=10, capthick=2)

for (i, color) in zip(ii, color_vec):
    pylab.plot(range(nmethods), y[i, :], 'D', color=color, markeredgewidth=0, markersize=8)

pylab.plot(range(nmethods), y.mean(axis=0), 's', color='white', markeredgewidth=2, markersize=8)

pylab.xticks(range(n), names, fontsize=15, rotation=40)
pylab.yticks(fontsize=16)
pylab.ylabel('accuracy\n', fontsize=16)

a = list(pylab.axis())
a[0] -= 1
a[1] += 1
pylab.axis(a)

pylab.savefig('../figs/compare-compas.pdf')
