import os

import pylab

from branch_bound import initialize
from serial_priority import bbound
import utils


def tdata_x(min_objective=1., method='curiosity', max_cache_size=1500000):
    (metadata, metrics, cache, priority_queue, best, rule_list) = \
    bbound(din=os.path.join('..', 'data'), dout=os.path.join('..', 'cache'),
           dlog=os.path.join('..', 'logs'), dfigs=os.path.join('..', 'figs'),
           froot='tdata_R', warm_start=False, max_accuracy=0., best_prefix=(),
           min_objective=min_objective, c=0.001, min_captured_correct=0.001,
           max_prefix_length=10, max_cache_size=max_cache_size, delimiter='\t',
           method=method, seed=0, sample=1., quiet=True, clear=True,
           garbage_collect=True, do_pruning=False)
    return (metadata, metrics, cache, priority_queue, best, rule_list)

def tdata_1(min_objective=1., method='curiosity', max_cache_size=360000):
    (metadata, metrics, cache, priority_queue, best, rule_list) = \
    bbound(din=os.path.join('..', 'data'), dout=os.path.join('..', 'cache'),
           dlog=os.path.join('..', 'logs'), dfigs=os.path.join('..', 'figs'),
           froot='tdata_R', warm_start=False, max_accuracy=0., best_prefix=(),
           min_objective=min_objective, c=0.01, min_captured_correct=0.01,
           max_prefix_length=10, max_cache_size=max_cache_size, delimiter='\t',
           method=method, seed=0, sample=1., quiet=True, clear=True,
           garbage_collect=True)
    return (metadata, metrics, cache, priority_queue, best, rule_list)

def tdata_2():
    (metadata, metrics, cache, priority_queue, best, rule_list) = \
    bbound(din=os.path.join('..', 'data'), dout=os.path.join('..', 'cache'),
           dlog=os.path.join('..', 'logs'), dfigs=os.path.join('..', 'figs'),
           froot='tdata_R', warm_start=False, max_accuracy=0., best_prefix=(),
           min_objective=1., c=0., min_captured_correct=0.,
           max_prefix_length=90, max_cache_size=3000000, delimiter='\t',
           method='curiosity', seed=0, sample=1., quiet=True, clear=True,
           garbage_collect=True)
    return (metadata, metrics, cache, priority_queue, best, rule_list)

def tdata_3(min_objective=1., method='curiosity', max_cache_size=30000):
    (metadata, metrics, cache, priority_queue, best, rule_list) = \
    bbound(din=os.path.join('..', 'data'), dout=os.path.join('..', 'cache'),
           dlog=os.path.join('..', 'logs'), dfigs=os.path.join('..', 'figs'),
           froot='tdata_R', warm_start=False, max_accuracy=0., best_prefix=(),
           min_objective=min_objective, c=0.001, min_captured_correct=0.001,
           max_prefix_length=10, max_cache_size=max_cache_size, delimiter='\t',
           method=method, seed=0, sample=1., quiet=True, clear=True,
           garbage_collect=True)
    return (metadata, metrics, cache, priority_queue, best, rule_list)

def example_adult(method='breadth_first', max_cache_size=2600000, c=0.01):
    (metadata, metrics, cache, priority_queue, best, rule_list) = \
    bbound(din=os.path.join('..', 'data'), dout=os.path.join('..', 'cache'),
           dlog=os.path.join('..', 'logs'), dfigs=os.path.join('..', 'figs'),
           froot='adult_R', warm_start=False, max_accuracy=0., best_prefix=(),
           min_objective=1., c=c, min_captured_correct=c,
           max_prefix_length=10, max_cache_size=max_cache_size, delimiter='\t',
           method=method, seed=0, sample=0.1, quiet=True, clear=True,
           garbage_collect=True)
    return (metadata, metrics, cache, priority_queue, best, rule_list)

def example_telco(method='breadth_first', max_cache_size=3000000, c=0.01):
    (metadata, metrics, cache, priority_queue, best, rule_list) = \
    bbound(din=os.path.join('..', 'data'), dout=os.path.join('..', 'cache'),
           dlog=os.path.join('..', 'logs'), dfigs=os.path.join('..', 'figs'),
           froot='telco.shuffled', warm_start=False, max_accuracy=0., best_prefix=(),
           min_objective=1., c=c, min_captured_correct=c,
           max_prefix_length=10, max_cache_size=max_cache_size, delimiter='\t',
           method=method, seed=0, sample=1., quiet=True, clear=True,
           garbage_collect=True)
    return (metadata, metrics, cache, priority_queue, best, rule_list)

def small(froot, c=0.01, min_captured_correct=0.01, method='curiosity',
          max_cache_size=3000000):
    (metadata, metrics, cache, priority_queue, best, rule_list) = \
    bbound(din=os.path.join('..', 'data'), dout=os.path.join('..', 'cache'),
           dlog=os.path.join('..', 'logs'), dfigs=os.path.join('..', 'figs'),
           froot=froot, warm_start=False, max_accuracy=0., best_prefix=(),
           min_objective=1., c=c, min_captured_correct=min_captured_correct,
           max_prefix_length=20, max_cache_size=max_cache_size, delimiter='\t',
           method=method, seed=0, sample=1., quiet=True, clear=True,
           garbage_collect=True)
    return (metadata, metrics, cache, priority_queue, best, rule_list)

def bcancer():
    return small('bcancer_R')

def cars():
    return small('cars_R')

def haberman():
    return small('haberman_R')

def monks1():
    return small('monks1_R')

def monks2():
    return small('monks2_R')

def monks3():
    return small('monks3_R')

def votes():
    return small('votes_R')

def load_data(froot):
    label_file = '%s.label' % froot
    out_file = '%s.out' % froot
    (nrules, ndata, ones, rules, rule_set, rule_names,
     max_accuracy, min_objective, best_prefix, cache) = \
            initialize(din=os.path.join('..', 'data'),
                       dout=os.path.join('..', 'cache'),
                       label_file=label_file, out_file=out_file,
                       warm_start=False, max_accuracy=0., min_objective=1.,
                       best_prefix=(), seed=0, sample=1.)
    ones = utils.mpz_to_array(ones)
    rules = utils.rules_to_array(rules)
    commuting_pairs = utils.find_commuting_pairs(rules)
    cdict = utils.commuting_dict(commuting_pairs, nrules)
    rule_names = np.array(rule_names)
    return (nrules, ndata, ones, rules, rule_set, rule_names)

def tdata():
    return load_data(froot='tdata_R')

def adult():
    return load_data(froot='adult_R')

def small_datasets(dout='../results/', fout='small.md'):
    import pylab
    if not os.path.exists(dout):
        os.mkdir(dout)
    fh = open(os.path.join(dout, fout), 'w')
    descr = []
    fh.write('##small datasets (with varying amounts of regularization)\n\n')
    fh.write('without rule mining\n\n')
    fh.write('| dataset | c | d | time (s) | objective | lower bound | accuracy | upper bound | length |\n')
    fh.write('| --- | --- | --- | --- | --- | --- | --- | --- | --- |\n')
    template = '| %s | %1.3f | %1.3f | %2.3f | %1.3f | %1.3f | %1.3f | %1.3f | %d |\n'
    flist = ['bcancer', 'cars', 'haberman', 'monks1', 'monks2', 'monks3', 'votes']
    params = [(0.01, 0.01), (0.003, 0.003), (0.001, 0.001), (0., 0.)]
    for f in flist:
        froot = '%s_R' % f
        for (c, d) in params:
            print froot, c, d
            pylab.close('all')
            (metadata, metrics, cache, priority_queue, best, rule_list) = \
                                                              small(froot, c, d)
            rec = (f, c, d, metrics.seconds, best.objective, best.lower_bound,
                   best.accuracy, best.upper_bound, len(best.prefix))
            fh.write(template % rec)
            descr += [(f, c, d, rule_list, metadata)]
    for (f, c, d, rule_list, md) in descr:
        fh.write('\n###%s, c=%1.3f, d=%1.3f\n\n' % (f, c, d))
        rl = '\n'.join(['\t' + line for line in rule_list.strip().split('\n')])
        fh.write('%s\n' % rl)
        if os.path.exists('../figs/%s-log.png' % md):
            fh.write('\n![%s-log](../figs/%s-log.png)\n' % (md, md))
        if os.path.exists('../figs/%s-cache.png' % md):
            fh.write('![%s-cache](../figs/%s-cache.png)\n' % (md, md))
    fh.close()
    return

def adult_metrics(dout='../results/', fout='adult-metrics.md'):
    import pylab
    if not os.path.exists(dout):
        os.mkdir(dout)
    fh = open(os.path.join(dout, fout), 'w')
    descr = []
    fh.write('##adult dataset with different priority metrics (c = d = 0.01)\n\n')
    fh.write('stop after 2,600,000 cache entries\n\n')
    fh.write('| priority metric | time (s) | objective | lower bound | accuracy | upper bound | best prefix |\n')
    fh.write('| --- | --- | --- | --- | --- | --- | --- |\n')
    template = '| %s | %2.3f | %1.3f | %1.3f | %1.3f | %1.3f | %s |\n'
    params = ['breadth_first', 'curiosity', 'lower_bound', 'objective']
    f = 'adult'
    froot = '%s_R' % f
    for method in params:
        print froot, method
        pylab.close('all')
        (metadata, metrics, cache, priority_queue, best, rule_list) = \
                                    example_adult(method=method, max_cache_size=2600000)
        rec = (method, metrics.seconds, best.objective, best.lower_bound,
               best.accuracy, best.upper_bound, best.prefix.__repr__())
        fh.write(template % rec)
        descr += [(method, rule_list, metadata)]
    for (method, rule_list, md) in descr:
        fh.write('\n###%s\n\n' % (method))
        rl = '\n'.join(['\t' + line for line in rule_list.strip().split('\n')])
        fh.write('%s\n' % rl)
        if os.path.exists('../figs/%s-log.png' % md):
            fh.write('\n![%s-log](../figs/%s-log.png)\n' % (md, md))
        if os.path.exists('../figs/%s-leaves.png' % md):
            fh.write('![%s-cache](../figs/%s-leaves.png)\n' % (md, md))
        if os.path.exists('../figs/%s-cache.png' % md):
            fh.write('![%s-cache](../figs/%s-cache.png)\n' % (md, md))
    fh.close()
    return

def adult_regularize(dout='../results/', fout='adult-regularize.md'):
    import pylab
    if not os.path.exists(dout):
        os.mkdir(dout)
    fh = open(os.path.join(dout, fout), 'w')
    descr = []
    fh.write('##adult dataset with varying regularization (breadth-first, c = d, max_cache_size=3000000)\n\n')
    fh.write('stop after 3,000,000 cache entries\n\n')
    fh.write('| c | time (s) | objective | lower bound | accuracy | upper bound | best prefix |\n')
    fh.write('| --- | --- | --- | --- | --- | --- | --- |\n')
    template = '| %1.2f | %2.3f | %1.3f | %1.3f | %1.3f | %1.3f | %s |\n'
    params = np.arange(0.1, 0., -0.01)
    f = 'adult'
    froot = '%s_R' % f
    for c in params:
        print froot, c
        pylab.close('all')
        (metadata, metrics, cache, priority_queue, best, rule_list) = \
                        example_adult(method='breadth_first', max_cache_size=3000000, c=c)
        rec = (c, metrics.seconds, best.objective, best.lower_bound,
               best.accuracy, best.upper_bound, best.prefix.__repr__())
        fh.write(template % rec)
        descr += [(c, rule_list, metadata)]
    for (c, rule_list, md) in descr:
        fh.write('\n###c = %1.2f\n\n' % (c))
        rl = '\n'.join(['\t' + line for line in rule_list.strip().split('\n')])
        fh.write('%s\n' % rl)
        if os.path.exists('../figs/%s-log.png' % md):
            fh.write('\n![%s-log](../figs/%s-log.png)\n' % (md, md))
        if os.path.exists('../figs/%s-leaves.png' % md):
            fh.write('![%s-cache](../figs/%s-leaves.png)\n' % (md, md))
        if os.path.exists('../figs/%s-cache.png' % md):
            fh.write('![%s-cache](../figs/%s-cache.png)\n' % (md, md))
    fh.close()
    return

def tdata_driver(dout='../results/', fout='tdata.md'):
    import pylab
    if not os.path.exists(dout):
        os.mkdir(dout)
    fh = open(os.path.join(dout, fout), 'w')
    descr = []
    fh.write('##tic-tac-toe dataset (curiosity, c = d = 0.001)\n\n')
    f = 'tdata'
    froot = '%s_R' % f
    print froot
    pylab.close('all')
    (metadata, metrics, cache, priority_queue, best, rule_list) = tdata_3()
    descr += [(rule_list, metadata)]
    for (rule_list, md) in descr:
        rl = '\n'.join(['\t' + line for line in rule_list.strip().split('\n')])
        fh.write('%s\n' % rl)
        if os.path.exists('../figs/%s-log.png' % md):
            fh.write('\n![%s-log](../figs/%s-log.png)\n' % (md, md))
        if os.path.exists('../figs/%s-leaves.png' % md):
            fh.write('![%s-cache](../figs/%s-leaves.png)\n' % (md, md))
        if os.path.exists('../figs/%s-cache.png' % md):
            fh.write('![%s-cache](../figs/%s-cache.png)\n' % (md, md))
    fh.close()
    return (metadata, metrics, cache, priority_queue, best, rule_list)

def small_expanded(dout='../results/', foutroot='small_expanded', c=0.01,
                   max_cache_size=2000000):
    import pylab
    if not os.path.exists(dout):
        os.mkdir(dout)
    fout = '%s-max_cache_size=%d.md' % (foutroot, max_cache_size)
    fh = open(os.path.join(dout, fout), 'w')
    d = c
    descr = []
    fh.write('##small datasets (c=%1.3f, max_cache_size=%d)\n\n' % (c, max_cache_size))
    fh.write('expanded with maximum cardinality = 2 and minimum support = 10%\n\n')
    fh.write('| dataset | method | time (s) | cache | queue | objective | lower bound | accuracy | upper bound | length |\n')
    fh.write('| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |\n')
    template = '| %s | %s | %3.3f | %d | %d | %1.3f | %1.3f | %1.3f | %1.3f | %d |\n'
    flist = ['bcancer', 'cars', 'haberman', 'monks1', 'monks2', 'monks3', 'votes']
    params = [('breadth_first',), ('curiosity',)]
    for f in flist:
        froot = '%s' % f
        for (method,) in params:
            print froot, method
            pylab.close('all')
            (metadata, metrics, cache, priority_queue, best, rule_list) = \
                small(froot, c, d, method=method, max_cache_size=max_cache_size)
            rec = (f, method, metrics.seconds, len(cache), len(priority_queue), best.objective,
                   best.lower_bound, best.accuracy, best.upper_bound, len(best.prefix))
            fh.write(template % rec)
            descr += [(f, method, rule_list, metadata)]
    for (f, method, rule_list, md) in descr:
        fh.write('\n###%s, %s\n\n' % (f, method))
        rl = '\n'.join(['\t' + line for line in rule_list.strip().split('\n')])
        fh.write('%s\n' % rl)
        if os.path.exists('../figs/%s-log.png' % md):
            fh.write('\n![%s-log](../figs/%s-log.png)\n' % (md, md))
        if os.path.exists('../figs/%s-leaves.png' % md):
            fh.write('![%s-cache](../figs/%s-leaves.png)\n' % (md, md))
        if os.path.exists('../figs/%s-cache.png' % md):
            fh.write('![%s-cache](../figs/%s-cache.png)\n' % (md, md))
    fh.close()
    return

def telco_metrics(dout='../results/', fout='telco-metrics.md'):
    import pylab
    if not os.path.exists(dout):
        os.mkdir(dout)
    fh = open(os.path.join(dout, fout), 'w')
    descr = []
    fh.write('## telco dataset with different priority metrics (c = d = 0.01)\n\n')
    fh.write('stop after 2,000,000 cache entries\n\n')
    fh.write('| priority metric | time (s) | objective | lower bound | accuracy | upper bound | best prefix |\n')
    fh.write('| --- | --- | --- | --- | --- | --- | --- |\n')
    template = '| %s | %2.3f | %1.3f | %1.3f | %1.3f | %1.3f | %s |\n'
    params = ['breadth_first', 'curiosity'] #, 'lower_bound', 'objective']
    f = 'telco'
    froot = '%s.shuffled' % f
    for method in params:
        print froot, method
        pylab.close('all')
        (metadata, metrics, cache, priority_queue, best, rule_list) = \
                                    example_telco(method=method, max_cache_size=2000000)
        rec = (method, metrics.seconds, best.objective, best.lower_bound,
               best.accuracy, best.upper_bound, best.prefix.__repr__())
        fh.write(template % rec)
        descr += [(method, rule_list, metadata)]
    for (method, rule_list, md) in descr:
        fh.write('\n###%s\n\n' % (method))
        rl = '\n'.join(['\t' + line for line in rule_list.strip().split('\n')])
        fh.write('%s\n' % rl)
        if os.path.exists('../figs/%s-log.png' % md):
            fh.write('\n![%s-log](../figs/%s-log.png)\n' % (md, md))
        if os.path.exists('../figs/%s-leaves.png' % md):
            fh.write('![%s-cache](../figs/%s-leaves.png)\n' % (md, md))
        if os.path.exists('../figs/%s-cache.png' % md):
            fh.write('![%s-cache](../figs/%s-cache.png)\n' % (md, md))
    fh.close()
    return
