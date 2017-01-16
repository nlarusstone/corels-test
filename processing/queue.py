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

q = tb.tabarray(SVfile='../queue/queue-8.txt', delimiter=' ')

d = dict(zip(rules, z.T))

uncap_minority = np.zeros(len(q))
i = 0
for (lower_bound, objective, length, frac_captured, rl) in q:
    rule_list = [r.split('~')[0] for r in rl.split(';')[:-1]]
    uncap = (np.array([d[r] for r in rule_list]).sum(axis=0) == 0)
    uncap_minority[i] = (uncap & m).sum()
    i += 1

new_lower_bound = q['lower_bound'] + uncap_minority / n

print 'old lower bound mean (min, max): %1.5f (%1.5f, %1.5f)' % (q['lower_bound'].mean(), q['lower_bound'].min(), q['lower_bound'].max())

print 'new lower bound mean (min, max): %1.5f (%1.5f, %1.5f)' % (new_lower_bound.mean(), new_lower_bound.min(), new_lower_bound.max())

"""
mean (min, max) old lower bound : 0.05598 (0.05592, 0.05602)
mean (min, max) new lower bound : 0.16066 (0.13333, 0.16562)
"""
