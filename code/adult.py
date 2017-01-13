"""
| Split into train-test using MLC++ GenCVFiles (2/3, 1/3 random).
| 48842 instances, mix of continuous and discrete    (train=32561, test=16281)
| 45222 if instances with unknown values are removed (train=30162, test=15060)
| Duplicate or conflicting instances : 6
| Class probabilities for adult.all file
| Probability for the label '>50K'  : 23.93% / 24.78% (without unknowns)
| Probability for the label '<=50K' : 76.07% / 75.22% (without unknowns)

age: continuous.
workclass: Private, Self-emp-not-inc, Self-emp-inc, Federal-gov, Local-gov, State-gov, Without-pay, Never-worked.
fnlwgt: continuous.
education: Bachelors, Some-college, 11th, HS-grad, Prof-school, Assoc-acdm, Assoc-voc, 9th, 7th-8th, 12th, Masters, 1st-4th, 10th, Doctorate, 5th-6th, Preschool.
education-num: continuous.
marital-status: Married-civ-spouse, Divorced, Never-married, Separated, Widowed, Married-spouse-absent, Married-AF-spouse.
occupation: Tech-support, Craft-repair, Other-service, Sales, Exec-managerial, Prof-specialty, Handlers-cleaners, Machine-op-inspct, Adm-clerical, Farming-fishing, Transport-moving, Priv-house-serv, Protective-serv, Armed-Forces.
relationship: Wife, Own-child, Husband, Not-in-family, Other-relative, Unmarried.
race: White, Asian-Pac-Islander, Amer-Indian-Eskimo, Other, Black.
sex: Female, Male.
capital-gain: continuous.
capital-loss: continuous.
hours-per-week: continuous.
native-country: United-States, Cambodia, England, Puerto-Rico, Canada, Germany, Outlying-US(Guam-USVI-etc), India, Japan, Greece, South, China, Cuba, Iran, Honduras, Philippines, Italy, Poland, Jamaica, Vietnam, Mexico, Portugal, Ireland, France, Dominican-Republic, Laos, Ecuador, Taiwan, Haiti, Columbia, Hungary, Guatemala, Nicaragua, Scotland, Thailand, Yugoslavia, El-Salvador, Trinadad&Tobago, Peru, Hong, Holand-Netherlands.
income: >50K, <=50K.
"""

import numpy as np
import tabular as tb

import ben
import minority


def age_func(a):
    if (a < 30):
        return '<30'
    elif (a < 50):
        return '30-50'
    elif (a < 65):
        return '51-65'
    else:
        return '>65'

def capital_gain_func(c):
    if (c >= 7298):
        return '>=7298'
    else:
        return '<7298'

def hours_func(h):
    if (c < 40):
        return '<40'
    elif (c == 40):
        return '40'
    else:
        return '>40'

names = ['age', 'workclass', 'fnlwgt', 'education', 'education-num',
         'marital-status', 'occupation', 'relationship', 'race', 'sex',
         'capital-gain', 'capital-loss', 'hours-per-week', 'native-country',
         'income']

x = open('../data/adult/adult.data', 'rU').read().strip().split('\n')
x = [','.join(line.split(', ')) for line in x if '?' not in line]

assert (len(x) == 30162)

f = open('../data/adult/adult-filtered.csv', 'w')
f.write(','.join(names) + '\n')
f.write('\n'.join(x))
f.close()

x = tb.tabarray(SVfile='../data/adult/adult-filtered.csv')

age = np.array([age_func(a) for a in x['age']])

capital_gain  = np.array([capital_gain_func(c) for c in x['capital-gain']])

capital_loss = np.array(['>0' if (c > 0) else '=0' for c in x['capital-loss']])

hours_per_week = np.array([hours_func(h) for h in x['hours-per-week']])

income = np.cast[int](x['income'] == '>50K')

columns = [age, x['workclass'], x['education'], x['marital-status'], x['occupation'],
           x['relationship'], x['race'], x['sex'], capital_gain, capital_loss,
           hours_per_week, x['native-country'], income]

names = ['age', 'workclass', 'education', 'marital-status', 'occupation',
         'relationship', 'race', 'sex', 'capital-gain', 'capital-loss',
         'hours-per-week', 'native-country', 'income']

y = tb.tabarray(columns=columns, names=names)
y.saveSV('../data/adult/adult.csv')

#ben.driver(din='../data/adult', dout='../data/adult', froot='adult', train_suffix='.csv',
#           delimiter=',', is_binary=False, maxlhs=2, minsupport=2.5, out_suffix='')

#minority.compute_minority(froot='adult', dir='../data/adult')
