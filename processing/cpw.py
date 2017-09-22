"""
http://www1.nyc.gov/site/nypd/stats/reports-analysis/stopfrisk.page
http://www1.nyc.gov/assets/nypd/downloads/zip/analysis_and_planning/stop-question-frisk/sqf-2008-csv.zip

ntot: 2941390
cpw: 376488
cpw & weapon: 11531
cpw & (stopped/frisked): 325800
cpw & (stopped/frisked) & weapon: 10885
train size: 566839

cpwf & (stopped/frisked): 382030
cpwf & (stopped/frisked) & weapon: 14061

"""
import os

import numpy as np
import tabular as tb

import mine
import utils

def cpw_func(c):
    c = c.lower()
    if ('cpw' in c) or ('c.p.w.' in c):  #or ('gun' in c) or ('weapon' in c):
        return True
    return False

city_dict = {1: 'Manhattan', 2: 'Brooklyn', 3: 'Bronx', 4: 'Queens', 5: 'Staten-Island'}

sex_dict = {0: 'female', 1: 'male'}
def sex_func(s):
    if (s == 'M'):
        return 'male'
    elif (s == 'F'):
        return 'female'
    else:
        return 'other'  # not listed or unknown

race_dict = {1: 'black', 2: 'black-Hispanic', 3: 'white-Hispanic', 4: 'white',
             5: 'Asian-Pacific-Islander', 6: 'Am-Indian-Native'}

race_dict = {'A': 'Asian/Pacific Islander', 'B': 'Black',
             'I': 'American-Indian-or-Alaskan-Native',
             'P': 'Black-Hispanic', 'Q': 'White-Hispanic', 'W': 'White',
             'X': 'Unknown', 'Z': 'Other', ' ': 'Not Listed'}

# Table 1:  White, black, Hispanic, Asian or other
def race_func(r):
    if (r == 'A'):
        return 'Asian'  # Asian or Pacific Islander
    elif (r == 'B'):
        return 'Black'
    elif (r == 'W'):
        return 'White'
    elif (r in ['P', 'Q']):
        return 'Hispanic'
    else:
        return 'other'  # American Indian or Alaskan Native, Unknown, Other, Not Listed

stop_dict = {'cs_objcs': 'reason for stop - suspicious object',
             'cs_descr': 'reason for stop - fits description',
             'cs_casng': 'reason for stop - casing',
             'cs_lkout': 'reason for stop - acting as lookout',
             'cs_cloth': 'reason for stop - suspicious clothing',
             'cs_drgtr': 'reason for stop - drug transaction',
             'cs_furtv': 'reason for stop - furtive movements',
             'cs_vcrim': 'reason for stop - actions of violent crime',
             'cs_bulge': 'reason for stop - suspicious bulge',
             'cs_other': 'reason for stop - other',
             'ac_proxm': 'additional circumstances - proximity to crime scene',
             'ac_evasv': 'additional circumstances - evasive response',
             'ac_assoc': 'additional circumstances - associating with criminals',
             'ac_cgdir': 'additional circumstances - changed direction',
             'ac_incid': 'additional circumstances - high crime area',
             'ac_time' : 'additional circumstances - time of day',
             'ac_stsnd': 'additional circumstances - sights and sounds of criminal activity',
             'ac_rept' : 'additional circumstances - witness report',
             'ac_inves': 'additional circumstances - ongoing investigation',
             'ac_other': 'additional circumstances - other'}

inout_dict = {'O': 'outside', 'I': 'inside'}

def trhsloc_func(t):
    if (t == 'H'):
        return 'housing-authority'
    elif (t == 'T'):
        return 'transit-authority'
    else:
        return 'neither'

def rename_pos(s):
    return s.replace(' - ', '=').replace('reason for stop', 'stop-reason').replace('additional circumstances', 'circumstances').replace(' ', '-')

def rename_neg(s):
    return s.replace(' - ', '=not-').replace('reason for stop', 'stop-reason').replace('additional circumstances', 'circumstances').replace(' ', '-')

def age_func(a):
    if (a < 18):
        return '<18'    # support = 5630
    elif (a <= 21):
        return '18-21'  # support = 9960
    elif (a <= 25):
        return '22-25'  # support = 8044
    elif (a <= 30):
        return '26-30'  # support = 6222
    elif (a <= 40):
        return '31-40'  # support = 7115
    else:
        return '>40'    # support = 6776

def check_binary(c):
    if (c.dtype.str[1] == 'S'):
        if (c.dtype == np.dtype('S1')):
            sc = set(c)
            if (sc == set(['Y', 'N'])):
                return np.cast[int](c == 'Y')
            elif (sc == set(['N'])):
                return np.zeros(len(c))
        #c[c == ' '] = '_'   # missing string data --> will filter these
        return c
    else:
        return c

# for the weapon prediction problem, we resample due to class imbalance
resample_test = False   # if True, will resample the test set, otherwise only resample the train set

max_cardinality = 2
min_support = 0.001
exclude_not = True
froot = 'cpw'
use_cpw_func = True
include_loc = False
filter_frisk = True

din = os.path.join('..', 'data', froot)
dout = os.path.join('..', 'data', 'CrossValidation')
if not os.path.exists(din):
    os.mkdir(din)
if not os.path.exists(dout):
    os.mkdir(dout)

if use_cpw_func:
    froot = '%sf' % froot
if not include_loc:
    froot = '%s-noloc' % froot
if not filter_frisk:
    froot = '%s-nofilter' % froot

fout = os.path.join(din, '%s.csv' % froot)
bout = os.path.join('..', 'data', '%s-binary.csv' % froot)

seed = 42
num_folds = 10
labels = ['no', 'yes']
minor = True

np.random.seed(seed)

ntot = 0
ncpw = 0

for year in range(2008, 2013):

    fdata = os.path.join(din, '%d.csv' % year)
    zdata = os.path.join('..', 'data', 'sqf-%d-csv.zip' % year)

    if not os.path.exists(fdata):
        print 'downloading data'
        uroot = 'http://www1.nyc.gov/assets/nypd/downloads/zip/analysis_and_planning/stop-question-frisk/sqf-%d-csv.zip' % year
        os.system('wget %s -O %s' % (uroot, zdata))
        print 'unzipping data'
        os.system('unzip %s' % zdata)
        os.system('mv %d.csv %s' % (year, din))


    weapon_list = ['pistol', 'riflshot', 'asltweap', 'knifcuti', 'machgun', 'othrweap']
    usecols = ['pct', 'inout', 'trhsloc', 'crimsusp', 'frisked', 'searched'] + weapon_list + stop_dict.keys() + ['city'] #['sex', 'race', 'age', 'city']

    #usecols = [1,  6,  7,  9, 22, 23, 26, 27, 28, 29, 30, 31, 42, 43, 46, 48,
    #       49, 50, 51, 53, 54, 55, 56, 57, 59, 61, 62, 63, 64, 65, 67, 68, 99]
           #79, 80, 82, 99]

    #if (year >= 2011):
    #    usecols[-1] += 1

    print 'reading data'
    x = tb.tabarray(SVfile=fdata)#, usecols=usecols)
    print 'original:', len(x)
    ntot += len(x)
    print 'filter for columns of interest'
    x = x[usecols]
    print 'filter for records with CPW'
    if (use_cpw_func):
        ind = np.array([cpw_func(c) for c in x['crimsusp']])
        x = x[ind]
    else:
        x = x[x['crimsusp'] == 'CPW']
    print 'lightly process data (e.g., to make binary features)'
    x = tb.tabarray(columns=[check_binary(x[n]) for n in x.dtype.names], names=x.dtype.names)

    print 'CPW:', len(x)
    ncpw += len(x)
    print 'frisked:', x['frisked'].sum()
    print 'searched:', x['searched'].sum()
    print 'frisked & searched:', (x['frisked'] & x['searched']).sum()
    print 'searched & not frisked:', (x['searched'] & np.invert(x['frisked'])).sum() 

    w = x[weapon_list].extract()
    (ii, jj) = np.isnan(w).nonzero()
    w[ii, jj] = 0
    weapon = w.any(axis=1)
    print 'weapon:', weapon.sum()
    print 'searched & weapon:', (x['searched'] & weapon).sum()
    print 'frisked & weapon:', (x['frisked'] & weapon).sum()
    print 'searched | frisked:', (x['searched'] | x['frisked']).sum()
    assert '(searched | frisked) & weapon', ((x['searched'] | x['frisked']) & weapon).sum()

    #print 'arrest:', x['arstmade'].sum()

    stop_reasons = [n for n in x.dtype.names if (n.startswith('cs') or n.startswith('ac'))
                                          and ('other' not in n)] # or n.startswith('ac'))
    for sr in stop_reasons:
        x[sr][np.isnan(x[sr]).nonzero()[0]] = 0

    if filter_frisk:
        ikeep = (x['searched'] == 1) | (x['frisked'] == 1)
        x = x[ikeep]
        weapon = weapon[ikeep]

    weapon = np.cast[int](weapon)
    #sex = np.array([sex_func(i) for i in x['sex']])
    #race = np.array([race_func(i) for i in x['race']])
    #age = np.array([age_func(i) for i in x['age']])
    inout = np.array([inout_dict[i] for i in x['inout']])

    if include_loc:
        city = x['city']
        city[city == 'STATEN ISLAND'] = 'STATEN-ISLAND'
        city[city == 'STATEN IS'] = 'STATEN-ISLAND'
        city[city == ' '] = '-'
        location = np.array([trhsloc_func(i) for i in x['trhsloc']])

    stop_reasons_list = []
    for sr in stop_reasons:
        stop_reasons_list += [[rename_pos(stop_dict[sr]) if s else rename_neg(stop_dict[sr]) for s in x[sr]]]

    if include_loc:
        columns = stop_reasons_list + [city, location, inout, weapon]
        cnames = stop_reasons + ['city', 'location', 'inout', 'weapon']
    else:
        columns = stop_reasons_list + [inout, weapon]
        cnames = stop_reasons + ['inout', 'weapon']

    fyear = fout.replace('.csv', ('-%d.csv' % year))
    print 'write categorical dataset', fyear
    y = tb.tabarray(columns=columns, names=cnames)
    y.saveSV(fyear)

print 'ntot:', ntot
print 'ncpw:', ncpw
print 'concatenate files'
fy = fout.replace('.csv', '-2008.csv')
cmd = 'head -1 %s > %s' % (fy, fout)
print cmd
os.system(cmd)
ff = fout.replace('.csv', '-*.csv')
cmd = 'ls %s' % ff
print cmd
os.system(cmd)
cmd = 'tail -n +2 -q %s >> %s' % (ff, fout)
print cmd
os.system(cmd)

print 'read categorical dataset'
y = tb.tabarray(SVfile=fout)
print 'total:', len(y)
y0 = y[y['weapon'] == 0]
y1 = y[y['weapon'] == 1]
y = y0.rowstack(y1)
print 'weapon:', len(y1)

print 'write binary dataset', bout
b = utils.to_binary(y)
b.saveSV(bout)

s0 = np.split(np.random.permutation(len(y0) / num_folds * num_folds), num_folds)
s1 = np.split(len(y0) + np.random.permutation(len(y1) / num_folds * num_folds), num_folds)
test_split_ind = [np.concatenate([i0, i1]) for (i0, i1) in zip(s0, s1)]
s1 = [i1[np.random.randint(0, len(i1), len(s0[0]))] for i1 in s1]
split_ind = [np.concatenate([i0, i1]) for (i0, i1) in zip(s0, s1)]

print 'permute and partition dataset'
print 'number of folds:', num_folds

num_rules = np.zeros(num_folds, int)
for i in range(num_folds):
    print 'generate cross-validation split', i
    cv_root = '%s_%d' % (froot, i)
    test_root = '%s_test' % cv_root
    train_root = '%s_train' % cv_root
    ftest = os.path.join(dout, '%s.csv' % test_root)
    ftrain = os.path.join(dout, '%s.csv' % train_root)
    btest = os.path.join(dout, '%s-binary.csv' % test_root)
    btrain = os.path.join(dout, '%s-binary.csv' % train_root)
    train_ind = np.concatenate([split_ind[j] for j in range(num_folds) if (j != i)])
    y[train_ind].saveSV(ftrain)
    b[train_ind].saveSV(btrain)
    if resample_test:
        y[split_ind[i]].saveSV(ftest)
        b[split_ind[i]].saveSV(btest)
    else:
        y[test_split_ind[i]].saveSV(ftest)
        b[test_split_ind[i]].saveSV(btest)

    print 'mine rules from', ftrain
    num_rules[i] = mine.mine_rules(din=dout, froot=train_root,
                                    max_cardinality=max_cardinality,
                                    min_support=min_support, labels=labels,
                                    minor=minor, exclude_not=exclude_not)
    mine.apply_rules(din=dout, froot=cv_root, labels=labels)

print '(min, max) # rules mined per fold:', (num_rules.min(), num_rules.max())

print 'train size:', len(train_ind)
print 'test size:', len(test_split_ind[0])
print 'resampled test size:', len(split_ind[0])
