import numpy as np
import tabular as tb

x = tb.tabarray(SVfile='../data/adult_R.out', namesinheader=False)
rules = x['f0']

y = tb.tabarray(SVfile='../data/adult_R.label')
y = y[list(y.dtype.names[1:])].extract()

z = x[list(x.dtype.names)[1:]].extract().T
s = np.array([str(tuple(i)) for i in z])

r = tb.tabarray(columns=[s, y, np.ones(len(s), int)], names=['obs', 'label', 'count'])

a = r.aggregate(On='obs')
a.sort(order=['count'])
a = a[::-1]

# minority label count
m = np.array([l if (l < (c - l)) else (c - l) for (l, c) in a[['label', 'count']]])

# min error = 0.1112 (max accuracy = 0.8887 < 0.8888)
print float(m.sum()) / a['count'].sum()

# minority label for each equivalence class
ml = np.array([1 if (l < (c - l)) else 0 for (l, c) in a[['label', 'count']]])

d = dict(zip(a['obs'], ml))

# indicator for observation has minority label within equivalence set
ind = np.array([int(d[obs] == label) for (obs, label) in zip(r['obs'], y)])

assert (ind.sum() == m.sum())

f = open('../data/adult_R.minor', 'w')
f.write('{group_minority} ' + ' '.join([str(i) for i in ind]) + '\n')
f.close()

ms = m.copy()
ms.sort()
ms = ms[::-1]

print 'mean (min, max) minority support within an equivalence class: %1.3f (%d, %d)' % (ms.mean(), ms.min(), ms.max())
print 'number of equivalence classes with minority support > 10 : %d' % (ms > 10).sum()
print 'number of equivalence classes with minority support > 1 : %d' % (ms > 1).sum()
print 'number of equivalence classes with minority support > 0 : %d' % (ms > 0).sum()

"""
mean (min, max) minority support within an equivalence class: 0.318 (0, 75)
number of equivalence classes with minority support > 10 : 55
number of equivalence classes with minority support > 1 : 450
number of equivalence classes with minority support > 0 : 1120
"""
