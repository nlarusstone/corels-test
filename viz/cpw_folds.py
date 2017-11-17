import numpy as np
import pylab
import tabular as tb

pylab.ion()
pylab.figure(2, figsize=(8, 3.5))
pylab.clf()
ax = pylab.subplot2grid((20, 1), (0, 1), colspan=1, rowspan=19)
pylab.figure(3, figsize=(8, 3.5))
pylab.clf()
pylab.figure(4, figsize=(8, 3.5))
pylab.clf()

#True Positive, False Negative, False Positive, True Negative
ct = []
#reg = np.array([0.005, 0.005, 0.01, 0.01, 0, 0, 0, 0])
#thresh = np.array([0, 0, 0, 0, 1, 2, 3, 4])
cvec = ['r'] * 2 + ['darkred'] * 2 + ['c', 'blue'] * 2
marker = ['s', '^', 's', '^'] + ['d', 'd', 'o', 'o']
legend = ['CORELS ($\lambda =$.005, Feature Set C)', 'CORELS ($\lambda =$.005, Feature Set D)', 'CORELS ($\lambda =$.01, Feature Set C)', 'CORELS ($\lambda =$.01, Feature Set D)'] + [u'Heuristic (T = %d)' % i for i in [1, 2, 3, 4]]
fs = 14
nfolds = 10
imap = [5, 6, 3, 4, 7, 2, 1, 0]
#imap2 = [4, 5, 6, 7, 3, 2, 1, 0]
imap2 = [6, 7, 0, 1, 5, 4, 3, 2]
names = 'Fold,Method,C,cp,R,T,accuracy,leaves,train_accuracy,ntest,TP,FP,FN,TN,TPR,FPR'.split(',')

for nfig in [3, 4]:
    pylab.figure(nfig)
    pylab.plot(-1, -1, 'D', markerfacecolor='w', markeredgecolor='k', markersize=6, markeredgewidth=2)
    pylab.plot(-1, -1, 'D', markerfacecolor='k', markersize=8, markeredgewidth=1, markeredgecolor='k')
    if (nfig == 3):
        loc = 'upper left'
    else:
        loc = 'upper left'
    pylab.legend(('TPR (open)', 'FPR (solid)'), fontsize=fs, numpoints=1, loc=loc, frameon=False, borderpad=0)

for fold in range(nfolds):
    ct = []
    ll = []

    # python2 eval_model.py cpw -n 10000 -r 0.005 -c 2 -p 1 -v 10 --minor --parallel
    ctables = np.array([[565, 523, 3724, 27767], [541, 547, 3734, 27757], [555, 533, 3753, 27738], [575, 513, 3604, 27887], [549, 539, 3663, 27828], [559, 529, 3669, 27822], [569, 519, 3757, 27734], [545, 543, 3641, 27850], [550, 538, 3706, 27785], [648, 440, 5567, 25924]])
    leaves = [5] * 9 + [6]
    ct += [ctables[fold]]
    ll += [leaves[fold]]

    # python2 eval_model.py cpw-noloc -n 10000 -r 0.005 -c 2 -p 1 -v 10 --minor --parallel
    ctables = np.array([[625, 463, 6468, 25023], [602, 486, 6377, 25114], [624, 464, 6538, 24953], [646, 442, 6495, 24996], [629, 459, 6462, 25029], [630, 458, 6555, 24936], [589, 499, 6263, 25228], [620, 468, 6225, 25266], [638, 450, 6559, 24932], [655, 433, 6389, 25102]])
    leaves = [5] * 10
    ct += [ctables[fold]]
    ll += [leaves[fold]]

    # python2 eval_model.py cpw -n 10000 -r 0.01 -c 2 -p 1 -v 10 --minor --parallel
    ctables = np.array([[435, 653, 1001, 30490], [439, 649, 990, 30501], [437, 651, 970, 30521], [471, 617, 949, 30542], [438, 650, 1031, 30460], [454, 634, 1026, 30465], [435, 653, 988, 30503], [438, 650, 1014, 30477], [423, 665, 1002, 30489], [457, 631, 946, 30545]])
    leaves = [3] * 10
    ct += [ctables[fold]]
    ll += [leaves[fold]]

    # python2 eval_model.py cpw-noloc -n 10000 -r 0.01 -c 2 -p 1 -v 10 --minor --parallel
    ctables = np.array([[490, 598, 3870, 27621], [508, 580, 3871, 27620], [508, 580, 3828, 27663], [534, 554, 3775, 27716], [505, 583, 3910, 27581], [508, 580, 3850, 27641], [503, 585, 3761, 27730], [503, 585, 3932, 27559], [493, 595, 3885, 27606], [522, 566, 3806, 27685]])
    leaves = [3] * 10
    ct += [ctables[fold]]
    ll += [leaves[fold]]

    fname = '../data/CrossValidation/cpw-noloc_%d_test-binary.csv' % fold
    y = tb.tabarray(SVfile=fname)
    z = 3 * y['cs_objcs:stop-reason=suspicious-object'] + y['ac_stsnd:circumstances=sights-and-sounds-of-criminal-activity'] + y['cs_bulge:stop-reason=suspicious-bulge']

    for t in range(1, 5):
        yes = (z >= t)
        no = np.invert(yes)
        weapon = (y['weapon:1'] == 1)
        nw = np.invert(y['weapon:1'])
        tp = (yes & weapon).sum()
        fn = (no & weapon).sum()
        fp = (yes & nw).sum()
        tn = (no & nw).sum()
        ct += [[tp, fn, fp, tn]]

    ct = [c for c in np.array(ct, float).T]
    (tp, fn, fp, tn) = ct

    n = (tp + tn + fp + fn)
    acc = (tp + tn) / n
    tpr = tp / (tp + fn)
    fpr = fp / (fp + tn)
    pos = (tp + fp) / n

    print 'accuracy:', acc
    print 'tpr:', tpr
    print 'fpr:', fpr

    nr = len(n)
    fold_name = ['cpw-noloc', 'cpw', 'cpw-noloc', 'cpw'] + ['cpw'] * 4
    fold_name = ['%s_%d' % (name, fold) for name in fold_name]
    method = ['CORELS'] * 4 + ['Heuristic'] * 4
    zz = np.zeros(8)
    rr = [0.005] * 2 + [0.01] * 2 + [0.] * 4
    tt = [0.] * 4 + [1, 2, 3, 4]
    ll += [4] * 4
    cols = [fold_name, method, zz, zz, rr, tt, zz, ll, acc, n,
            np.cast[int](tp), np.cast[int](fp), np.cast[int](fn), np.cast[int](tn), tpr, fpr]
    if (fold == 0):
        x = tb.tabarray(columns=cols, names=names)
    else:
        x = x.rowstack(tb.tabarray(columns=cols, names=names))

    pylab.figure(2)
    for i in range(len(tp)):
        pylab.plot(pos[i], tpr[i], markersize=7, marker=marker[i], markerfacecolor='white', markeredgecolor=cvec[i], markeredgewidth=1, linestyle="None")
        print pos[i], tpr[i]

    pylab.figure(3)
    for i in range(len(tp)):
        #pylab.subplot(1, 2, 1)
        pylab.plot(imap[i] + 0.5, tpr[i], markersize=7, marker=marker[i], markerfacecolor='white', markeredgecolor=cvec[i], markeredgewidth=1, linestyle="None")
        #pylab.subplot(1, 2, 2)
        pylab.plot(imap[i] + 0.5, fpr[i], markersize=7, marker=marker[i], color=cvec[i], markeredgewidth=0, linestyle="None")
        if (fold == 0):
            pylab.text(imap[i] + 0.7, tpr[i], str(ll[i]), fontsize=fs)
        #    pylab.text(imap[i] + 0.42, 0.37 + (0.1 * ll[i] - 0.4) / 2, str(ll[i]), fontsize=fs)

    pylab.figure(4)
    for i in range(len(tp)):
        pylab.plot(imap2[i] + 0.5, tpr[i], markersize=7, marker=marker[i], markerfacecolor='white', markeredgecolor=cvec[i], markeredgewidth=1, linestyle="None")
        pylab.plot(imap2[i] + 0.5, fpr[i], markersize=7, marker=marker[i], color=cvec[i], markeredgewidth=0, linestyle="None")
        if (fold == 0):
            pylab.text(imap2[i] + 0.7, tpr[i], str(ll[i]), fontsize=fs)

x.saveSV('../eval/cpw-noloc_sparsity_jmlr-CORELS.csv')

pylab.figure(2)
pylab.axis([0, 0.35, 0, 0.65])
pylab.plot([0, 0.35], [0.5, 0.5], 'k:')
pylab.xlabel('Fraction of stops', fontsize=fs)
pylab.ylabel('Fraction recovered', fontsize=fs)
pylab.title('Fraction of weapons recovered (NYPD dataset)', fontsize=fs)
pylab.xticks(fontsize=fs)
pylab.yticks(np.arange(0, 0.8, 0.2), fontsize=fs)
pylab.legend(legend, loc='lower right', fontsize=fs-2, frameon=False, numpoints=1, ncol=2, columnspacing=0., handletextpad=0.1)
pylab.savefig('../figs/cpw_folds.pdf')

pylab.figure(3)
#pylab.subplot(1, 2, 1)
pylab.axis([0, 8, 0, 0.7])
pylab.plot([0, 8], [0.5, 0.5], 'k:')
#pylab.xticks(np.arange(0.5, 8, 1), ())
pylab.yticks(np.arange(0, 0.8, 0.2), fontsize=fs)
#pylab.title('True positive rate', fontsize=fs)
#pylab.subplot(1, 2, 2)
#pylab.axis([0, 8.5, 0, 0.7])
#pylab.xticks(np.arange(0.5, 8, 1), [u'=4', u'=3', u'=2', '.01*', '.01', '.005*', '.005', u'=1'], rotation=25)
pylab.xticks(np.arange(0.5, 8, 1), [u'Heuristic\n(T = 4)', u'Heuristic\n(T = 3)', u'Heuristic\n(T = 2)', 'CORELS\n(.01, C)', 'CORELS\n(.01, D)', 'CORELS\n(.005, C)', 'CORELS\n(.005, D)', u'Heuristic\n(T = 1)'])
pylab.yticks(np.arange(0, 0.8, 0.2), fontsize=fs)
pylab.ylabel('True or false positive rate', fontsize=fs)
pylab.title('Comparison of CORELS and heuristic models (NYPD dataset)', fontsize=fs)
pylab.savefig('../figs/cpw_tpr_fpr.pdf')

pylab.figure(4)
pylab.axis([0, 8, 0, 0.65])
pylab.plot([0, 8], [0.5, 0.5], 'k:')
#pylab.xticks(np.arange(0.5, 8, 1), ())
pylab.yticks(np.arange(0, 0.8, 0.2), fontsize=fs)
#pylab.title('True positive rate', fontsize=fs)
#pylab.subplot(1, 2, 2)
#pylab.axis([0, 8.5, 0, 0.7])
#pylab.xticks(np.arange(0.5, 8, 1), [u'=4', u'=3', u'=2', '.01*', '.01', '.005*', '.005', u'=1'], rotation=25)
pylab.xticks(np.arange(0.5, 8, 1), ['CORELS\n(.01, C)', 'CORELS\n(.01, D)', u'Heuristic\n(T = 4)', u'Heuristic\n(T = 3)', u'Heuristic\n(T = 2)', u'Heuristic\n(T = 1)', 'CORELS\n(.005, C)', 'CORELS\n(.005, D)'])
pylab.yticks(np.arange(0, 0.8, 0.2), fontsize=fs)
pylab.ylabel('True or false positive rate', fontsize=fs)
pylab.title('Comparison of CORELS and heuristic models (NYPD dataset)', fontsize=fs)
pylab.savefig('../figs/cpw_tpr_fpr_sparsity.pdf')
