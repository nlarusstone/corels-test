"""
Quick stats on ProPublica variants and other analysis


our age categories, no race
test mean, std 0.676 0.020

coarse age categories + race:  mine 197-198 rules (mean = 197.2)
test mean, std 0.659 0.015

COMPAS score accuracy
test mean, std 0.654 0.015

"""
import numpy as np
import tabular as tb
import pylab


print 'our age categories, no race'

test = np.array([0.7073509015256588, 0.6823855755894591, 0.6893203883495146, 0.680998613037448, 0.6490984743411928, 0.6601941747572816, 0.6435506241331485, 0.6893203883495146, 0.6588072122052705, 0.694868238557559])

#Test accuracies mean, std 0.675589459085 0.0201987656911
print 'test mean, std', test.mean(), test.std()


print 'coarse age categories + race:  mine 197-198 rules (mean = 197.2)'
"""
$ tail ../logs/for-propublica_*_train.out-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=100000000-*opt*
{priors:>3}~1;{sex:Male,age:<25}~1;default~0
{sex:Male,age:<25}~1;{priors:>3}~1;default~0
{age:<25,priors:2-3}~1;{age:<25,juvenile-crimes:>0}~1;{priors:>3}~1;default~0
{priors:>3}~1;{sex:Male,age:<25}~1;default~0
{priors:>3}~1;{age:<25,priors:2-3}~1;{age:<25,juvenile-crimes:>0}~1;default~0
{priors:>3}~1;{sex:Male,age:<25}~1;default~0
{sex:Male,age:<25}~1;{priors:>3}~1;default~0
{juvenile-crimes:=0,priors:=0}~0;{sex:Male,age:<25}~1;{priors:>3}~1;default~0
{age:<25,priors:2-3}~1;{priors:>3}~1;{age:<25,juvenile-crimes:>0}~1;default~0
{priors:>3}~1;{sex:Male,age:<25}~1;default~0

"""
c_train = np.array([0.6598859608568346, 0.6628139929110803, 0.6669748805671136, 0.6623516720604099, 0.670519340422253, 0.6631222068115272, 0.665433811064879, 0.6666666666666666, 0.6692864848204654, 0.6621975651101865])

#Train accuracies mean, std 0.664925258129 0.00323994974049
print 'train mean, std', c_train.mean(), c_train.std()

c_test = np.array([0.6865464632454924, 0.6601941747572816, 0.665742024965326, 0.6643550624133149, 0.6338418862690708, 0.6574202496532594, 0.636615811373093, 0.6740638002773925, 0.6449375866851595, 0.665742024965326])

# Test accuracies mean, std 0.65894590846 0.0156235036776
print 'test mean, std', c_test.mean(), c_test.std()

print 'COMPAS score accuracy'
s_test = np.array([0.66019417, 0.67822469, 0.66574202, 0.66574202, 0.65742025, 0.65603329, 0.63522885, 0.63245492, 0.65325936, 0.63245492])

# Test accuracies mean, std 0.653675450763 0.014822341024
print 'test mean, std', s_test.mean(), s_test.std()

color_vec = ['r', 'orange', 'y', 'g', 'c', 'b', 'purple', 'violet', 'm', 'gray']
ii = c_test.argsort()[::-1]

pylab.ion()
pylab.figure(1)
pylab.clf()
pylab.errorbar(0, test.mean(), test.std(), fmt=None, ecolor='k', elinewidth=2, capsize=8, capthick=2)
pylab.errorbar(1, c_test.mean(), s_test.std(), fmt=None, ecolor='k', elinewidth=2, capsize=8, capthick=2)
pylab.errorbar(2, s_test.mean(), s_test.std(), fmt=None, ecolor='k', elinewidth=2, capsize=8, capthick=2)

for (i, color) in zip(ii, color_vec):
    pylab.plot(0, test[i], 'D', color=color, markeredgewidth=0, markersize=4.5)
    pylab.plot(1, c_test[i], 'D', color=color, markeredgewidth=0, markersize=4.5)
    pylab.plot(2, s_test[i], 'D', color=color, markeredgewidth=0, markersize=4.5)

pylab.plot(0, test.mean(), 's', markerfacecolor='w', markeredgecolor='k', markeredgewidth=2, linewidth=2, markersize=7)
pylab.plot(1, c_test.mean(), 's', markerfacecolor='w', markeredgecolor='k', markeredgewidth=2, linewidth=2, markersize=7)
pylab.plot(2, s_test.mean(), 's', markerfacecolor='w', markeredgecolor='k', markeredgewidth=2, linewidth=2, markersize=7)
pylab.axis([-0.5, 2.5, 0.63, 0.71])
pylab.xticks([0, 1, 2], ['CORELS (1)', 'CORELS (2)', 'COMPAS'], fontsize=14)
pylab.yticks(np.arange(0.63, 0.72, 0.02), fontsize=14)
pylab.ylabel('Accuracy', fontsize=14)
