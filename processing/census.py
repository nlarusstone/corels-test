"""
See https://archive.ics.uci.edu/ml/datasets/US+Census+Data+(1990)

Income and earning fields from https://archive.ics.uci.edu/ml/machine-learning-databases/census1990-mld/USCensus1990raw.attributes.txt

AINCOME1     C       X      1             Wages and Salary Inc. Allocation Flag
AINCOME2     C       X      1             Nonfarm Self Employment Inc. Allocation
AINCOME3     C       X      1             Farm Self Employment Inc. Allocation Fla
AINCOME4     C       X      1             Int., Dividend, and Net Rental Inc. Allo
AINCOME5     C       X      1             Soc. Sec Inc. Allocation Flag
AINCOME6     C       X      1             Pub. Asst. Allocation Flag
AINCOME7     C       X      1             Ret. Inc. Allocation Flag
AINCOME8     C       X      1             All Other Inc. Allocation Flag
RPINCOME     C       X      6             Total Pers. Inc. Signed
REARNING     C       X      6             Total Pers. Earnings

dRearning < dRincome about 18% of the time

create function discRpincome( @arg varchar(255) )
RETURNS int
AS
BEGIN
  DECLARE @value bigint
  DECLARE @ret int
  SET @value = @arg

  IF @value = 0             <-- Discard (32%) (1677761 with positive income)
     SET @ret = 0
  ELSE IF @value <0         <-- Discard (0.1 %) can be negative
     SET @ret = 1
  ELSE IF @value <15000     <-- (35%)
     SET @ret = 2
  ELSE IF @value <30000     <-- (19%)
     SET @ret = 3
  ELSE IF @value <60000     <-- (11%)
     SET @ret = 4
  ELSE                      <-- (3%)
     SET @ret = 5
RETURN(@ret)
END


We focus on Wages and Salary (Income 1).  Discretization function from

https://archive.ics.uci.edu/ml/machine-learning-databases/census1990-mld/USCensus1990.mapping.sql

create function discIncome1( @arg varchar(255) )
RETURNS int
AS
BEGIN
  DECLARE @value bigint
  DECLARE @ret int
  SET @value = @arg

  IF @value = 0             <-- Discard these records (1220882 remaining)
     SET @ret = 0
  ELSE IF @value <15000     <-- Class label 0 (46%)
     SET @ret = 1
  ELSE IF @value <30000     <-- Class label 1 (31%)
     SET @ret = 2
  ELSE IF @value <60000     <-- Class label 1 (19%)
     SET @ret = 3
  ELSE
     SET @ret = 4           <-- Class label 1 (4%)
RETURN(@ret)
END
"""
import os

import numpy as np
import tabular as tb

import mine
import utils


seed = 81
num_folds = 10
max_cardinality = 1
min_support = 0.01
prefix = ''

labels = ['<15K', '>=15K']
minor = False

din = os.path.join('..', 'data', 'census')
dout = os.path.join('..', 'data', 'CrossValidation')
fin = os.path.join(din, 'USCensus1990.data.txt')
fattr = os.path.join(din, 'USCensus1990.attributes.txt')
fsql = os.path.join(din, 'USCensus1990.mapping.sql')
freadme = os.path.join(din, 'USCensus1990.readme.txt')
fsub = os.path.join(din, 'USCensus1990.subset.txt')
fraw = os.path.join(din, 'USCensus1990raw.attributes.txt')
fout = os.path.join(din, 'census.csv')
bout = os.path.join('..', 'data', 'census-binary.csv')

if not os.path.exists(din):
    os.mkdir(din)

if not os.path.exists(fin):
    uroot = 'https://archive.ics.uci.edu/ml/machine-learning-databases/census1990-mld/'
    udata = uroot + 'USCensus1990.data.txt'
    uattr = uroot + 'USCensus1990.attributes.txt'
    usql = uroot + 'USCensus1990.mapping.sql'
    ureadme = uroot + 'USCensus1990.readme.txt'
    uraw = uroot + 'USCensus1990raw.attributes.txt'
    os.system('wget %s -O %s' % (udata, fin))
    os.system('wget %s -O %s' % (uattr, fattr))
    os.system('wget %s -O %s' % (usql, fsql))
    os.system('wget %s -O %s' % (ureadme, freadme))
    os.system('wget %s -O %s' % (uraw, fraw))

label_name = 'dRpincome'

ntot = 2458285
np.random.seed(seed)
fh = open(fin, 'rU')
header = fh.readline()
lines = [header]
ind = header.strip().split(',').index(label_name)

# select random subset so that 10-fold cross-validation training sets have
# 1 million points, i.e., subset of size 1111112
"""
ii = np.random.permutation(ntot)[:(10**6*10/9 + 1)]
ii.sort()
j = 0
for i in ii:
    while (i < j):
        j += 1
        fh.readline()
    lines.append(fh.readline())

"""

print 'selecting individuals with positive total income'
for i in range(ntot):
    line = fh.readline()
    if (line.strip().split(',')[ind] in ['0', '1']):
        continue
    lines.append(line)

print 'printing subset file with', len(lines) - 1, 'records'
fh.close()
gh = open(fsub, 'w')
gh.write(''.join(lines))
gh.close()

print 'reading subset file'
x = tb.tabarray(SVfile=fsub)

d = dict()
ncat = 0
for name in x.dtype.names[1:]:
    nc = x[name].max() + 1
    ncat += nc
    d[name] = nc
    print name, nc

print 'num attributes:', len(x.dtype.names[1:])
print 'num categories:', ncat

# ignore `caseid` field and use `dIncome1` as class labels
# binarize labels s.t. 1 maps to 0 and >1 maps to 1
# don't include other fields for income or earnings
names = list(x.dtype.names)
names = [nn for nn in names[1:ind] + names[(ind + 1):] if ('income' not in nn.lower()) and ('earning' not in nn.lower())]
names += [label_name]
x = x[names]
z = np.ones(len(x), int)
z[x[label_name] == 2] = 0
x[label_name] = z

print 'write categorical dataset', fout
x.saveSV(fout)

print 'write binary dataset', bout
b = utils.to_binary(x)
b.saveSV(bout)

print 'permute and partition dataset'
split_ind = np.split(np.random.permutation(len(x) / num_folds * num_folds), num_folds)
print 'number of folds:', num_folds
print 'train size:', len(split_ind[0]) * (num_folds - 1)
print 'test size:', len(split_ind[0])

num_rules = np.zeros(num_folds, int)
for i in range(num_folds):
    print 'generate cross-validation split', i
    cv_root = 'census_%d' % i
    test_root = '%s_test' % cv_root
    train_root = '%s_train' % cv_root
    ftest = os.path.join(dout, '%s.csv' % test_root)
    ftrain = os.path.join(dout, '%s.csv' % train_root)
    btest = os.path.join(dout, '%s-binary.csv' % test_root)
    btrain = os.path.join(dout, '%s-binary.csv' % train_root)
    train_ind = np.concatenate([split_ind[j] for j in range(num_folds) if (j != i)])
    x[split_ind[i]].saveSV(ftest)
    x[train_ind].saveSV(ftrain)
    b[split_ind[i]].saveSV(btest)
    b[train_ind].saveSV(btrain)
    print 'mine rules from', ftrain
    num_rules[i] = mine.mine_rules(din=dout, froot=train_root,
                                   max_cardinality=max_cardinality,
                                   min_support=min_support, labels=labels,
                                   minor=minor, prefix=prefix)
    mine.apply_rules(din=dout, froot=cv_root, labels=labels, prefix=prefix, numerical=True)

print '(min, max) # rules mined per fold:', (num_rules.min(), num_rules.max())
