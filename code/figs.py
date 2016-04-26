import os

import tabular as tb
import pylab


def make_figure(froot, din, dout, max_accuracy, max_length, delimiter='\t'):
    fin = os.path.join(din, '%s.txt' % froot)
    x = tb.tabarray(SVfile=fin, delimiter=delimiter)
    pylab.ion()
    pylab.figure(1, figsize=(10, 8))
    pylab.clf()
    nrows = max_length
    ncols = 2
    for i in range(1, max_length + 1):
        y = x[x['length'] == i]
        pylab.subplot(nrows, ncols, (i - 1) * ncols + 1)
        pylab.hist(y['accuracy'])
        pylab.xlabel('accuracy')
        a = list(pylab.axis())
        a[0] = 0.5
        a[1] = 1.
        pylab.axis(a)
        pylab.subplot(nrows, ncols, (i - 1) * ncols + 2)
        pylab.hist(y['upper_bound'])
        pylab.xlabel('upper_bound')
        a = list(pylab.axis())
        a[0] = max_accuracy
        a[1] = 1.
        pylab.axis(a)
    fout = os.path.join(dout, '%s.pdf' % froot)
    pylab.savefig(fout)

din = os.path.join('..', 'cache')
dout = os.path.join('..', 'figs')
if not os.path.exists(dout):
    os.mkdir(dout)

"""
make_figure(froot='serial-max_accuracy=0.91-max_length=2', din=din, dout=dout,
            max_accuracy=0.91, max_length=2)

make_figure(froot='serial_lazy-max_accuracy=0.99-max_length=4', din=din,
            dout=dout, max_accuracy=0.99, max_length=4)

make_figure(froot='serial_lazy-max_accuracy=0.999-max_length=5', din=din,
            dout=dout, max_accuracy=0.999, max_length=5)
"""

make_figure(froot='tdata_R-serial_gc-max_accuracy=0.999-max_length=5',
            din=din, dout=dout, max_accuracy=0.999, max_length=5)