import pandas as pd
import argparse
import re
import subprocess

parser = argparse.ArgumentParser(description='Find rulelist and evaluate on model')
parser.add_argument('-s', action='store_true')
parser.add_argument('-b', action='store_true')
parser.add_argument('-n', type=str, metavar='max_num_nodes', default='100000')
parser.add_argument('-r', type=str, metavar='regularization', default='0.01')
parser.add_argument('-v', type=str, metavar='verbosity', default='1')
parser.add_argument('-c', type=str, metavar='(1|2|3)')
parser.add_argument('-p', type=str, metavar='(0|1|2)')
parser.add_argument('-f', type=str, metavar='logging_frequency', default='1000')
parser.add_argument('fname')
parser.add_argument('--parallel', action='store_true')
#parser.add_argument('label')

def run_model(fname, log_fname):
    with open(log_fname, 'r') as f:
        line = f.readline()
        opt = map(lambda x: x.split('~'), line.split(';'))
        opt = map(lambda x: (x[0], int(x[1])), opt)
        #print opt

    fname = re.sub('train', 'test', fname)
    nrules = 0
    try:
        with open('../data/{0}.out'.format(fname)) as f:
            line = f.readline()
            nrules = len(line.split()) - 1
        out = pd.read_csv('../data/{0}.out'.format(fname), sep=' ', names=['Rule'] + range(nrules))
        label = pd.read_csv('../data/{0}.label'.format(fname), sep=' ', names=['Rule'] + range(nrules))
    except:
        with open('../data/CrossValidation/{0}.out'.format(fname)) as f:
            line = f.readline()
            nrules = len(line.split()) - 1
        out = pd.read_csv('../data/CrossValidation/{0}.out'.format(fname), sep=' ', names=['Rule'] + range(nrules))
        label = pd.read_csv('../data/CrossValidation/{0}.label'.format(fname), sep=' ', names=['Rule'] + range(nrules))

    out.set_index('Rule', inplace=True)
    label.set_index('Rule', inplace=True)

    captured = set()
    preds = []
    for (rule, pred) in opt[:-1]:
        cappd = out.ix[rule] == 1
        unfiltered_cappd = set(out.T[cappd].index)
        filtered_cappd = unfiltered_cappd.difference(captured)
        preds += map(lambda x: (x, pred), filtered_cappd)
        captured = captured.union(filtered_cappd)
        
    # Handle default rule
    _, def_pred = opt[-1]
    preds += [(x, def_pred) for x in set(range(nrules)).difference(captured)]

    corr = 0
    for (ind, pred) in preds:
        corr += label.iloc[pred, ind]
    acc = float(corr) / float(nrules)
    print 'Validation accuracy: ', acc
    return acc

if __name__ == '__main__':
    args = parser.parse_args()
    num_folds = 10
    accuracies = []
    plist = []
    for i in range(num_folds):
        print args
        fxn = ['../src/bbcache']
        fname = args.fname + '_' + str(i) + '_train'
        out = '../data/CrossValidation/' + fname + '.out'
        label = '../data/CrossValidation/' + fname + '.label'
        print fname
        print out
        log_fname = '../logs/for-{0}.out-'.format(fname)
        if args.s:
            fxn.append('-s')
            log_fname += 'stochastic-'
        if args.b:
            fxn.append('-b')
            log_fname += 'bfs-'
        if args.c:
            fxn.append('-c ' + args.c)
            log_fname += 'curiosity-' if args.c == '1' else 'curious_lb-'
        if args.p:
            fxn.append('-p ' + args.p)
            log_fname += ('with_prefix_perm_map-' if args.p == '1' else 'with_captured_symmetry_map-') if args.p != '0' else 'no_pmap-'
        if args.n:
            fxn.append('-n ' + args.n)
            log_fname += 'max_num_nodes={0}-'.format(args.n)
        if args.r:
            fxn.append('-r ' + args.r)
            log_fname += 'c=%.7f-' % float(args.r)
        if args.v:
            fxn.append('-v ' + args.v)
            log_fname += 'v={0}-'.format(args.v)
        if args.f:
            fxn.append('-f ' + args.f)
            log_fname += 'f={0}'.format(args.f)
        log_fname += '-opt.txt'
        fxn.append(out)
        fxn.append(label)
        if (not args.parallel):
            exit_code = subprocess.call(fxn)
            print
            print '---- Calculating Validation Accuracy For Fold {0} -----'.format(i)
            print
            accuracies.append(run_model(fname, log_fname))
        else:
            print 'Popen', fxn
            plist.append(subprocess.Popen(fxn))

    if (args.parallel):
        for i in range(num_folds):
            plist[i].wait()
            fname = args.fname + '_' + str(i) + '_train'
            accuracies.append(run_model(fname, log_fname))

    print
    print 'Accuracies'
    print accuracies
