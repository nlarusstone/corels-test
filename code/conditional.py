"""
Sanity check for Cynthia :)

"""

import numpy as np
import tabular as tb

x = tb.tabarray(SVfile='../data/adult_R.out', namesinheader=False)
rules = x['f0']

y = tb.tabarray(SVfile='../data/adult_R.label')
y = y[list(y.dtype.names[1:])].extract()

n = float(len(y))

m = np.cast[int](np.array(open('../data/adult_R.minor', 'rU').read().strip().split()[1:]))

z = x[list(x.dtype.names)[1:]].extract().T
s = np.array([str(tuple(i)) for i in z])

rr = tb.tabarray(columns=[s, y, np.ones(len(s), int)], names=['obs', 'label', 'count'])

q = tb.tabarray(SVfile='../queue/queue-8.txt', delimiter=' ')

d = dict(zip(rules, z.T))

i = 0
for (lower_bound, objective, length, frac_captured, rl) in q:
    rule_list = [r.split('~')[0] for r in rl.split(';')[:-1]]
    uncap = (np.array([d[r] for r in rule_list]).sum(axis=0) == 0)
    a = rr[uncap].aggregate(On='obs')
    mu = np.array([l if (l < (c - l)) else (c - l) for (l, c) in a[['label', 'count']]])
    assert (mu.sum() == m[uncap].sum())
    i += 1
    print i
