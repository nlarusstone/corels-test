"""
| Split into train-test using MLC++ GenCVFiles (2/3, 1/3 random).
| 48842 instances, mix of continuous and discrete    (train=32561, test=16281)
| 45222 if instances with unknown values are removed (train=30162, test=15060)
| Duplicate or conflicting instances : 6
| Class probabilities for adult.all file
| Probability for the label '>50K'  : 23.93% / 24.78% (without unknowns)
| Probability for the label '<=50K' : 76.07% / 75.22% (without unknowns)

age: continuous.
workclass: Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked.
fnlwgt: continuous.
education: Bachelors, Some-college, 11th, HS-grad, Prof-school, Assoc-acdm, Assoc-voc, 9th, 7th-8th, 12th, Masters, 1st-4th, 10th, Doctorate, 5th-6th, Preschool.
education-num: continuous.
marital-status: Married-civ-spouse, Divorced, Never-married, Separated, Widowed, Married-spouse-absent, Married-AF-spouse.
occupation: Tech-support, Craft-repair, Other-service, Sales, Exec-managerial, Prof-specialty, Handlers-cleaners, Machine-op-inspct, Adm-clerical, Farming-fishing, Transport-moving, Priv-house-serv, Protective-serv, Armed-Forces.
relationship: Wife, Own-child, Husband, Not-in-family, Other-relative, Unmarried.
race: White, Asian-Pac-Islander, Amer-Indian-Eskimo, Other, Black.
sex: Female, Male.
capital-gain: continuous.
capital-loss: continuous.
hours-per-week: continuous.
native-country: United-States, Cambodia, England, Puerto-Rico, Canada, Germany, Outlying-US(Guam-USVI-etc), India, Japan, Greece, South, China, Cuba, Iran, Honduras, Philippines, Italy, Poland, Jamaica, Vietnam, Mexico, Portugal, Ireland, France, Dominican-Republic, Laos, Ecuador, Taiwan, Haiti, Columbia, Hungary, Guatemala, Nicaragua, Scotland, Thailand, Yugoslavia, El-Salvador, Trinadad&Tobago, Peru, Hong, Holand-Netherlands.
income: >50K, <=50K.
"""
import os

import numpy as np
import tabular as tb

import mine


def age_func(a):
    if (a < 30):
        return '<30'
    elif (a < 50):
        return '30-50'
    elif (a < 65):
        return '51-65'
    else:
        return '>65'

def capital_gain_func(c):
    if (c >= 7298):
        return '>=7298'
    else:
        return '<7298'

def hours_func(h):
    if (h < 40):
        return '<40'
    elif (h == 40):
        return '40'
    else:
        return '>40'


din = os.path.join('..', 'data', 'adult')
dout = os.path.join('..', 'data', 'CrossValidation')
fdata = os.path.join(din, 'adult.data')
ftest = os.path.join(din, 'adult.test')
fnames = os.path.join(din, 'adult.names')
fcomplete = os.path.join(din, 'adult-filtered.csv')
fout = os.path.join(din, 'adult.csv')

seed = sum([1, 4, 21, 12, 20]) # a:1, d:4, u:21, l:12, t:20
num_folds = 10
max_cardinality = 2
min_support = 0.045 # target 300 mined rules
labels = ['<=50K', '>50K']
minor = True


np.random.seed(seed)

if not os.path.exists(din):
    os.mkdir(din)

if not os.path.exists(dout):
    os.mkdir(dout)

if not os.path.exists(fdata):
    print 'downloading data'
    uroot = 'https://archive.ics.uci.edu/ml/machine-learning-databases/adult/'
    os.system('wget %sadult.data -O %s' % (uroot, fdata))
    os.system('wget %sadult.test -O %s' % (uroot, ftest))
    os.system('wget %sadult.names -O %s' % (uroot, fnames))

names = ['age', 'workclass', 'fnlwgt', 'education', 'education-num',
         'marital-status', 'occupation', 'relationship', 'race', 'sex',
         'capital-gain', 'capital-loss', 'hours-per-week', 'native-country',
         'income']

print 'read original train data:', fdata
x = open(fdata, 'rU').read().strip().split('\n')
x = [','.join(line.split(', ')) for line in x if '?' not in line]
assert (len(x) == 30162)

print 'read original test data:', ftest
z = open(ftest, 'rU').read().strip().split('\n')[1:]
z = [','.join(line.split(', ')).strip('.') for line in z if '?' not in line]
assert (len(z) == 15060)

print 'concatenate train and test:', fcomplete
f = open(fcomplete, 'w')
f.write(','.join(names) + '\n')
f.write('\n'.join(x + z))
f.close()

print 'lightly process data (e.g., to make binary features)'
x = tb.tabarray(SVfile=fcomplete)

age = np.array([age_func(a) for a in x['age']])

capital_gain  = np.array([capital_gain_func(c) for c in x['capital-gain']])

capital_loss = np.array(['>0' if (c > 0) else '=0' for c in x['capital-loss']])

hours_per_week = np.array([hours_func(h) for h in x['hours-per-week']])

income = np.cast[int](x['income'] == '>50K')

columns = [age, x['workclass'], x['education'], x['marital-status'], x['occupation'],
           x['relationship'], x['race'], x['sex'], capital_gain, capital_loss,
           hours_per_week, x['native-country'], income]

names = ['age', 'workclass', 'education', 'marital-status', 'occupation',
         'relationship', 'race', 'sex', 'capital-gain', 'capital-loss',
         'hours-per-week', 'native-country', 'income']

print 'write binary dataset', fout
y = tb.tabarray(columns=columns, names=names)
y.saveSV(fout)

print 'permute and partition dataset'
split_ind = np.split(np.random.permutation(len(y) / num_folds * num_folds), num_folds)
print 'number of folds:', num_folds
print 'train size:', len(split_ind[0]) * (num_folds - 1)
print 'test size:', len(split_ind[0])

num_rules = np.zeros(num_folds, int)
for i in range(num_folds):
    print 'generate cross-validation split', i
    cv_root = 'adult_%d' % i
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

#ben.driver(din='../data/adult', dout='../data/adult', froot='adult', train_suffix='.csv',
#           delimiter=',', is_binary=False, maxlhs=2, minsupport=2.5, out_suffix='')
#minority.compute_minority(froot='adult', dir='../data/adult')

#mine.mine_rules(din=din, froot=root, max_cardinality=max_cardinality,
#                min_support=min_support, labels=labels, suffix='_e', minor=minor)
