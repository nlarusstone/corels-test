import os

import numpy as np
import tabular as tb
import matplotlib.pyplot as plt


def viz_log(metadata=None, din=None, dout=None, delimiter=',', lw=3, fs=14):
    fin = os.path.join(din, '%s.txt' % metadata)
    x = tb.tabarray(SVfile=fin, delimiter=delimiter)
    t = x['seconds']
    names = ['cache_size', 'priority_queue_length', 'captured_small',
             'captured_all', 'captured_same', 'insufficient', 'commutes',
             'commutes_II', 'dominates', 'rejects', 'dead_prefix', 'inferior',
             'garbage_collect', 'prune_up']
    rename_dict = {'captured_small': 'insufficient\ncaptured', 'insufficient': 'insufficent\ncorrect'}
    display_names = [rename_dict[n] if n in rename_dict else n for n in names]
    display_names = [n.replace('_', ' ') for n in display_names]
    color_vec = ['blue', 'blue', 'green', 'grey', 'orange', 'magenta', 'cyan',
                 'yellow', 'pink', 'black', 'gray', 'brown', 'violet', 'purple']
    plt.ion()
    plt.figure(1, figsize=(15, 9))
    plt.clf()
    title = metadata.replace('-', ', ').split(' ')
    plt.title(' '.join(title[:4]) + '\n' + ' '.join(title[4:]), fontsize=fs)

    plt.subplot(4, 5, 1)
    plt.plot(t, x['min_objective'], '-', linewidth=lw)
    plt.title('objective', fontsize=fs)

    plt.subplot(4, 5, 2)
    plt.plot(t, x['accuracy'], '-', linewidth=lw)
    plt.title('accuracy', fontsize=fs)

    plt.subplot(4, 5, 3)
    plt.plot(t, [len([q for q in str(p).strip(';').split(';') if q]) for p in x['best_prefix']], '-', linewidth=lw)
    plt.title('prefix length', fontsize=fs)

    plot_num = 3
    for (n, c, dn) in zip(names, color_vec, display_names):
        plot_num += 1
        plt.subplot(4, 5, plot_num)
        plt.plot(t, x[n], '-', linewidth=lw, color=c)
        plt.title(dn, fontsize=fs)
        if (plot_num > 5):
            plt.xlabel('time (sec)', fontsize=fs)
    try:
        plt.tight_layout()
    except:
        pass
    fout = os.path.join(dout, '%s-log.png' % metadata)
    plt.savefig(fout)

    try:
        plt.figure(2, figsize=(8, 6))
        plt.clf()
        k = int(x.dtype.names[-1].split('_')[-1]) + 1
        y = x[-1]
        c = np.array([y[name] for name in x.dtype.names if name.startswith('cache_size')][1:])
        ind = (c > 0).nonzero()[0]
        try:
            for (i, n) in enumerate(names[1:]):
                data = np.array([y['%s_%d' % (n, j)] for j in range(k)])[ind]
                plt.bar(np.arange(len(data)) * len(names) + i, data, color=color_vec[i+1])
            plt.legend(display_names[1:], loc='upper left')
            plt.xticks(np.arange(len(data)) * len(names), np.arange(len(data)))
            plt.xlabel('prefix length', fontsize=fs)
            plt.ylabel('count', fontsize=fs)
            fout = os.path.join(dout, '%s-hist.pdf' % metadata)
            plt.savefig(fout)
        except:
            pass
    except:
        pass

    try:
        c = np.array([x[name] for name in x.dtype.names
                      if name.startswith('cache_size')][1:]).sum(axis=1)
        ind = (c > 0).nonzero()[0]
        z = np.array([x['%s_%d' % ('cache_size', j)] for j in range(k)])[ind]
        zmax = z.max()
        tmax = x['seconds'][-1]
        nrows = int(np.ceil(len(z) / 5.))
        plt.figure(3, figsize=(8, 6))
        plt.clf()
        plot_num = 0
        y = np.zeros(z.shape[1])
        for i in range(len(z)):
            plot_num += 1
            y += z[i, :]
            plt.plot(x['seconds'], y, linewidth=lw)
        plt.xlabel('time (sec)', fontsize=fs)
        plt.ylabel('cache entries', fontsize=fs)
        plt.title('cache entries by prefix length', fontsize=fs)
        try:
            plt.tight_layout()
        except:
            pass
        fout = os.path.join(dout, '%s-cache.png' % metadata)
        plt.savefig(fout)
    except:
        pass
    return

def make_figure(metadata, din, dout, delimiter='\t', alpha=0.05, lw=3, fs=14):
    fin = os.path.join(din, '%s.txt' % metadata)
    x = tb.tabarray(SVfile=fin, delimiter=delimiter)
    plt.ion()
    plt.figure(4, figsize=(16, 10))
    plt.clf()
    min_length = max(x[0]['length'], 1)
    max_length = x[-1]['length']
    for i in range(min_length, max_length + 1):
        y = x[x['length'] == i]
        if (len(y) < 2):
            continue
        plt.subplot(max_length, 3, (i - 1) * 3 + 1)
        plt.hist(y['objective'])
        plt.hist(y['lower_bound'])
        # plt.legend(('objective', 'lower bound'), loc='upper left')
        a = list(plt.axis())
        min_objective = y['objective'].min()
        plt.plot([min_objective] * 2, [0, a[3]], 'b:', linewidth=lw)
        max_lower_bound = y['lower_bound'].max()
        plt.plot([max_lower_bound] * 2, [0, a[3]], 'g:', linewidth=lw)
        plt.yticks([plt.yticks()[0][-2]])
        plt.ylabel('\nlen=%d' % i, rotation='horizontal')
        if (i == min_length):
            plt.title('lower bound & objective', fontsize=fs)
            a1 = list(plt.axis())
            a1[0] = max(0, a1[0])
            plt.axis(a1)
        else:
            a = list(plt.axis())
            a[0] = a1[0]
            a[1] = a1[1]
            plt.axis(a)
        plt.text(0.05 * (a[1] - a[0]) + a[0], 0.6 * a[3], 'n=%d' % len(y))
        if (i < max_length):
            plt.xticks([], [])

        plt.subplot(max_length, 3, (i - 1) * 3 + 2)
        plt.hist(y['accuracy'])
        plt.hist(y['upper_bound'])
        # plt.legend(('accuracy', 'upper bound'), loc='upper right')
        a = list(plt.axis())
        a[0] = 0.5
        a[1] = 1.
        max_accuracy = y['accuracy'].max()
        plt.plot([max_accuracy] * 2, [0, a[3]], 'b:', linewidth=lw)
        min_upper_bound = y['upper_bound'].min()
        plt.plot([min_upper_bound] * 2, [0, a[3]], 'g:', linewidth=lw)
        plt.yticks([plt.yticks()[0][-2]])
        if (i == min_length):
            plt.title('accuracy & upper bound', fontsize=fs)
            a2 = plt.axis()
        else:
            a = list(plt.axis())
            a[0] = a2[0]
            a[1] = a2[1]
            plt.axis(a)
        if (i < max_length):
            plt.xticks([], [])

        plt.subplot(max_length, 3, (i - 1) * 3 + 3)
        plt.hist(y['curiosity'])
        plt.yticks([plt.yticks()[0][-2]])
        if (i == min_length):
            plt.title('curiosity', fontsize=fs)
            a3 = plt.axis()
        else:
            a = list(plt.axis())
            a[0] = a3[0]
            a[1] = a3[1]
            plt.axis(a)
        if (i < max_length):
            plt.xticks([], [])

    fout = os.path.join(dout, '%s-leaves.png' % metadata)
    plt.suptitle(metadata.replace('-', ', '), fontsize=fs)
    plt.savefig(fout)

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