"""
Have 9 features: c1, c2, ..., c9
Each feature can have 1 of 3 values: b, o, x

For j, k in (b, o, x) s.t. j != k,  ci=j commutes with ci=k, for all ci

If prefix contains ci=j and ci=k, then should never check ci=l

"""

import numpy as np

from serial_priority import load_data


(nrules, ndata, ones, rules, rule_set, rule_names) = load_data('tdata_R')

print 'ndata:', ndata
print 'nrules:', nrules

clauses = np.array([r.strip('{}').split(',') for r in rule_names])
num_clauses = np.array([len(c) for c in clauses])

for n in [1, 2, 3]:
    print '(nclauses = %d):' % n, (num_clauses == n).sum()

