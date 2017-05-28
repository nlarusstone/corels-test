"""
See https://archive.ics.uci.edu/ml/datasets/US+Census+Data+(1990)

**Consider thresholds instead of ranges**

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
POVERTY      C       X      3             Pers. Poverty Stat. Recode See Appendix

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

Example rule lists:

if ({dHour89:1}) then ({dRpincome:<15K})        # objective: 0.28208
else if ({dWeek89:2}) then ({dRpincome:>=15K})  # accuracy:  0.73792
else ({dRpincome:<15K})

if ({dHour89:1}) then ({dRpincome:<15K})        # objective: 0.27933
else if ({dPoverty:1}) then ({dRpincome:<15K})  # accuracy:  0.75067
else if ({dHours:0}) then ({dRpincome:<15K})
else ({dRpincome:>=15K})

if ({dHour89:1}) then ({dRpincome:<15K})        # objective: 0.27882
else if ({dPoverty:1}) then ({dRpincome:<15K})  # accuracy:  0.76118
else if ({dAge:2}) then ({dRpincome:<15K})
else if ({iYearwrk:1}) then ({dRpincome:>=15K})
else ({dRpincome:<15K})


HOUR89       C       X      2             Usual Hrs. Worked Per Week Last Yr. 1989
                                  00      N/a Less Than 16 Yrs. Old/did Not Work i
                                  99      99 or More Usual Hrs.

WEEK89       C       X      2             Wks. Worked Last Yr. 1989
                                  00      N/a Less Than 16 Yrs. Old/did Not Work i

POVERTY      C       X      3             Pers. Poverty Stat. Recode See Appendix
                                  000     N/a
                                  501     501% or More of Poverty Value

HOURS        C       X      2             Hrs. Worked Last Week
                                  00      N/a Less Than 16 Yrs. Old/not At Work/un
                                  99      99 or More Hrs. Worked Last Week

YEARWRK      C       X      1             Yr. Last Worked
                                  0       N/a Less Than 16 Yrs. Old
                                  1       1990
                                  2       1989
                                  3       1988
                                  4       1985 to 1987
                                  5       1980 to 1984
                                  6       1979 or Earlier
                                  7       Never Worked

create function discHour89( @arg varchar(255) )
RETURNS int
AS
BEGIN
  DECLARE @value bigint
  DECLARE @ret int
  SET @value = @arg

  IF @value = 0
     SET @ret = 0
  ELSE IF @value <30
     SET @ret = 1
  ELSE IF @value <40
     SET @ret = 2
  ELSE IF @value <41
     SET @ret = 3
  ELSE IF @value <50
     SET @ret = 4
  ELSE
     SET @ret = 5
RETURN(@ret)
END

create function discWeek89( @arg varchar(255) )
RETURNS int
AS
BEGIN
  DECLARE @value bigint
  DECLARE @ret int
  SET @value = @arg

  IF @value = 0
     SET @ret = 0
  ELSE IF @value < 52
     SET @ret = 1
  ELSE
     SET @ret = 2
RETURN(@ret)
END

create function discPoverty( @arg varchar(255) )
RETURNS int
AS
BEGIN
  DECLARE @value bigint
  DECLARE @ret int
  SET @value = @arg

  IF @value = 0
     SET @ret = 0
  ELSE IF @value <100
     SET @ret = 1
  ELSE
     SET @ret = 2
RETURN(@ret)
END

create function discHours( @arg varchar(255) )
RETURNS int
AS
BEGIN
  DECLARE @value bigint
  DECLARE @ret int
  SET @value = @arg

  IF @value = 0
     SET @ret = 0
  ELSE IF @value <30
     SET @ret = 1
  ELSE IF @value <40
     SET @ret = 2
  ELSE IF @value <41
     SET @ret = 3
  ELSE IF @value <50
     SET @ret = 4
  ELSE
     SET @ret = 5
RETURN(@ret)
END

create function discAge( @arg varchar(255) )
RETURNS int
AS
BEGIN
  DECLARE @value bigint
  DECLARE @ret int
  SET @value = @arg

  IF @value = 0
     SET @ret = 0
  ELSE IF @value <13
     SET @ret = 1
  ELSE IF @value <20
     SET @ret = 2
  ELSE IF @value <30
     SET @ret = 3
  ELSE IF @value <40
     SET @ret = 4
  ELSE IF @value <50
     SET @ret = 5
  ELSE IF @value <65
     SET @ret = 6
  ELSE
     SET @ret = 7
RETURN(@ret)
END

"""
import os

import numpy as np
import tabular as tb

import mine
import utils

def threshold_func(col, vals, descr):
    columns = []
    names = []
    if (vals[0] == 0):
        columns += [np.cast[int](col == 0)]
        names += ['%s=0' % descr]
        vals = vals[1:]
    for v in vals:
        columns += [np.cast[int](col <= v)]
        names += ['%s<%d' % (descr, v)]
    return tb.tabarray(columns=columns, names=names)

# 'dIncome1': [0, 15000, 30000, 60000]
# 'dPoverty': [0, 100]
# 'dRearning': [0, 15000, 30000, 60000]
# 'dRpincome': ['0', '<0', '<15000', '<30000', '<60000', '>=60000']

threshold_dict = {'dAge': [0, 13, 20, 30, 40, 50, 65],
                  'dDepart': [0, 600, 700, 800, 1000],
                  'dHour89': [0, 30, 40, 41, 50],
                  'dHours': [0, 30, 40, 41, 50],
                  'dPwgt1': [50, 125, 200],
                  'dTravtime': [0, 10, 15, 20, 30, 60],
                  'dWeek89': [0, 52],
                  'dYrsserv': [0, 5]}

# also consider:  iFertil, iRiders

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
names = [nn for nn in names[1:ind] + names[(ind + 1):] if (nn not in threshold_dict.keys())
         and ('income' not in nn.lower()) and ('earning' not in nn.lower())
         and ('poverty' not in nn.lower())]

print 'compute thresholds'
for (i, nn) in enumerate(threshold_dict.keys()):
    print nn
    if (i == 0):
        y = threshold_func(x[nn], threshold_dict[nn], nn)
    else:
        y = y.colstack(threshold_func(x[nn], threshold_dict[nn], nn))

print 'get class labels'
z = np.ones(len(x), int)
z[x[label_name] == 2] = 0

x = y.colstack(x[names]).colstack(tb.tabarray(columns=[z], names=[label_name]))
print x.dtype.names

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
