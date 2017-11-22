"""
For KDD 2017 Figure 2.

"""
import numpy as np
import pylab

# see:  http://phyletica.org/matplotlib-fonts/
pylab.rcParams['pdf.fonttype'] = 42
pylab.rcParams['ps.fonttype'] = 42

figure = True
vertical = False

if figure:
    pylab.ion()
    if vertical:
        pylab.figure(1, figsize=(5, 6))
    else:
        pylab.figure(1, figsize=(9, 3))
    pylab.clf()

# see ../eval/eval_bias_ela.py
compas = np.array([0.68451519536903038, 0.65557163531114326, 0.65412445730824886, 0.66570188133140373, 0.64833574529667148, 0.678726483357453, 0.64544138929088279, 0.66956521739130437, 0.6768115942028986, 0.61884057971014494])

for dataset in ['compas', 'weapon']:

    if (dataset == 'compas'):
        names = ['GLM', 'SVM', 'AdaBoost\n\n', 'CART', 'C4.5', 'RF', 'RIPPER\n', 'SBRL', 'COMPAS', 'CORELS']
        title = 'Recidivism prediction (ProPublica)'
        yticks = np.arange(0.62, 0.74, 0.03)
    elif (dataset == 'weapon'):
        names = ['GLM', 'SVM', 'AdaBoost\n\n', 'CART', 'C4.5', 'RF', 'SBRL', 'CORELS']
        title = 'Weapon prediction (NYCLU)'
        #    a[2] = 0.755
        #    a[3] = 0.885
        yticks = np.arange(0.75, 0.89, 0.03)

    x = open('../compare/%s.txt' % dataset, 'rU').read().strip().split('\n')

    sbrl = [line.strip().split()[3] for line in x if line.startswith('test accuracy')]
    sbrl = np.array(sbrl)

    other = [line.strip().split() for line in x if line.startswith('0.')]
    other = np.array(other)

    corels = [line for line in x if line.startswith('Test accuracies')][0]
    corels = np.array(corels.strip().split('[')[1].split(']')[0].split(','))

    print other.shape
    print sbrl.shape
    if (dataset == 'compas'):
        y = np.cast[float](np.vstack([other.T, sbrl, compas, corels]).T)
    elif (dataset == 'weapon'):
        y = np.cast[float](np.vstack([other.T, sbrl, corels]).T)

    print '\n'.join(['%s & %2.1f $\\pm$ %2.1f' % (n.strip(), m, s) for (n, m, s) in zip(names, y.mean(axis=0) * 100, y.std(axis=0) * 100)])

    if figure:
        if not vertical:
            if dataset == 'compas':
                pylab.subplot2grid((10, 81), (0, 6), colspan=42, rowspan=8)
            elif dataset == 'weapon':
                pylab.subplot2grid((10, 81), (0, 48), colspan=36, rowspan=8)
        else:
            if dataset == 'compas':
                pylab.subplot2grid((40, 10), (0, 1), colspan=10, rowspan=15)
            elif dataset == 'weapon':
                pylab.subplot2grid((40, 10), (23, 1), colspan=10, rowspan=15)

        fs=14

        (nfolds, nmethods) = y.shape

        color_vec = ['r', 'orange', 'y', 'g', 'c', 'b', 'purple', 'violet', 'm', 'gray']
        ii = y[:,-1].argsort()[::-1]

        pylab.errorbar(range(nmethods), y.mean(axis=0), y.std(axis=0), fmt=None, ecolor='k', elinewidth=2, capsize=8, capthick=2)

        for (i, color) in zip(ii, color_vec):
            pylab.plot(range(nmethods), y[i, :], 'D', color=color, markeredgewidth=0, markersize=4.5)

        pylab.plot(range(nmethods), y.mean(axis=0), 's', color='white', markeredgecolor='k', markeredgewidth=2, markersize=7)

        if not vertical:
            pylab.xticks(range(nmethods), names, fontsize=fs, rotation=40)
        else:
            pylab.xticks(range(nmethods), names, fontsize=fs-1, rotation=40)
    
        if (vertical) or (dataset == 'compas'):
            pylab.yticks(yticks, fontsize=fs)
        else:
            pylab.yticks(yticks, fontsize=fs)
        if (vertical) or (dataset == 'compas'):
            pylab.ylabel('Accuracy', fontsize=fs)

        a = list(pylab.axis())
        a[0] -= 0.5
        a[1] += 0.5
        if dataset == 'compas':
            a[2] = 0.615
            a[3] = 0.725
        else:
            a[2] = 0.755
            a[3] = 0.885
        print a
        pylab.axis(a)
        pylab.tight_layout()
        pylab.title(title, fontsize=fs)

    if vertical:
        pylab.savefig('../figs/compare-compas-weapon-vertical.pdf')
    else:
        pylab.savefig('../figs/compare-compas-weapon.pdf')
