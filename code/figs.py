import os

import tabular as tb
import pylab


def viz_log(metadata=None, din=None, dout=None, delimiter=',', lw=3, fs=14):
    metadata = 'adult_R-serial_priority-c=0-min_objective=495.000-method=breadth_first-max_cache_size=3000000-sample=0.10'
    din = '../logs'
    dout = '../figs'
    fin = os.path.join(din, '%s.txt' % metadata)
    x = tb.tabarray(SVfile=fin)
    t = x['seconds']
    names = ['priority_queue_length', 'cache_size', 'inferior', 'dead_prefix', 'commutes', 'captured_zero']
    pylab.ion()
    pylab.figure(1, figsize=(13, 8))
    pylab.clf()
    for (i, n) in enumerate(names):
        if (x[n] == 0).all():
            continue
        #pylab.subplot(len(names), 1, i + 1)
        pylab.plot(t, x[n], '-o', linewidth=lw)
    pylab.xlabel('time (sec)', fontsize=fs)
    pylab.ylabel('count', fontsize=fs)
    pylab.xticks(fontsize=fs)
    pylab.yticks(fontsize=fs)
    display_names = [n.replace('_', ' ') for n in names]
    pylab.legend(display_names, loc='upper left')
    pylab.title(metadata.replace('_', ' ').replace('-', ', ') + '\n', fontsize=fs)
    fout = os.path.join(dout, '%s-log.pdf' % metadata)
    pylab.savefig(fout)

    pylab.figure(2, figsize=(16, 10))
    pylab.clf()
    k = int(x.dtype.names[-1].split('_')[-1]) + 1
    y = x[-1]
    for (i, n) in enumerate(names[1:]):
        data = [y['%s_%d' % (n, j)] for j in range(k)]
        pylab.plot(data, '-o', linewidth=lw)
    return

def make_figure(metadata, din, dout, max_accuracy, max_length, delimiter='\t',
                alpha=0.05, lw=3, fs=14):
    fin = os.path.join(din, '%s.txt' % metadata)
    x = tb.tabarray(SVfile=fin, delimiter=delimiter)
    pylab.ion()
    pylab.figure(1, figsize=(16, 10))
    pylab.clf()
    for i in range(1, max_length + 1):
        print i
        y = x[x['length'] == i]

        pylab.subplot(max_length, 3, (i - 1) * 3 + 1)
        pylab.hist(y['objective'])
        pylab.hist(y['lower_bound'])
        # pylab.legend(('objective', 'lower bound'), loc='upper left')
        a = list(pylab.axis())
        min_objective = y['objective'].min()
        pylab.plot([min_objective] * 2, [0, a[3]], 'b:', linewidth=lw)
        max_lower_bound = y['lower_bound'].max()
        pylab.plot([max_lower_bound] * 2, [0, a[3]], 'g:', linewidth=lw)
        pylab.ylabel('%d' % len(y))
        pylab.yticks([pylab.yticks()[0][-2]])
        if (i == 1):
            pylab.title('lower bound & objective', fontsize=fs)
            a1 = pylab.axis()
        else:
            a = list(pylab.axis())
            a[0] = a1[0]
            a[1] = a1[1]
            pylab.axis(a)
        if (i < max_length):
            pylab.xticks([], [])

        pylab.subplot(max_length, 3, (i - 1) * 3 + 2)
        pylab.hist(y['accuracy'])
        pylab.hist(y['upper_bound'])
        # pylab.legend(('accuracy', 'upper bound'), loc='upper right')
        a = list(pylab.axis())
        a[0] = 0.5
        a[1] = 1.
        max_accuracy = y['accuracy'].max()
        pylab.plot([max_accuracy] * 2, [0, a[3]], 'b:', linewidth=lw)
        min_upper_bound = y['upper_bound'].min()
        pylab.plot([min_upper_bound] * 2, [0, a[3]], 'g:', linewidth=lw)
        pylab.yticks([pylab.yticks()[0][-2]])
        if (i == 1):
            pylab.title('accuracy & upper bound', fontsize=fs)
            a2 = pylab.axis()
        else:
            a = list(pylab.axis())
            a[0] = a2[0]
            a[1] = a2[1]
            pylab.axis(a)
        if (i < max_length):
            pylab.xticks([], [])

        pylab.subplot(max_length, 3, (i - 1) * 3 + 3)
        pylab.hist(y['curiosity'])
        pylab.yticks([pylab.yticks()[0][-2]])
        if (i == 1):
            pylab.title('curiosity', fontsize=fs)
            a3 = pylab.axis()
        else:
            a = list(pylab.axis())
            a[0] = a3[0]
            a[1] = a3[1]
            pylab.axis(a)
        if (i < max_length):
            pylab.xticks([], [])

    fout = os.path.join(dout, '%s-max_length=%d.pdf' % (metadata, max_length))
    pylab.suptitle(metadata.replace('-', ', '), fontsize=fs)
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