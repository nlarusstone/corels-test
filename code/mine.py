import itertools
import os

import numpy as np
import tabular as tb

import minority


din = '../data/adult'
froot = 'adult'
labels = ['<=50K', '>50K']
max_cardinality = 2
min_support = 0.01

fin = os.path.join(din, '%s.csv' % froot)
fout = os.path.join(din, '%s_e.out' % froot)
flabel = os.path.join(din, '%s_e.label' % froot)
fminor = os.path.join(din, '%s_e.minor' % froot)

x = tb.tabarray(SVfile=fin)
features = list(x.dtype.names)[:-1]
label_name = x.dtype.names[-1]
ndata = len(x)
min_threshold = ndata * min_support
max_threshold = ndata * (1. - min_support)

records = []
names = []
udict = {}
for n in features:
    ulist = tb.utils.uniqify(x[n])
    udict[n] = []
    for u in ulist:
        bvec = (x[n] == u)
        supp = bvec.sum()
        if ((supp > min_threshold) and (supp < max_threshold)):
            names += ['{%s:%s}' % (n, u)]
            udict[n] += [u]
            records += [bvec]

for cardinality in range(2, max_cardinality + 1):
    for dlist in list(itertools.combinations(features, cardinality)):
        for values in list(itertools.product(*[udict[d] for d in dlist])):
            bvec = np.array([(x[d] == v) for (d, v) in zip(dlist, values)]).all(axis=0)
            supp = bvec.sum()
            if ((supp > min_threshold) and (supp < max_threshold)):
                descr = '{%s}' % ','.join(['%s:%s' % (d, v) for (d, v) in zip(dlist, values)])
                names.append(descr)
                records.append(bvec)
                print descr

print len(names), 'rules mined'
print 'writing', fout
f = open(fout, 'w')
f.write('\n'.join(['%s %s' % (n, ' '.join(np.cast[str](np.cast[int](r))))
                   for (n, r) in zip(names, records)]) + '\n')
f.close()

print 'writing', flabel
recs = [(x[label_name] == 0), (x[label_name] == 1)]
f = open(flabel, 'w')
f.write('\n'.join(['{%s:%s} %s' % (label_name, l, ' '.join(np.cast[str](np.cast[int](r))))
                   for (l, r) in zip(labels, recs)]) + '\n')
f.close()

print 'computing', fminor
minority.compute_minority(froot='%s_e' % froot, dir=din)
