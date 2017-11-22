"""
This could be improved with the use of functions and using either pandas or tabluar

"""
import os

import numpy as np
import pandas as pd
import pylab
import tabular as tb

pylab.ion()
pylab.figure(10, figsize=(14, 4.5))
pylab.clf()
fs = 16
pylab.subplot(1, 2, 1)
#pylab.plot(-1, -1, 'D', markerfacecolor='w', markeredgecolor='k', markersize=6, markeredgewidth=2)
#pylab.plot(-1, -1, 'D', markerfacecolor='k', markersize=8, markeredgewidth=1, markeredgecolor='gray')
#pylab.legend(('TPR (open)', 'FPR (solid)'), fontsize=fs, numpoints=1, loc='lower left', frameon=False, borderpad=0)
pylab.subplot(1, 2, 2)
#pylab.plot(-1, -1, 'D', markerfacecolor='k', markersize=8, markeredgewidth=1, markeredgecolor='gray')
#pylab.plot(-1, -1, 'D', markerfacecolor='w', markeredgecolor='k', markersize=6, markeredgewidth=2)
#pylab.legend(('TNR  = 1 - FPR (open)', 'FNR  = 1 - TPR (solid)'), fontsize=fs, numpoints=1, loc='lower left', frameon=False, borderpad=0)

compas_accuracy = []
fin = os.path.join('..', 'compas', 'compas-scores-two-years.csv')
#fout = os.path.join('..', 'viz', 'compas-accuracy.csv')
seed = sum([3, 15, 13, 16, 1, 19]) # c:3, o:15, m:13, p:16, a:1, s:19
np.random.seed(seed)
# duplicate names in header:  decile_score, priors_count
names = open(fin, 'rU').read().strip().split('\n')[0].split(',')
nlist = []
for n in names:
    if n in nlist:
        print 'duplicate name', n, '->', n + '_'
        nlist.append('%s_' % n)
    else:
        nlist.append(n)

num_folds = 10
y = tb.tabarray(SVfile=fin, names=nlist)
# require record to have c_jail_in field
keep = y['c_jail_in'] != ''
y = y[keep]
train = False
split_ind = np.array_split(np.random.permutation(len(y)), num_folds)
if train:
    split_ind = [np.concatenate([split_ind[j] for j in range(num_folds) if (j != i)]) for i in range(num_folds)]
    ftag = 'train'
else:
    ftag = 'test'

for fold in range(num_folds):

    fname = '../jmlr/for-compas_%d_train.out-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=1000000000-c=0.0050000-v=10-f=1000-opt.txt' % fold
    with open(fname, 'r') as f:
        line = f.readline()
        opt = map(lambda x: x.split('~'), line.split(';'))
        print opt

    nrules = 0
    with open('../data/CrossValidation/compas_%d_%s.out' % (fold, ftag)) as f:
        line = f.readline()
        nrules = len(line.split()) - 1
    out = pd.read_csv('../data/CrossValidation/compas_%d_%s.out' % (fold, ftag), sep=' ', names=['Rule'] + range(nrules))
    label = pd.read_csv('../data/CrossValidation/compas_%d_%s.label' % (fold, ftag), sep=' ', names=['Rule'] + range(nrules))
    out.set_index('Rule', inplace=True)
    label.set_index('Rule', inplace=True)

    captured = set()
    preds = []
    for (rule, pred) in opt[:-1]:
        cappd = out.ix[rule] == 1
        unfiltered_cappd = out.T[cappd].index
        filtered_cappd = set(unfiltered_cappd).difference(captured)
        preds += map(lambda x: (x, pred), filtered_cappd)
        captured = captured.union(filtered_cappd)
    
    # Handle default rule
    _, def_pred = opt[-1]
    preds += [(x, def_pred) for x in set(range(nrules)).difference(captured)]
    sorted_preds = sorted(preds, key=lambda x: x[0])
    pred_arr = np.array(pd.Series(map(lambda x: int(x[1]), sorted_preds)))
    true_arr = np.array(label.iloc[1, :])

    black = y[split_ind[fold]]['race'] == 'African-American'
    white = y[split_ind[fold]]['race'] == 'Caucasian'

    print 'CORELS'
    black_preds = pred_arr[black]
    black_true = true_arr[black]
    black_tp = ((black_preds == 1) & (black_true == 1)).sum()
    black_fp = ((black_preds == 1) & (black_true == 0)).sum()
    black_fn = ((black_preds == 0) & (black_true == 1)).sum()
    black_tn = ((black_preds == 0) & (black_true == 0)).sum()
    black_tpr = float(black_tp) / (black_tp + black_fn)
    black_fpr = float(black_fp) / (black_fp + black_tn)
    black_fnr = float(black_fn) / (black_tp + black_fn)
    black_tnr = float(black_tn) / (black_fp + black_tn)
    print 'Black TP: {0} FN: {1}, FP: {2}, TN: {3}'.format(black_tp, black_fn, black_fp, black_tn)
    print 'Black TPR: {0}'.format(black_tpr)
    print 'Black FPR: {0}'.format(black_fpr)

    white_preds = pred_arr[white]
    white_true = true_arr[white]
    white_tp = ((white_preds == 1) & (white_true == 1)).sum()
    white_fp = ((white_preds == 1) & (white_true == 0)).sum()
    white_fn = ((white_preds == 0) & (white_true == 1)).sum()
    white_tn = ((white_preds == 0) & (white_true == 0)).sum()
    white_tpr = float(white_tp) / (white_tp + white_fn)
    white_fpr = float(white_fp) / (white_fp + white_tn)
    white_fnr = float(white_fn) / (white_tp + white_fn)
    white_tnr = float(white_tn) / (white_fp + white_tn)
    print 'white TP: {0} FN: {1}, FP: {2}, TN: {3}'.format(white_tp, white_fn, white_fp, white_tn)
    print 'white TPR: {0}'.format(white_tpr)
    print 'white FPR: {0}'.format(white_fpr)

    offset = fold * 0.02
    pylab.suptitle('Comparison of CORELS and COMPAS by race (ProPublica dataset)\n', fontsize=fs)
    pylab.subplot(1, 2, 1)
    p1 = pylab.plot(1 + offset, black_tpr, 'd', markerfacecolor='w', markeredgecolor='r', markersize=6, markeredgewidth=2)
    p2 = pylab.plot(1 + offset, black_fpr, 'd', markerfacecolor='r', markersize=8, markeredgewidth=1, markeredgecolor='gray')
    p3 = pylab.plot(3 + offset, white_tpr, 's', markerfacecolor='w', markeredgecolor='b', markersize=6, markeredgewidth=2)
    p4 = pylab.plot(3 + offset, white_fpr, 's', markerfacecolor='b', markersize=7, markeredgewidth=1, markeredgecolor='gray')
    pylab.axis([0.5, 4.5, 0, 0.89])
    pylab.xticks(np.array([1, 2, 3, 4]) + 0.1, ['Black\n(CORELS)', 'Black\n(COMPAS)', 'White\n(CORELS)', 'White\n(COMPAS)'], fontsize=fs-2)
    pylab.yticks(np.arange(0, 0.9, 0.2), fontsize=fs)
    pylab.ylabel('True or false positive rate', fontsize=fs)
    pylab.subplot(1, 2, 2)
    pylab.plot(1 + offset, black_tnr, 'd', markerfacecolor='darkred', markersize=8, markeredgewidth=1, markeredgecolor='gray')
    pylab.plot(1 + offset, black_fnr, 'd', markerfacecolor='w', markeredgecolor='darkred', markersize=6, markeredgewidth=2)
    pylab.plot(3 + offset, white_tnr, 's', markerfacecolor='c', markersize=7, markeredgewidth=1, markeredgecolor='gray')
    pylab.plot(3 + offset, white_fnr, 's', markerfacecolor='w', markeredgecolor='c', markersize=6, markeredgewidth=2)
    pylab.axis([0.5, 4.5, 0, 0.89])
    pylab.xticks(np.array([1, 2, 3, 4]) + 0.1,  ['Black\n(CORELS)', 'Black\n(COMPAS)', 'White\n(CORELS)', 'White\n(COMPAS)'], fontsize=fs-2)
    pylab.yticks(np.arange(0, 0.9, 0.2), fontsize=fs)
    pylab.ylabel('True or false negative rate', fontsize=fs)

    print 'COMPAS'
    compas = np.array(y[split_ind[fold]]['decile_score'] >= 5, int)
    black_preds = compas[black]
    black_tp = ((black_preds == 1) & (black_true == 1)).sum()
    black_fp = ((black_preds == 1) & (black_true == 0)).sum()
    black_fn = ((black_preds == 0) & (black_true == 1)).sum()
    black_tn = ((black_preds == 0) & (black_true == 0)).sum()
    black_tpr = float(black_tp) / (black_tp + black_fn)
    black_fpr = float(black_fp) / (black_fp + black_tn)
    black_fnr = float(black_fn) / (black_tp + black_fn)
    black_tnr = float(black_tn) / (black_fp + black_tn)
    print 'Black TP: {0} FN: {1}, FP: {2}, TN: {3}'.format(black_tp, black_fn, black_fp, black_tn)
    print 'Black TPR: {0}'.format(black_tpr)
    print 'Black FPR: {0}'.format(black_fpr)

    white_preds = compas[white]
    white_tp = ((white_preds == 1) & (white_true == 1)).sum()
    white_fp = ((white_preds == 1) & (white_true == 0)).sum()
    white_fn = ((white_preds == 0) & (white_true == 1)).sum()
    white_tn = ((white_preds == 0) & (white_true == 0)).sum()
    white_tpr = float(white_tp) / (white_tp + white_fn)
    white_fpr = float(white_fp) / (white_fp + white_tn)
    white_fnr = float(white_fn) / (white_tp + white_fn)
    white_tnr = float(white_tn) / (white_fp + white_tn)

    compas_accuracy += [(compas == true_arr).sum() / float(len(true_arr))]

    pylab.subplot(1, 2, 1)
    pylab.plot(2 + offset, black_tpr, 'd', markerfacecolor='w', markeredgecolor='r', markersize=6, markeredgewidth=2)
    pylab.plot(2 + offset, black_fpr, 'd', markerfacecolor='r', markersize=8, markeredgewidth=1, markeredgecolor='gray')
    pylab.plot(4 + offset, white_tpr, 's', markerfacecolor='w', markeredgecolor='b', markersize=6, markeredgewidth=2)
    pylab.plot(4 + offset, white_fpr, 's', markerfacecolor='b', markersize=7, markeredgewidth=1, markeredgecolor='gray')
    pylab.subplot(1, 2, 2)
    pylab.plot(2 + offset, black_fnr, 'd', markerfacecolor='w', markeredgecolor='darkred', markersize=6, markeredgewidth=2)
    pylab.plot(2 + offset, black_tnr, 'd', markerfacecolor='darkred', markersize=8, markeredgewidth=1, markeredgecolor='gray')
    pylab.plot(4 + offset, white_fnr, 's', markerfacecolor='w', markeredgecolor='c', markersize=6, markeredgewidth=2)
    pylab.plot(4 + offset, white_tnr, 's', markerfacecolor='c', markersize=7, markeredgewidth=1, markeredgecolor='gray')

pylab.subplot(1,2,1)
pylab.legend(('Black TPR', 'Black FPR', 'White TPR', 'White FPR'), fontsize=fs-1, numpoints=1, loc='lower left', frameon=False, borderpad=0, ncol=2, columnspacing=0.1, handletextpad=0.1, borderaxespad=0.3, handlelength=1.6)

pylab.subplot(1,2,2)
pylab.legend(('Black TNR', 'Black FNR', 'White TNR (= 1 $-$ FPR)', 'White FNR (= 1 $-$ TPR)'), fontsize=fs-1, numpoints=1, loc='lower left', frameon=False, borderpad=0, ncol=2, columnspacing=0.1, handletextpad=0.1, borderaxespad=0.3, handlelength=1.6)

print 'COMPAS accuracy:', compas_accuracy

if train:
    pylab.savefig('../figs/compare_corels_compas-train.pdf')
else:
    pylab.savefig('../figs/compare_corels_compas.pdf')
