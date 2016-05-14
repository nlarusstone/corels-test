import os

import tabular as tb
import pylab


def viz_log(metadata, din, dout, delimiter=','):
    pass

def make_figure(metadata, din, dout, max_accuracy, max_length, delimiter='\t',
                alpha=0.05):
    fin = os.path.join(din, '%s.txt' % metadata)
    x = tb.tabarray(SVfile=fin, delimiter=delimiter)
    pylab.ion()
    for i in range(1, max_length + 1):
        print i
        pylab.figure(1, figsize=(14, 8))
        pylab.clf()
        y = x[x['length'] == i]
        pylab.subplot(2, 3, 1)
        pylab.hist(y['accuracy'])
        pylab.xlabel('accuracy')
        a = list(pylab.axis())
        a[0] = 0.5
        a[1] = 1.
        max_accuracy = y['accuracy'].max()
        pylab.plot([max_accuracy, max_accuracy], [0, a[3]], 'r-')
        pylab.axis(a)
        pylab.subplot(2, 3, 2)
        pylab.hist(y['upper_bound'])
        pylab.xlabel('upper_bound')
        a = list(pylab.axis())
        a[0] = max_accuracy
        a[1] = 1.
        pylab.axis(a)
        pylab.subplot(2, 3, 3)
        pylab.hist(y['curiosity'])
        pylab.xlabel('curiosity')
        a = list(pylab.axis())
        a[0] = 0
        a[1] = 1.
        pylab.axis(a)
        pylab.subplot(2, 3, 4)
        pylab.plot(y['accuracy'], y['upper_bound'], '.', alpha=alpha)
        pylab.xlabel('accuracy')
        pylab.ylabel('upper_bound')
        pylab.subplot(2, 3, 5)
        pylab.plot(y['accuracy'], y['curiosity'], '.', alpha=alpha)
        pylab.xlabel('accuracy')
        pylab.ylabel('curiosity')
        pylab.subplot(2, 3, 6)
        pylab.plot(y['upper_bound'], y['curiosity'], '.', alpha=alpha)
        pylab.xlabel('upper_bound')
        pylab.ylabel('curiosity')        

        fout = os.path.join(dout, '%s-length=%d.png' % (metadata, i))
        pylab.savefig(fout)

din = os.path.join('..', 'cache')
dout = os.path.join('..', 'figs')
if not os.path.exists(dout):
    os.mkdir(dout)

"""
make_figure(metadata='serial-max_accuracy=0.91-max_length=2', din=din, dout=dout,
            max_accuracy=0.91, max_length=2)

make_figure(metadata='serial_lazy-max_accuracy=0.99-max_length=4', din=din,
            dout=dout, max_accuracy=0.99, max_length=4)

make_figure(metadata='serial_lazy-max_accuracy=0.999-max_length=5', din=din,
            dout=dout, max_accuracy=0.999, max_length=5)

make_figure(metadata='tdata_R-serial_gc-max_accuracy=0.999-max_length=6',
            din=din, dout=dout, max_accuracy=0.999, max_length=6)

make_figure(metadata='tdata_R-serial_gc-max_accuracy=1.000-max_length=8',
            din=din, dout=dout, max_accuracy=1.000, max_length=8)

make_figure(metadata='adult_R-serial_gc-max_accuracy=0.829-max_length=3',
            din=din, dout=dout, max_accuracy=0.829, max_length=3)

"""