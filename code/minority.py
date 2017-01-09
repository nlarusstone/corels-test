import os

import numpy as np
import tabular as tb

def compute_minority(froot, dir='../data/'):
    fout = os.path.join(dir, '%s.out' % froot)
    flabel = os.path.join(dir, '%s.label' % froot)
    fminor = os.path.join(dir, '%s.minor' % froot)

    x = tb.tabarray(SVfile=fout, namesinheader=False)
    rules = x['f0']

    y = tb.tabarray(SVfile=flabel)
    y = y[list(y.dtype.names[1:])].extract()

    z = x[list(x.dtype.names)[1:]].extract().T
    s = np.array([str(tuple(i)) for i in z])

    r = tb.tabarray(columns=[s, y, np.ones(len(s), int)], names=['obs', 'label', 'count'])

    a = r.aggregate(On='obs')
    a.sort(order=['count'])
    a = a[::-1]

    # minority label count
    m = np.array([l if (l < (c - l)) else (c - l) for (l, c) in a[['label', 'count']]])

    print 'minimum error: %1.5f' % (float(m.sum()) / a['count'].sum())

    # minority label for each equivalence class
    ml = np.array([1 if (l < (c - l)) else 0 for (l, c) in a[['label', 'count']]])

    d = dict(zip(a['obs'], ml))

    # indicator for observation has minority label within equivalence set
    ind = np.array([int(d[obs] == label) for (obs, label) in zip(r['obs'], y)])

    assert (ind.sum() == m.sum())

    f = open(fminor, 'w')
    f.write('{group_minority} ' + ' '.join([str(i) for i in ind]) + '\n')
    f.close()

    ms = m.copy()
    ms.sort()
    ms = ms[::-1]

    print 'mean (min, max) minority support within an equivalence class: %1.3f (%d, %d)' % (ms.mean(), ms.min(), ms.max())
    print 'number of equivalence classes with minority support > 10 : %d' % (ms > 10).sum()
    print 'number of equivalence classes with minority support > 1 : %d' % (ms > 1).sum()
    print 'number of equivalence classes with minority support > 0 : %d' % (ms > 0).sum()

def adult_minority():
    """
    # minimum error: 0.11130
    mean (min, max) minority support within an equivalence class: 0.318 (0, 75)
    number of equivalence classes with minority support > 10 : 55
    number of equivalence classes with minority support > 1 : 450
    number of equivalence classes with minority support > 0 : 1120
    """
    compute_minority('adult_R')

def bcancer_minority():
    """
    minimum error: 0.01171
    mean (min, max) minority support within an equivalence class: 0.033 (0, 5)
    number of equivalence classes with minority support > 10 : 0
    number of equivalence classes with minority support > 1 : 1
    number of equivalence classes with minority support > 0 : 4
    """
    compute_minority('bcancer')

def cars_minority():
    """
    minimum error: 0.00000
    """
    compute_minority('cars')

def haberman_minority():
    """
    minimum error: 0.19281
    mean (min, max) minority support within an equivalence class: 0.738 (0, 4)
    number of equivalence classes with minority support > 10 : 0
    number of equivalence classes with minority support > 1 : 15
    number of equivalence classes with minority support > 0 : 32
    """
    compute_minority('haberman')

def monks1_minority():
    """
    minimum error: 0.00000
    """
    compute_minority('monks1')

def monks2_minority():
    """
    minimum error: 0.00000
    """
    compute_minority('monks2')

def monks3_minority():
    """
    minimum error: 0.00000
    """
    compute_minority('monks3')

def votes_minority():
    """
    minimum error: 0.00000
    """
    compute_minority('votes')

def compas_minority():
    """
    minimum error: 0.29623
    mean (min, max) minority support within an equivalence class: 3.273 (0, 92)
    number of equivalence classes with minority support > 10 : 54
    number of equivalence classes with minority support > 1 : 210
    number of equivalence classes with minority support > 0 : 299
    """
    compute_minority('compas')

def telco_minority():
    """
    minimum error: 0.05282
    mean (min, max) minority support within an equivalence class: 0.070 (0, 18)
    number of equivalence classes with minority support > 10 : 2
    number of equivalence classes with minority support > 1 : 45
    number of equivalence classes with minority support > 0 : 249
    """
    compute_minority('telco.shuffled')
