"""
http://www.nyclu.org/content/stop-and-frisk-data

"""
import os

import numpy as np
import tabular as tb

import mine


city_dict = {1: 'Manhattan', 2: 'Brooklyn', 3: 'Bronx', 4: 'Queens', 5: 'Staten Island'}

sex_dict = {0: 'female', 1: 'male'}

race_dict = {1: 'black', 2: 'black Hispanic', 3: 'white Hispanic', 4: 'white',
             5: 'Asian/Pacific Islander', 6: 'Am. Indian/Native'}

build_dict = {1: 'heavy', 2: 'musuclar', 3: 'medium', 4: 'thin'}

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
    else:
        return '>50'    # support = 978


din = os.path.join('..', 'data', 'frisk')
dout = os.path.join('..', 'data', 'CrossValidation')
zdata = os.path.join('..', 'data', '2014-20SQF.zip')
fdata = os.path.join(din, '2014-SQF-web.csv')
fout = os.path.join(din, 'frisk.csv')

seed = sum([1, 4, 21, 12, 20]) # f:6, r:18, i:09, s:19, k:11
num_folds = 10
max_cardinality = 2
min_support = 0.01
labels = ['no', 'yes']
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

print 'lightly process data (e.g., to make binary features)'
x = tb.tabarray(SVfile=fdata)
assert (len(x) == 45787)

assert not np.isnan(x['frisked']).any()
assert x['frisked'].sum() == 30345  # 66% frisked

assert not np.isnan(x['searched']).any()
assert x['searched'].sum() == 7283  # 16% searched

assert (x['frisked'] & x['searched']).sum() == 6667

assert (x['searched'] & np.invert(x['frisked'])).sum() == 616

weapon = x['pistol'] + x['riflshot'] + x['asltweap'] + x['knifcuti'] + x['machgun'] + x['othrweap']

assert np.isnan(weapon).sum() == 10860

assert not np.isnan(x['arstmade']).any()
assert x['arstmade'].sum() == 6898  # 15% arrested

assert len(set(x['year'])) == 1     # year of stop

assert len(set(x['pct'])) == 77     # precinct of stop
assert (x['pct'].min() >= 1) and (x['pct'].max() <= 123)

assert len(set(x['ser_num'])) == 2281   # UF-250 serial number

# datestop, timestop

assert set(x['city']) == set(range(1, 6))

assert np.isnan(x['sex']).sum() == 394

assert np.isnan(x['race']).sum() == 1039

# dob

assert np.isnan(x['age']).sum() == 107
assert (x['age'] >= 100).sum() == 27
assert x[x['age']==366]['dob']==6161978
x[x['age']==366]['age'] = 36
assert (x['age'] >= 90).sum() == 29     # the two entries in the 90s are ambiguous (see dob)
assert (x['age'] < 12).sum() == 99      # the single digit / younger ages seem like typos (see height, weight)

assert not np.isnan(x['height']).any()

assert not np.isnan(x['weight']).any()

assert np.isnan(x['haircolr']).sum() == 492

assert np.isnan(x['eyecolor']).sum() == 286

assert np.isnan(x['build']).sum() == 721

assert len(set(x['othfeatr'])) == 220

names = ['city', 'sex', 'race', 'age', 'build', 'frisked']

keep = np.invert(np.isnan(x[names].extract()).any(axis=1))
x = x[keep]
assert len(x) == 43858  # throw out 1929 records with missing data
x = x[(x['age'] > 11) & (x['age'] < 90)]     # throw out age extremes

age = [age_func(i) for i in x['age']]

columns = [x['city'], x['sex'], x['race'], age, x['build'], x['frisked']]

cnames = names

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
    cv_root = 'frisk_%d' % i
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
