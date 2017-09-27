"""
See also `weapon_ablation.py`

"""
import os

import gmpy2
import numpy as np
import pylab
import tabular as tb

import utils


froot = 'weapon'
data_dir = '../data/CrossValidation/'
log_dir = '../logs/'
lw = 2  # linewidth
ms = 9  # markersize
fs = 18 # fontsize

num_folds = 10
make_figure = False
figure_fold = -1
make_small = False

make_figure = True
#num_folds = 1
figure_fold = 0

# log files generated on beepboop
#log_dir = '/Users/elaine/Dropbox/bbcache/logs/keep/'
#log_dir = '/Users/elaine/Dropbox/bbcache/logs/corels/'
#log_dir = '/Users/elaine/Dropbox/bbcache/logs/arxiv/'
log_dir = '/Users/nlarusstone/Documents/Research/bbcache/jmlr/'

if make_figure:
    log_root_list = ['for-%s-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=1000000000-c=0.0400000-v=10-f=1000.txt',
    'for-%s-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=1000000000-c=0.0100000-v=10-f=1000.txt',
    'for-%s-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=1000000000-c=0.0025000-v=10-f=1000.txt']
else:
    log_root_list = ['for-%s-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=1000000000-c=0.0400000-v=10-f=1000.txt',
    'for-%s-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=1000000000-c=0.0100000-v=10-f=1000.txt',
    'for-%s-curious_lb-with_prefix_perm_map-minor-removed=none-max_num_nodes=1000000000-c=0.0025000-v=10-f=1000.txt']

labels = ['$\lambda$ = 0.04', '$\lambda$ = 0.01', '$\lambda$ = 0.0025']
ftag = "weapon_reg"

if (make_figure):
    pylab.ion()
    pylab.figure(6, figsize=(16, 6.55))

ntot = len(log_root_list)

num_rules = np.zeros(num_folds, int)

t_tot = np.zeros((ntot, num_folds))
t_opt = np.zeros((ntot, num_folds))
max_prefix_length = np.zeros((ntot, num_folds), int)
num_insertions = np.zeros((ntot, num_folds), int)
max_queue = np.zeros((ntot, num_folds), int)
min_obj = np.zeros((ntot, num_folds))
lower_bound_num = np.zeros((ntot, num_folds), int)
optimal_prefix_length = np.zeros((ntot, num_folds), int)
ablation_names = ['0.04', '0.01', '0.0025']

for (ncomp, log_root) in enumerate(log_root_list):
    for fold in range(num_folds):
        if (fold == figure_fold):
            make_figure = True
        else:
            make_figure = False
        tname = '%s_%d_train.out' % (froot, fold)
        log_fname = log_root % tname
        print log_fname
        fname = os.path.join(data_dir, tname)

        c = float(log_fname.split('c=')[1].split('-')[0])
        log_fname = os.path.join(log_dir, log_fname)
        try:
            print 'reading', log_fname
            x = tb.tabarray(SVfile=log_fname)
            oname = log_fname.replace('.txt', '-opt.txt').replace('0001', '0002')
            print oname
            if not os.path.exists(oname):
                oname = oname.replace('f=1000', 'f=10')
            olength = len(open(oname, 'rU').read().strip().split(';')[:-1])
            optimal_prefix_length[ncomp, fold] = olength
        except:
            print 'skipping', log_fname
            continue

        #x = x[:-1]  # ignore last log record because it measures the time to delete the queue

        x['total_time'] = x['total_time'] - x['total_time'][0] + 10**-4

        if ('no_minor' in log_fname):
            x = x[x['tree_min_objective'] > 0]

        min_obj[ncomp, fold] = x['tree_min_objective'].min()
        default_objective = x['tree_min_objective'][1]
        imin = np.nonzero(x['tree_min_objective'] == x['tree_min_objective'][-1])[0][0]
        tmin = x['total_time'][imin]
        tmax = x['total_time'][-1]

        prefix_sums = np.array([utils.parse_prefix_sums(p) for p in x['prefix_lengths']])
        n_ins = x['tree_insertion_num'][-1]
        lower_bound_num[ncomp, fold] = x['lower_bound_num'][-1]

        print "num records:", len(x)
        t_opt[ncomp, fold] = tmin
        print "time to achieve optimum:", tmin
        t_tot[ncomp, fold] = tmax
        print "time to verify optimum:", tmax
        num_insertions[ncomp, fold] = n_ins
        print "num insertions (millions): ", n_ins / 10**6.

        prefix_lengths = list(x['prefix_lengths'])
        max_length = max(set([int(lc.split(':')[0]) for lc in ''.join(prefix_lengths).split(';') if lc]))
        max_prefix_length[ncomp, fold] = max_length
        print "max prefix length:", max_length
        split_hist = [[lc.split(':') for lc in lh.strip(';').split(';')] for lh in prefix_lengths]
        kvp = [[(lc[0], int(lc[1])) for lc in lh if (len(lc) == 2)] for lh in split_hist]
        z = tb.tabarray(kvpairs=kvp)
        assert ([int(name) for name in z.dtype.names] == range(max_length + 1))
        #zc = z.extract()[:, ::-1].cumsum(axis=1)[:, ::-1]
        zc = z.extract()
        qc = zc.sum(axis=1)
        if (ncomp > -1):
            queue_comp = zc.sum(axis=1)
            ii = queue_comp.nonzero()[0]
            queue_comp = queue_comp[ii]
            t_comp = x['total_time'][ii]
        
        max_q = zc.sum(axis=1).max()
        max_queue[ncomp, fold] = max_q
        print "max queue size (millions): ", max_q / 10**6.

        if (make_figure):
            color_vec = ['r', 'r', 'orange', 'y', 'g', 'c', 'b', 'purple', 'm', 'violet', 'pink', 'gray', 'k']#[:(max_length + 1)][::-1]
            color_vec = ['k', 'violet', 'm', 'purple', 'darkslateblue', 'b', 'cornflowerblue', 'c', 'mediumseagreen', 'green', 'yellowgreen', 'y', 'orange', 'tomato', 'r', 'brown']
            #color_vec = ['purple', 'b', 'c', 'm', 'gray', 'k'][::-1]

            if (ncomp == 0):
                pylab.clf()

            pylab.subplot(1, 3, ncomp+1)

            pylab.fill_between(t_comp, 10**-0.1 * np.ones(len(t_comp)), queue_comp, color='gray', alpha=0.3)

            for length in range(1, max_length + 1):
                jj = zc[:, length].nonzero()[0]
                tt = x['total_time'][jj]
                yy = zc[jj, length]
                if (ncomp + 1 < ntot):
                    yy = np.array([1] + list(yy) + [1])
                    tt = np.array([tt[0]] + list(tt) + [tt[-1]])
                else:
                    yy = np.array([1] + list(yy))
                    tt = np.array([tt[0]] + list(tt))
                pylab.loglog(tt, yy, color=color_vec[length % len(color_vec)], linewidth=lw*2)
                if make_small:
                    if (length == 1):
                        txt = pylab.text(tt[0] * 0.47, 1.5, '%d ' % length, fontsize=fs+4)
                    else:
                        txt = pylab.text(tt[0] * 0.4, 1.5, '%d ' % length, fontsize=fs+4)
            if (ncomp > -1):
                pylab.xlabel('Time (s)\n', fontsize=fs+2)
            if (ncomp % 3 == 0):
                pylab.ylabel('Count', fontsize=fs+2)
            (ymin, ymax) = (10**-0.01, 10**6.8)
            t_corels = t_comp[-1]
            tmax = np.round(tt[-1])
            pylab.plot([tt[-1], tt[-1]], [ymin, ymax], 'k--', linewidth=lw)
            if (tmax == 0):
                descr = '%1.2f s' % tt[-1]
            else:
                descr = '%d s' % tmax
            descr = ' ' * 2 * (5 - len(descr)) + descr
            print "TTTT: ", tt[-1]
            pylab.text(tt[-1] / 170, qc.max() * 1.1, descr, fontsize=fs+2)
            pylab.text(10**-3.7, 10**6.1, labels[ncomp], fontsize=fs+2)
            pylab.xticks(fontsize=fs-2)
            pylab.yticks(fontsize=fs-2)
            pylab.xticks(10.**np.array([-2, 0, 2]), fontsize=fs)
            xmax = 10**3
            if ncomp == 2:
                print "NCOMP 2"
                xmax = 10**3.5
                pylab.xlim([10**-2, 10**3.5])
            pylab.yticks(10.**np.array([0, 2, 4, 6]), fontsize=fs)
            ax = [10**-4, xmax, ymin, ymax]
            pylab.axis(ax)
            pylab.draw()
            if (ncomp + 1 == ntot):
                if not (make_small):
                    pylab.legend(['%d' % ii for ii in range(1, max_length + 1)], loc=(-1.83, 0.52), handletextpad=0, borderaxespad=0.1, ncol=2, frameon=False, columnspacing=0.5)
                    pylab.suptitle('Execution traces of queue contents (NYCLU stop-and-frisk dataset)', fontsize=fs+4)
                pylab.savefig('../figs/%s-queue.pdf' % ftag)

max_prefix_length += 1
print 'num rules:', num_rules
print 't_tot:', t_tot
print 't_opt:', t_opt
print 'K_max:', max_prefix_length
print 'i_total:', num_insertions
print 'max_Q:', max_queue
print 'min_obj:', min_obj

#tt_m = np.cast[int](np.round(t_tot.mean(axis=1)))
#tt_s = np.cast[int](np.round(t_tot.std(axis=1)))
tt_m = t_tot.mean(axis=1)
tt_s = t_tot.std(axis=1)
to_m = t_opt.mean(axis=1)
to_s = t_opt.std(axis=1)
km_m = np.cast[int](max_prefix_length.mean(axis=1))
km_s = max_prefix_length.std(axis=1)
km_min = max_prefix_length.min(axis=1)
km_max = max_prefix_length.max(axis=1)
k_min = optimal_prefix_length.min(axis=1)
k_max = optimal_prefix_length.max(axis=1)
it_m = num_insertions.mean(axis=1) / 10**3
it_s = num_insertions.std(axis=1) / 10**3
mq_m = max_queue.mean(axis=1) / 10**3
mq_s = max_queue.std(axis=1) / 10**3

slow_m = (t_tot / t_tot[0]).mean(axis=1) # slowdown
lb_m = lower_bound_num.mean(axis=1) / 10**6
lb_s = lower_bound_num.std(axis=1) / 10**6

print '& Total time & Time to & Max evaluated & Optimal \\\\'
print '$\\lambda$ & (s) & optimum (s) & prefix length & prefix length \\\\'
for rec in zip(ablation_names, tt_m, tt_s, to_m, to_s, km_min, km_max, k_min, k_max):
    print '%s & %1.2f (%1.2f) & %1.3f (%1.5f) & %d-%d & %d-%d \\\\' % rec

print '& Lower bound & Total queue &  Max queue \\\\'
print '$\\lambda$ & evaluations ($\\times 10^6$) & insertions ($\\times 10^3$) & size ($\\times 10^3$) \\\\'
for rec in zip(ablation_names, lb_m, lb_s, it_m, it_s, mq_m, mq_s):
    print '%s & %1.3f (%1.3f) & %1.1f (%1.1f) & %1.2f (%1.2f) \\\\' % rec


#print '& Lower bound & Total queue &  Max queue \\\\'
#print 'Algorithm variant & computations ($\\times 10^6$) & insertions ($\\times 10^5$) & size #($\\times 10^5$) \\\\'
#for rec in zip(labels, lb_m, lb_s, it_m, it_s, mq_m, mq_s):
#    print '%s & %1.2f (%1.1f) & %1.2f (%1.1f) & %1.2f (%1.1f) \\\\' % rec
