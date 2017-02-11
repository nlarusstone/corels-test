import numpy as np
import pylab

figure = False


# COMPAS
names = ['GLM', 'SVM', 'AdaBoost\n\n', 'CART', 'C4.5', 'RF', 'RIPPER\n', 'SBRL', 'CORELS']
x = open('../compare/compas.txt', 'rU').read().strip().split('\n')

# weapon
names = ['GLM', 'SVM', 'AdaBoost\n\n', 'CART', 'C4.5', 'RF', 'SBRL', 'CORELS']
x = open('../compare/weapon.txt', 'rU').read().strip().split('\n')

sbrl = [line.strip().split()[3] for line in x if line.startswith('test accuracy')]
sbrl = np.array(sbrl)

other = [line.strip().split() for line in x if line.startswith('0')]
other = np.array(other)

corels = [line for line in x if line.startswith('Test accuracies')][0]
corels = np.array(corels.strip().split('[')[1].split(']')[0].split(','))

y = np.cast[float](np.vstack([other.T, sbrl, corels]).T)

print '\n'.join(['%s & %2.1f $\\pm$ %2.1f' % (n.strip(), m, s) for (n, m, s) in zip(names, y.mean(axis=0) * 100, y.std(axis=0) * 100)])

if figure:
    pylab.ion()
    pylab.figure(1, figsize=(7, 5))
    pylab.clf()
    pylab.subplot2grid((10, 20), (0, 1), colspan=19, rowspan=9)

    fs=16

    (nfolds, nmethods) = y.shape

    color_vec = ['r', 'orange', 'y', 'g', 'c', 'b', 'purple', 'violet', 'm', 'gray']
    ii = y[:,-1].argsort()[::-1]

    pylab.errorbar(range(nmethods), y.mean(axis=0), y.std(axis=0), fmt=None, ecolor='k', elinewidth=2, capsize=10, capthick=2)

    for (i, color) in zip(ii, color_vec):
        pylab.plot(range(nmethods), y[i, :], 'D', color=color, markeredgewidth=0, markersize=8)

    pylab.plot(range(nmethods), y.mean(axis=0), 's', color='white', markeredgewidth=2, markersize=8)

    pylab.xticks(range(nmethods), names, fontsize=fs, rotation=40)
    pylab.yticks(fontsize=fs)
    pylab.ylabel('accuracy\n', fontsize=fs)

    a = list(pylab.axis())
    a[0] -= 1
    a[1] += 1
    pylab.axis(a)

    pylab.savefig('../paper/figs/compare-compas.pdf')
