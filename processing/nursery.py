"""
From https://archive.ics.uci.edu/ml/datasets/Nursery

    12960 instances, 8 attributes, no missing values

From https://archive.ics.uci.edu/ml/machine-learning-databases/nursery/nursery.names

   parents        usual, pretentious, great_pret
   has_nurs       proper, less_proper, improper, critical, very_crit
   form           complete, completed, incomplete, foster
   children       1, 2, 3, more
   housing        convenient, less_conv, critical
   finance        convenient, inconv
   social         non-prob, slightly_prob, problematic
   health         recommended, priority, not_recom

   class        N         N[%]
   ------------------------------
   not_recom    4320   (33.333 %)
   recommend       2   ( 0.015 %)
   very_recom    328   ( 2.531 %)
   priority     4266   (32.917 %)
   spec_prior   4044   (31.204 %)

From https://arxiv.org/pdf/1602.08610v1.pdf

    "the goal is to predict whether a child's application to nursey school will
    be in either the 'very recommended' or 'special priority' categories,"

"""
import os

import numpy as np
import tabular as tb

import mine
import utils


din = os.path.join('..', 'data', 'nursery')
dout = os.path.join('..', 'data', 'CrossValidation')
fdata = os.path.join(din, 'nursery.data')
ftest = os.path.join(din, 'nursery.test')
fnames = os.path.join(din, 'nursery.names')
fcomplete = os.path.join(din, 'nursery-filtered.csv')
bout = os.path.join('..', 'data', 'nursery-binary.csv')
fout = os.path.join(din, 'nursery.csv')

seed = sum([14, 21, 18, 19, 5, 18, 25]) # n:14, u:21, r:18, s:19, e:5, r:18, y:25
num_folds = 10
max_cardinality = 2
min_support = 0.1
labels = ['No', 'Yes']
minor = False

np.random.seed(seed)

if not os.path.exists(din):
    os.mkdir(din)

if not os.path.exists(dout):
    os.mkdir(dout)

if not os.path.exists(fdata):
    print 'downloading data'
    uroot = 'https://archive.ics.uci.edu/ml/machine-learning-databases/nursery/'
    os.system('wget %snursery.data -O %s' % (uroot, fdata))
    os.system('wget %snursery.names -O %s' % (uroot, fnames))

names = ['parents', 'has_nurs', 'form', 'children', 'housing', 'finance',
         'social', 'health', 'recommend']

print 'read original train data:', fdata
x = open(fdata, 'rU').read().strip().split('\n')
x = [','.join(line.split(', ')) for line in x if '?' not in line]
assert (len(x) == 12960)

f = open(fcomplete, 'w')
f.write(','.join(names) + '\n')
f.write('\n'.join(x))
f.close()

print 'lightly process data (e.g., to make binary features)'
x = tb.tabarray(SVfile=fcomplete)

recommend = np.cast[int]((x['recommend'] == 'spec_prior') | (x['recommend'] == 'very_recom'))

y = x[names[:-1]].colstack(tb.tabarray(columns=[recommend], names=names[-1:]))

print 'write categorical dataset', fout
y.saveSV(fout)

print 'write binary dataset', bout
b = utils.to_binary(y)
b.saveSV(bout)

print 'permute and partition dataset'
split_ind = np.split(np.random.permutation(len(y) / num_folds * num_folds), num_folds)
print 'number of folds:', num_folds
print 'train size:', len(split_ind[0]) * (num_folds - 1)
print 'test size:', len(split_ind[0])

num_rules = np.zeros(num_folds, int)
for i in range(num_folds):
    print 'generate cross-validation split', i
    cv_root = 'nursery_%d' % i
    test_root = '%s_test' % cv_root
    train_root = '%s_train' % cv_root
    ftest = os.path.join(dout, '%s.csv' % test_root)
    ftrain = os.path.join(dout, '%s.csv' % train_root)
    b[split_ind[i]].saveSV(ftest)
    b[np.concatenate([split_ind[j] for j in range(num_folds) if (j != i)])].saveSV(ftrain)

    print 'mine rules from', ftrain
    num_rules[i] = mine.mine_binary(din=dout, froot=train_root,
                                   max_cardinality=max_cardinality,
                                   min_support=min_support,
                                   minor=minor)
    mine.apply_binary(din=dout, froot=cv_root)

print '(min, max) # rules mined per fold:', (num_rules.min(), num_rules.max())

#ben.driver(din='../data/nursery', dout='../data/nursery', froot='nursery', train_suffix='.csv',
#           delimiter=',', is_binary=False, maxlhs=2, minsupport=2.5, out_suffix='')
#minority.compute_minority(froot='nursery', dir='../data/nursery')

#mine.mine_rules(din=din, froot=root, max_cardinality=max_cardinality,
#                min_support=min_support, labels=labels, suffix='_e', minor=minor)

