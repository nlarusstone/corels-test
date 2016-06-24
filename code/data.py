import os

import numpy as np
import tabular as tb

def csv_to_R(din='../data/csv'):
    flist = [f for f in os.listdir(din) if f.endswith('.csv')]
    for f in flist:
        fname = os.path.join(din, f)
        froot = f.split('_binary.csv')[0]
        print fname
        try:
            x = tb.tabarray(SVfile=fname)
        except:
            s = '\n'.join([line for line in
                           open(fname, 'rU').read().strip().split('\n')
                           if line.strip()])
            fh = open(fname, 'w')
            fh.write(s)
            fh.close()
            x = tb.tabarray(SVfile=fname)

        l1 = '{label=1} ' + ' '.join(list(np.cast[str](x['y'])))
        l0 = '{label=0} ' + ' '.join(list(np.cast[str](1 - x['y'])))
        flabel = os.path.join('../data/', froot + '_R.label')
        fh = open(flabel, 'w')
        fh.write('\n'.join([l0, l1]))
        fh.close()
    
        lines = [('{%s} ' % n) + ' '.join(list(np.cast[str](x[n])))
                 for n in x.dtype.names[:-1]]
        fout = os.path.join('../data/', froot + '_R.out')
        fh = open(fout, 'w')
        fh.write('\n'.join(lines))
        fh.close()
    return

