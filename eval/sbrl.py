"""
E.g., first run

    ./sbrl.sh adult > adult_sparsity-sbrl.txt

"""

import numpy as np

dataset = 'frisk'
dataset = 'compas'
#dataset = 'adult'
#dataset = '1adult'
descr = 'sparsity-sbrl'

dataset = 'weapon'
#dataset = 'compas'
descr = 'sparsity-sbrl-eta=3-lambda=9'
#descr = 'sparsity-sbrl-eta=15-lambda=5'
#descr = 'sparsity-sbrl-eta=500-lambda=5'

folds = open('%s_%s.txt' % (dataset, descr), 'rU').read().strip().split('Initialize')[1:]
out = []

for (i, f) in enumerate(folds):
    f = f.strip().split('\n')
    model = [line for line in f if line.startswith('n0') and 'nan' not in line]
    a = np.array([float(m.strip().split()[-1]) for m in model])
    cap = np.array([float(m.strip().split()[2].split('=')[1].strip(',')) for m in model])
    train_acc = (a * cap).sum() / cap.sum()
    test_acc = float([line for line in f if line.startswith('test acc')][0].strip().split()[-1])
    out += ['%d,%s,0,0,0,%1.10f,%d,%1.10f' % (i, 'SBRL', test_acc, len(model), train_acc)]

fh = open('%s_%s.csv' % (dataset, descr), 'w')
fh.write('\n'.join(out) + '\n')
fh.close()
