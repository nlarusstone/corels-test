import numpy as np


folds = open('frisk-sparsity-sbrl.txt', 'rU').read().strip().split('Initialize')[1:]

out = []

for (i, f) in enumerate(folds):
    f = f.strip().split('\n')
    model = [line for line in f if line.startswith('n0')]
    a = np.array([float(m.strip().split()[-1]) for m in model])
    cap = np.array([float(m.strip().split()[2].split('=')[1].strip(',')) for m in model])
    train_acc = (a * cap).sum() / cap.sum()
    test_acc = float([line for line in f if line.startswith('test acc')][0].strip().split()[-1])
    out += ['%d,%s,0,0,0,%1.10f,%d,%1.10f' % (i, 'SBRL', test_acc, len(model), train_acc)]

fh = open('frisk_sparsity-sbrl.csv', 'w')
fh.write('\n'.join(out) + '\n')
fh.close()
