"""
http://www.nyclu.org/content/stop-and-frisk-data

"""
import os

import numpy as np
import tabular as tb

import mine


def age_func(a):
    if (a <=25):
        return '<=25'
    elif (a <= 45):
        return '26-45'
    elif (a <=75):
        return '46-75'
    else:
        return '>75'

def workclass_func(w):
    if ('gov' in w):
        return 'Government'
    elif w.startswith('Self'):
        return 'Self-employed'
    else:
        assert (w in ['Private', 'Without-pay']), w
        return w

def education_func(s):
    if (s in ['Preschool', '1st-4th', '5th-6th', '7th-8th']):   # education-num = 1-4
        return 'At-most-middle-school'
    elif (s in ['9th', '10th', '11th', '12th']):                # education-num = 5-8
        return 'Some-high-school'
    elif ('Assoc' in s):                                        # education-num = 11-12
        return 'Assoc-degree'
    elif (s in ['Prof-school', 'Masters', 'Doctorate']):        # education-num = 14-16
        return 'Grad-school'
    else:
        assert (s in ['HS-grad', 'Some-college', 'Bachelors'])  # education-num = 9-10, 13
        return s

def marital_status_func(m):
    if (m in ['Married-AF-spouse', 'Married-civ-spouse']):
        return 'Married'
    elif (m == 'Never-married'):
        return m
    else:
        assert (m in ['Divorced', 'Widowed', 'Separated', 'Married-spouse-absent']), m
        return 'No-longer-with-spouse'

def capital_gain_func(c):
    if (c >= 7298):
        return '>=7298'
    else:
        return '<7298'

def hours_func(h):
    if (h <= 25):
        return '<=25'
    elif (h <= 40):
        return '26-40'
    elif (h < 60):
        return '41-60'
    else:
        return '>60'

def native_country_func(c):
    if (c == 'United-States'):
        return c
    else:
        return 'Not-United-States'

din = os.path.join('..', 'data', 'frisk')
dout = os.path.join('..', 'data', 'CrossValidation')
zdata = os.path.join('..', 'data', '2014-20SQF.zip')
fdata = os.path.join(din, '2014-SQF-web.csv')
fcomplete = os.path.join(din, 'frisk-filtered.csv')
fout = os.path.join(din, 'frisk.csv')

seed = sum([1, 4, 21, 12, 20]) # f:6, r:18, i:09, s:19, k:11
num_folds = 10
max_cardinality = 1
min_support = 0.01
labels = ['<=50K', '>50K']
minor = True


np.random.seed(seed)

if not os.path.exists(din):
    os.mkdir(din)

if not os.path.exists(dout):
    os.mkdir(dout)

if not os.path.exists(fdata):
    print 'downloading data'
    uroot = 'http://www.nyclu.org/files/2014%20SQF.zip'
    os.system('wget %s -O %s' % (uroot, zdata))
    print 'unzipping data'
    os.system('unzip %s' % zdata)
    os.system('mv 2014\ SQF/* %s' % din)
    print 'renaming files'
    for f in os.listdir(din):
        f1 = os.path.join(din, f)
        f2 = f1.replace(' ', '-').replace('_', '-')
        f1 = f1.replace(' ', '\\ ')
        os.system('mv %s %s' % (f1, f2))

print 'read downloaded data:', fdata
x = open(fdata, 'rU').read().strip().split('\n')
x = [','.join(line.split(', ')) for line in x if '?' not in line]
assert (len(x) == 45787)

"""
names = ['age', 'workclass', 'fnlwgt', 'education', 'education-num',
         'marital-status', 'occupation', 'relationship', 'race', 'sex',
         'capital-gain', 'capital-loss', 'hours-per-week', 'native-country',
         'income']

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

workclass = np.array([workclass_func(w) for w in x['workclass']])

education = np.array([education_func(s) for s in x['education']])

marital_status = np.array([marital_status_func(m) for m in x['marital-status']])

capital_gain  = np.array([capital_gain_func(c) for c in x['capital-gain']])

capital_loss = np.array(['>0' if (c > 0) else '=0' for c in x['capital-loss']])

hours_per_week = np.array([hours_func(h) for h in x['hours-per-week']])

native_country = np.array([native_country_func(c) for c in x['native-country']])

income = np.cast[int](x['income'] == '>50K')

columns = [age, workclass, education, marital_status, x['occupation'],
           x['relationship'], x['race'], x['sex'], capital_gain, capital_loss,
           hours_per_week, native_country, income]

names = ['age', 'workclass', 'education', 'marital-status', 'occupation',
         'relationship', 'race', 'sex', 'capital-gain', 'capital-loss',
         'hours-per-week', 'native-country', 'income']

print 'write categorical dataset', fout
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

"""