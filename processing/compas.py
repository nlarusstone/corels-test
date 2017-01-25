import os

import numpy as np
import tabular as tb

import mine


def age_func(a):
    if (a <= 20):       # minimum age is 18
        return '18-20'  # support = 220
    elif (a <= 22):
        return '21-25'  # support = 1641
    elif (a <= 25):
        return '26-30'  # support = 1512
    elif (a <= 40):
        return '31-40'  # support = 1818
    elif (a <= 50):
        return '41-50'  # support = 1045
    elif (a <= 60):
        return '51-60'  # support = 748
    else:
        return '>60'    # support = 230

def priors_count_func(p):
    if (p == 0):
        return '=0'     # support = 2150
    elif (p <= 1):
        return '=1'     # support = 1397
    elif (p <= 3):
        return '2-3'    # support = 1408
    else:
        return '>=4'    # support = 736+1523


fin = os.path.join('..', 'compas', 'compas-scores-two-years.csv')
fout = os.path.join('..', 'data', 'compas.csv')
din = os.path.join('..', 'data')
dout = os.path.join('..', 'data', 'CrossValidation')

seed = sum([3, 15, 13, 16, 1, 19]) # c:3, o:15, m:13, p:16, a:1, s:19
num_folds = 10
max_cardinality = 2
min_support = 0.005
labels = ['No', 'Yes']
minor = True

np.random.seed(seed)

x = tb.tabarray(SVfile=fin)

# duplicate names in header:  decile_score, priors_count
names = open(fin, 'rU').read().strip().split('\n')[0].split(',')

nlist = []
for (d, n) in zip(x.dtype.names, names):
    if n in nlist:
        print 'duplicate name', n, '->', n + '_'
        x.renamecol(d, '%s_' % n)
    else:
        x.renamecol(d, n)
        nlist.append(n)

assert (x['priors_count'] == x['priors_count_']).all()
assert (x['decile_score'] == x['decile_score_']).all()

"""
columns = [(x['sex'] == 'Male'),
           (x['age'] <= 20), (x['age'] <= 22), (x['age'] <= 25),
           (x['age'] < 30), (x['age'] >= 60),
           ((x['age'] >= 30) & (x['age'] <= 44)),
           ((x['age'] >= 45) & (x['age'] <= 59))]
"""

age = np.array([age_func(i) for i in x['age']])

juvenile_felonies = np.array(['>0' if (i > 0) else '=0' for i in x['juv_fel_count']])   # support = 282

juvenile_misdemeanors = np.array(['>0' if (i > 0) else '=0' for i in x['juv_misd_count']])  # support = 415

priors_count = np.array([priors_count_func(i) for i in x['priors_count']])

assert (set(x['c_charge_degree']) == set(['F', 'M']))

c_charge_degree = np.array(['Misdemeanor' if (i == 'M') else 'Felony' for i in x['c_charge_degree']])

# see `c_jail_in` and `c_jail_out` for time in jail?

columns = [x['sex'], age, juvenile_felonies, juvenile_misdemeanors,
           priors_count, c_charge_degree, x['two_year_recid']]

cnames = ['sex', 'age', 'juvenile-felonies', 'juvenile-misdemeanors',
          'priors', 'current-charge-degree', 'recidivate-within-two-years']

"""
race_list = list(set(x['race']))
 
columns += [(x['race'] == n) for n in race_list]

cnames = ['Gender=Male', 'Age=18-20', 'Age=18-22', 'Age=18-25',
          'Age<30', 'Age>=60', 'Age=30-44', 'Age=45-59']

cnames += ['Race=%s' % r for r in race_list]
"""


print 'write categorical dataset', fout
y = tb.tabarray(columns=columns, names=cnames)
y.saveSV(fout)

print 'permute and partition dataset'
split_ind = np.split(np.random.permutation(len(y) / num_folds * num_folds), num_folds)
print 'number of folds:', num_folds
print 'train size:', len(split_ind[0]) * (num_folds - 1)
print 'test size:', len(split_ind[0])

num_rules = np.zeros(num_folds, int)
for i in range(num_folds):
    print 'generate cross-validation split', i
    cv_root = 'compas_%d' % i
    test_root = '%s_test' % cv_root
    train_root = '%s_train' % cv_root
    ftest = os.path.join(dout, '%s.csv' % test_root)
    ftrain = os.path.join(dout, '%s.csv' % train_root)
    y[split_ind[i]].saveSV(ftest)
    y[np.concatenate([split_ind[j] for j in range(num_folds) if (j != i)])].saveSV(ftrain)

    print 'mine rules from', ftrain
    num_rules[i] = mine.mine_rules(din=dout, froot=train_root,
                                    max_cardinality=max_cardinality,
                                    min_support=min_support, labels=labels,
                                    minor=minor)
    mine.apply_rules(din=dout, froot=cv_root, labels=labels)

print '(min, max) # rules mined per fold:', (num_rules.min(), num_rules.max())
