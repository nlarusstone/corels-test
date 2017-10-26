import numpy as np
import pandas as pd
import pylab

pylab.ion()
pylab.figure(10, figsize=(12, 4))
pylab.clf()
fs = 12
pylab.subplot(1, 2, 1)
pylab.plot(-1, -1, 'D', markerfacecolor='w', markeredgecolor='k', markersize=6, markeredgewidth=2)
pylab.plot(-1, -1, 'D', markerfacecolor='k', markersize=8, markeredgewidth=1, markeredgecolor='gray')
pylab.legend(('TPR (open)', 'FPR (solid)'), fontsize=fs, numpoints=1, loc='upper left')
pylab.subplot(1, 2, 2)
pylab.plot(-1, -1, 'D', markerfacecolor='w', markeredgecolor='k', markersize=6, markeredgewidth=2)
pylab.plot(-1, -1, 'D', markerfacecolor='k', markersize=8, markeredgewidth=1, markeredgecolor='gray')
pylab.legend(('TNR (open)', 'FNR (solid)'), fontsize=fs, numpoints=1, loc='upper left')

for fold in range(10):

    fname = '../jmlr/for-compas_%d_train.out-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=1000000000-c=0.0050000-v=10-f=1000-opt.txt' % fold
    with open(fname, 'r') as f:
        line = f.readline()
        opt = map(lambda x: x.split('~'), line.split(';'))
        print opt

    binary = pd.read_csv('../data/CrossValidation/propublica_ours_%d_test-binary.csv' % fold)
    #bin_1 = binary.loc[split_1].reset_index(drop=True).T
    black = binary['race:African-American']
    white = binary['race:Caucasian']

    nrules = 0
    with open('../data/CrossValidation/compas_%d_test.out' % fold) as f:
        line = f.readline()
        nrules = len(line.split()) - 1
    out = pd.read_csv('../data/CrossValidation/compas_%d_test.out' % fold, sep=' ', names=['Rule'] + range(nrules))
    label = pd.read_csv('../data/CrossValidation/compas_%d_test.label' % fold, sep=' ', names=['Rule'] + range(nrules))
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
    pred_arr = pd.Series(map(lambda x: int(x[1]), sorted_preds))
    true_arr = label.iloc[1, :]

    black_preds = pred_arr.loc[black.astype(bool)]
    black_true = true_arr.loc[black.astype(bool)]
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

    white_preds = pred_arr.loc[white.astype(bool)]
    white_true = true_arr.loc[white.astype(bool)]
    white_tp = ((white_preds == 1) & (white_true == 1)).sum()
    white_fp = ((white_preds == 1) & (white_true == 0)).sum()
    white_fn = ((white_preds == 0) & (white_true == 1)).sum()
    white_tn = ((white_preds == 0) & (white_true == 0)).sum()
    white_tn = white_cnf[0][0]
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
    pylab.plot(1 + offset, black_tpr, 'd', markerfacecolor='w', markeredgecolor='r', markersize=6, markeredgewidth=2)
    pylab.plot(1 + offset, black_fpr, 'd', markerfacecolor='r', markersize=8, markeredgewidth=1, markeredgecolor='gray')
    pylab.plot(2 + offset, black_tpr, 'd', markerfacecolor='w', markeredgecolor='b', markersize=6, markeredgewidth=2)
    pylab.plot(2 + offset, black_fpr, 'd', markerfacecolor='b', markersize=8, markeredgewidth=1, markeredgecolor='gray')
    pylab.plot(3 + offset, white_tpr, 's', markerfacecolor='w', markeredgecolor='darkred', markersize=6, markeredgewidth=2)
    pylab.plot(3 + offset, white_fpr, 's', markerfacecolor='darkred', markersize=7, markeredgewidth=1, markeredgecolor='gray')
    pylab.plot(4 + offset, white_tpr, 's', markerfacecolor='w', markeredgecolor='c', markersize=6, markeredgewidth=2)
    pylab.plot(4 + offset, white_fpr, 's', markerfacecolor='c', markersize=7, markeredgewidth=1, markeredgecolor='gray')
    pylab.axis([0.5, 4.5, 0, 1])
    pylab.xticks(np.array([1, 2, 3, 4]) + 0.1, ['Black\n(CORELS)', 'Black\n(COMPAS)', 'White\n(CORELS)', 'White\n(COMPAS)'], fontsize=fs)
    pylab.yticks(fontsize=fs)
    pylab.ylabel('True or false positive rate')
    pylab.subplot(1, 2, 2)
    pylab.plot(1 + offset, black_tnr, 'd', markerfacecolor='w', markeredgecolor='r', markersize=6, markeredgewidth=2)
    pylab.plot(1 + offset, black_fnr, 'd', markerfacecolor='r', markersize=8, markeredgewidth=1, markeredgecolor='gray')
    pylab.plot(2 + offset, black_tnr, 'd', markerfacecolor='w', markeredgecolor='b', markersize=6, markeredgewidth=2)
    pylab.plot(2 + offset, black_fnr, 'd', markerfacecolor='b', markersize=8, markeredgewidth=1, markeredgecolor='gray')
    pylab.plot(3 + offset, white_tnr, 's', markerfacecolor='w', markeredgecolor='darkred', markersize=6, markeredgewidth=2)
    pylab.plot(3 + offset, white_fnr, 's', markerfacecolor='darkred', markersize=7, markeredgewidth=1, markeredgecolor='gray')
    pylab.plot(4 + offset, white_tnr, 's', markerfacecolor='w', markeredgecolor='c', markersize=6, markeredgewidth=2)
    pylab.plot(4 + offset, white_fnr, 's', markerfacecolor='c', markersize=7, markeredgewidth=1, markeredgecolor='gray')
    pylab.axis([0.5, 4.5, 0, 1])
    pylab.xticks(np.array([1, 2, 3, 4]) + 0.1,  ['Black\n(CORELS)', 'Black\n(COMPAS)', 'White\n(CORELS)', 'White\n(COMPAS)'], fontsize=fs)
    pylab.yticks(fontsize=fs)
    pylab.ylabel('True or false negative rate')

pylab.savefig('../figs/compare_corels_compas.pdf')
