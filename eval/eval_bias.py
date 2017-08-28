import pandas as pd
import numpy as np

fname = '../logs/for-compas_1_train.out-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=100000000-c=0.0050000-v=100-f=1000-opt.txt'
with open(fname, 'r') as f:
    line = f.readline()
    opt = map(lambda x: x.split('~'), line.split(';'))
    print opt

seed = sum([3, 15, 13, 16, 1, 19])
num_samples = 7214
num_folds = 10
np.random.seed(seed)
splits = np.split(np.random.permutation(num_samples / num_folds * num_folds), num_folds)
print splits
split_1 = np.concatenate([splits[j] for j in range(num_folds) if (j != 1)])
print split_1

binary = pd.read_csv('../data/compas-binary.csv')
bin_1 = binary.loc[split_1].reset_index(drop=True).T
black = bin_1.loc['Race=African-American:True']
white = bin_1.loc['Race=Caucasian:True']

nrules = 0
with open('../data/CrossValidation/compas_1_train.out') as f:
    line = f.readline()
    nrules = len(line.split()) - 1
out = pd.read_csv('../data/CrossValidation/compas_1_train.out', sep=' ', names=['Rule'] + range(nrules))
label = pd.read_csv('../data/CrossValidation/compas_1_train.label', sep=' ', names=['Rule'] + range(nrules))
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
black_preds.name = 'preds'
black_true.name = 'true'
black_cnf = pd.crosstab(black_preds, black_true)
print black_cnf
black_tp = black_cnf[1][1]
black_fp = black_cnf[0][1]
black_fn = black_cnf[1][0]
black_tn = black_cnf[0][0]
print 'Black TP: {0} FN: {1}, FP: {2}, TN: {3}'.format(black_tp, black_fn, black_fp, black_tn)
print 'Black TPR: {0}'.format(float(black_tp) / (black_tp + black_fn))
print 'Black FPR: {0}'.format(float(black_fp) / (black_fp + black_tn))

white_preds = pred_arr.loc[white.astype(bool)]
white_true = true_arr.loc[white.astype(bool)]
white_preds.name = 'preds'
white_true.name = 'true'
white_cnf = pd.crosstab(white_preds, white_true)
print white_cnf
white_tp = white_cnf[1][1]
white_fp = white_cnf[0][1]
white_fn = white_cnf[1][0]
white_tn = white_cnf[0][0]
print 'white TP: {0} FN: {1}, FP: {2}, TN: {3}'.format(white_tp, white_fn, white_fp, white_tn)
print 'white TPR: {0}'.format(float(white_tp) / (white_tp + white_fn))
print 'white FPR: {0}'.format(float(white_fp) / (white_fp + white_tn))
