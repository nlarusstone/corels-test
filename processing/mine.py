import itertools
import os

import numpy as np
import tabular as tb


def mine_rules(din='../data/adult', froot='adult', max_cardinality=2,
               min_support=0.01, labels=['<=50K', '>50K'], minor=True,
               verbose=False, suffix=''):

    fin = os.path.join(din, '%s.csv' % froot)
    fout = os.path.join(din, '%s%s.out' % (froot, suffix))
    flabel = os.path.join(din, '%s%s.label' % (froot, suffix))

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
                    if (verbose):
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

    if (minor):
        import minority
        fminor = os.path.join(din, '%s%s.minor' % (froot, suffix))
        print 'computing', fminor
        minority.compute_minority(froot='%s%s' % (froot, suffix), dir=din)

    return len(names)

def apply_rules(din='../data/adult', froot='adult', labels=['<=50K', '>50K']):

    ftrain = os.path.join(din, '%s-train.out' % froot)
    ftest = os.path.join(din, '%s-test.csv' % froot)
    fout = os.path.join(din, '%s-test.out' % froot)
    flabel = os.path.join(din, '%s-test.label' % froot)

    x = tb.tabarray(SVfile=ftest)
    names = x.dtype.names
    label_name = names[-1]
    y = x[label_name]
    x = x.extract()
    d = dict(zip(names, [x[:,i] for i in range(len(names))]))

    print 'reading rules from', ftrain
    rule_descr = [line.strip().split()[0] for line in open(ftrain, 'rU').read().strip().split('\n')]

    print 'extracting these rules from', ftest
    out = []
    for descr in rule_descr:
        rule = [clause.split(':') for clause in descr.strip('{}').split(',')]
        bv = np.cast[str](np.cast[int](np.array([(d[name] == value) for (name, value) in rule]).all(axis=0)))
        out.append('%s %s' % (descr, ' '.join(bv)))

    print 'writing', fout
    f = open(fout, 'w')
    f.write('\n'.join(out))
    f.close()

    print 'writing', flabel
    recs = [(y == 0), (y == 1)]
    f = open(flabel, 'w')
    f.write('\n'.join(['{%s:%s} %s' % (label_name, l, ' '.join(np.cast[str](np.cast[int](r))))
                       for (l, r) in zip(labels, recs)]) + '\n')
    f.close()
