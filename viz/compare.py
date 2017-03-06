import numpy as np
import pylab

figure = True

if figure:
    pylab.ion()
    pylab.figure(1, figsize=(10, 3.1))
    pylab.clf()

for dataset in ['compas', 'weapon']:

    if (dataset == 'compas'):
        names = ['GLM', 'SVM', 'AdaBoost\n\n', 'CART', 'C4.5', 'RF', 'RIPPER\n', 'SBRL', 'CORELS']
        title = 'Recidivism prediction (ProPublica)'
        yticks = np.arange(0.63, 0.72, 0.02)
    elif (dataset == 'weapon'):
        names = ['GLM', 'SVM', 'AdaBoost\n\n', 'CART', 'C4.5', 'RF', 'SBRL', 'CORELS']
        title = 'Weapon prediction (NYCLU)'
        yticks = np.arange(0.62, 0.76, 0.03)

    x = open('../compare/%s.txt' % dataset, 'rU').read().strip().split('\n')

    sbrl = [line.strip().split()[3] for line in x if line.startswith('test accuracy')]
    sbrl = np.array(sbrl)

    other = [line.strip().split() for line in x if line.startswith('0')]
    other = np.array(other)

    corels = [line for line in x if line.startswith('Test accuracies')][0]
    corels = np.array(corels.strip().split('[')[1].split(']')[0].split(','))

    y = np.cast[float](np.vstack([other.T, sbrl, corels]).T)

    print '\n'.join(['%s & %2.1f $\\pm$ %2.1f' % (n.strip(), m, s) for (n, m, s) in zip(names, y.mean(axis=0) * 100, y.std(axis=0) * 100)])

    if figure:
        if dataset == 'compas':
            pylab.subplot2grid((10, 40), (0, 0), colspan=18, rowspan=8)
        elif dataset == 'weapon':
            pylab.subplot2grid((10, 40), (0, 21), colspan=18, rowspan=8)

        fs=14

        (nfolds, nmethods) = y.shape

        color_vec = ['r', 'orange', 'y', 'g', 'c', 'b', 'purple', 'violet', 'm', 'gray']
        ii = y[:,-1].argsort()[::-1]

        pylab.errorbar(range(nmethods), y.mean(axis=0), y.std(axis=0), fmt=None, ecolor='k', elinewidth=2, capsize=8, capthick=2)

        for (i, color) in zip(ii, color_vec):
            pylab.plot(range(nmethods), y[i, :], 'D', color=color, markeredgewidth=0, markersize=5)

        pylab.plot(range(nmethods), y.mean(axis=0), 's', color='white', markeredgewidth=2, markersize=7)

        pylab.xticks(range(nmethods), names, fontsize=fs, rotation=40)
        pylab.yticks(yticks, fontsize=fs)
        if dataset == 'compas':
            pylab.ylabel('Accuracy', fontsize=fs)

        a = list(pylab.axis())
        a[0] -= 1
        a[1] += 1
        #a[2] = 0.601
        #a[3] = 0.76
        pylab.axis(a)
        pylab.title(title, fontsize=fs)

    pylab.savefig('../figs/compare-compas-weapon.pdf')
