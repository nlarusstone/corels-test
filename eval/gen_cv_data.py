import pandas as pd
import numpy as np
import sklearn
from sklearn.model_selection import ShuffleSplit
import os
import re

extensions = ['.label', '.out', '_binary.csv']
f_names = set()
for f_name in os.listdir('../data'):
    for extension in extensions:
        if extension in f_name:
            f_names.add(re.sub(extension, '', f_name))

for fname in f_names:
    nrules = 0
    with open('../data/{0}.out'.format(fname)) as f:
        line = f.readline()
        nrules = len(line.split()) - 1
    out = pd.read_csv('../data/{0}.out'.format(fname), sep=' ', names=['Rule'] + range(nrules))
    label = pd.read_csv('../data/{0}.label'.format(fname), sep=' ', names=['Rule'] + range(nrules))
    cv = ShuffleSplit(n_splits=10, random_state=137)
    i = 0
    for train, test in cv.split(out.T):
        train = train[train > 0]
        test = test[test > 0]
        for seg, split in [('train', train), ('test', test)]:
            out_train = '../data/{0}_{1}_{2}.out'.format(fname, i, seg)
            label_train = '../data/{0}_{1}_{2}.label'.format(fname, i, seg)
            with open(out_train, 'w') as out_f:
                out_concat = pd.concat([out.iloc[:, 0], out.iloc[:, split]], axis=1)
                out_concat.to_csv(out_f, sep=' ', index=False, header=False)
            with open(label_train, 'w') as label_f:
                label_concat = pd.concat([label.iloc[:, 0], label.iloc[:, split]], axis=1)
                label_concat.to_csv(label_f, sep=' ', index=False, header=False)
        i += 1
