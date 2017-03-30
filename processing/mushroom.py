"""
https://archive.ics.uci.edu/ml/datasets/Mushroom

https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/agaricus-lepiota.names

"""
import os

import numpy as np
import tabular as tb

import mine
import utils


din = os.path.join('..', 'data', 'mushroom')
dout = os.path.join('..', 'data', 'CrossValidation')
fdata = os.path.join(din, 'mushroom.data')
ftest = os.path.join(din, 'mushroom.test')
fnames = os.path.join(din, 'mushroom.names')
fcomplete = os.path.join(din, 'mushroom-filtered.csv')
bout = os.path.join('..', 'data', 'mushroom-binary.csv')
fout = os.path.join(din, 'mushroom.csv')

seed = sum([13, 21, 19, 8, 15, 15, 13]) # m:13 u:21 s:19 h:8 r:18 o:15 o:15 m:13
num_folds = 10
max_cardinality = 2
min_support = 0.1      # <-- might want to experiment with this
labels = ['edible', 'poisonous']
minor = False

np.random.seed(seed)

if not os.path.exists(din):
    os.mkdir(din)

if not os.path.exists(dout):
    os.mkdir(dout)

if not os.path.exists(fdata):
    print 'downloading data'
    uroot = 'https://archive.ics.uci.edu/ml/machine-learning-databases/mushroom/'
    os.system('wget %sagaricus-lepiota.data -O %s' % (uroot, fdata))
    os.system('wget %sagaricus-lepiota.names -O %s' % (uroot, fnames))

names = ['poisonous', 'cap-shape', 'cap-surface', 'cap-color', 'bruises', 'odor',
         'gill-attachment', 'gill-spacing', 'gill-size', 'gill-color', 'stalk-shape',
         'stalk-root', 'stalk-surface-above-ring', 'stalk-surface-below-ring',
         'stalk-color-above-ring', 'stalk-color-below-ring',
         'veil-type', 'veil-color', 'ring-number', 'ring-type',
         'spore-print-color', 'population', 'habitat']

print 'read original train data:', fdata
x = open(fdata, 'rU').read().strip().split('\n')
x = [','.join(line.split(', ')) for line in x] # if '?' not in line]   # filter out unknowns
assert (len(x) == 8124)

f = open(fcomplete, 'w')
f.write(','.join(names) + '\n')
f.write('\n'.join(x))
f.close()

print 'lightly process data (e.g., to make binary features)'
x = tb.tabarray(SVfile=fcomplete)

poisonous = np.cast[int](x[names[0]] == 'p')

y = x[names[1:]].colstack(tb.tabarray(columns=[poisonous], names=names[:1]))

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
    cv_root = 'mushroom_%d' % i
    test_root = '%s_test' % cv_root
    train_root = '%s_train' % cv_root
    ftest = os.path.join(dout, '%s.csv' % test_root)
    ftrain = os.path.join(dout, '%s.csv' % train_root)
    btest = os.path.join(dout, '%s-binary.csv' % test_root)
    btrain = os.path.join(dout, '%s-binary.csv' % train_root)
    train_ind = np.concatenate([split_ind[j] for j in range(num_folds) if (j != i)])
    y[split_ind[i]].saveSV(ftest)
    y[train_ind].saveSV(ftrain)
    b[split_ind[i]].saveSV(btest)
    b[train_ind].saveSV(btrain)

    print 'mine rules from', ftrain
    """
    num_rules[i] = mine.mine_binary(din=dout, froot=train_root,
                                   max_cardinality=max_cardinality,
                                   min_support=min_support,
                                   minor=minor)
    mine.apply_binary(din=dout, froot=cv_root)
    """

    num_rules[i] = mine.mine_rules(din=dout, froot=train_root,
                                   max_cardinality=max_cardinality,
                                   min_support=min_support,
                                   minor=minor, labels=labels)
    mine.apply_rules(din=dout, froot=cv_root, labels=labels)

print '(min, max) # rules mined per fold:', (num_rules.min(), num_rules.max())

#ben.driver(din='../data/mushroom', dout='../data/mushroom', froot='mushroom', train_suffix='.csv',
#           delimiter=',', is_binary=False, maxlhs=2, minsupport=2.5, out_suffix='')
#minority.compute_minority(froot='mushroom', dir='../data/mushroom')

#mine.mine_rules(din=din, froot=root, max_cardinality=max_cardinality,
#                min_support=min_support, labels=labels, suffix='_e', minor=minor)

