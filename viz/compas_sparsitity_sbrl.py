import numpy as np
import tabular as tb

import pylab
pylab.ion()
pylab.clf()

x = tb.tabarray(SVfile='../eval/compas_sparsity-sbrl-sweeps.csv')

m = x.aggregate(On=['eta', 'lambda'], AggFuncDict={'num_rules': np.mean, 'test_acc': np.mean})

s = x.aggregate(On=['eta', 'lambda'], AggFuncDict={'num_rules': np.std, 'test_acc': np.std})

colors = ['b', 'g', 'c', 'm', 'k']

legend = []
for mm in m:
    legend += ['(%d, %d)' % (mm['eta'], mm['lambda'])]
    pylab.plot(mm['num_rules'], mm['test_acc'], 'o', color=colors[mm['eta'] - 1])

pylab.axis([7.5, 12, 0.65, 0.725])
pylab.legend(legend, numpoints=1, labelspacing=0.1, ncol=5, columnspacing=0., fontsize=13.6, loc='upper center')

i = 0
for i in range(len(m)):
    pylab.errorbar(m[i]['num_rules'], m[i]['test_acc'], xerr=s[i]['num_rules'], yerr=s[i]['test_acc'], marker='o',  color=colors[m[i]['eta'] - 1], capsize=0)

pylab.title('(eta, lambda)')
pylab.xlabel('Model size')
pylab.ylabel('Test accuracy')
pylab.xticks(range(8, 13))
pylab.savefig('../figs/compas_sparsity_sbrl.pdf')