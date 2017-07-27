"""
E.g., first run the script `adult.py` in the directory `processing`, then do

$ python eval_model.py adult -n 1000 -r 0.01 -b -p 1

or

$ python eval_model.py adult --parallel -n 100000 -r 0.01 -c 1 -p 1

or

$ python eval_model.py adult --parallel --minor -n 1000 -r 0.01 -c 1 -p 1

"""
import argparse
import subprocess

import numpy as np
import pandas as pd


parser = argparse.ArgumentParser(description='Find rulelist and evaluate on model')
parser.add_argument('-s', action='store_true')
parser.add_argument('-b', action='store_true')
parser.add_argument('-n', type=str, metavar='max_num_nodes', default='100000')
parser.add_argument('-r', type=str, metavar='regularization', default='0.01')
parser.add_argument('-v', type=str, metavar='verbosity', default='2')
parser.add_argument('-c', type=str, metavar='(1|2|3|4)')
parser.add_argument('-a', type=str, metavar='(1|2)')
parser.add_argument('-p', type=str, metavar='(0|1|2)')
parser.add_argument('-f', type=str, metavar='logging_frequency', default='1000')
parser.add_argument('fname')
parser.add_argument('--parallel', action='store_true')
parser.add_argument('--minor', action='store_true')
parser.add_argument('-k', type=int, default=10)
parser.add_argument('--sparsity', type=str, default='')

def run_model(fname, log_fname):
    with open(log_fname, 'r') as f:
        line = f.readline()
        opt = map(lambda x: x.split('~'), line.split(';'))
        opt = map(lambda x: (x[0], int(x[1])), opt)
        #print opt

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
    true_positive = 0
    false_positive = 0
    false_negative = 0
    true_negative = 0
    for (ind, pred) in preds:
        correct = label.iloc[pred, ind]
        corr += correct
        if (pred == 1):
            if (correct == 1):
                true_positive += 1
            else:
                false_positive += 1
        else:
            if (correct == 1):
                true_negative += 1
            else:
                false_negative += 1
    acc = float(corr) / float(nrules)
    print 'Accuracy: ', acc
    print 'True Positive  | False Negative || %d | %d' % (true_positive, false_negative)
    print 'False Positive | True Negative  || %d | %d' % (false_positive, true_negative)

    return (len(opt), acc, [true_positive, false_negative, false_positive, true_negative])

if __name__ == '__main__':
    args = parser.parse_args()
    num_folds = args.k
    accuracies = []
    test_accuracies = []
    ctables = []
    test_ctables = []
    plist = []
    log_list = []
    for i in range(num_folds):
        print args
        fxn = ['../src/corels']
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
            if (args.c == '1'):
                log_fname += 'curiosity-'
            elif (args.c == '2'):
                log_fname += 'curious_lb-'
            else:
                log_fname += 'curious_obj-'
        if args.p:
            fxn.append('-p ' + args.p)
            log_fname += ('with_prefix_perm_map-' if args.p == '1' else 'with_captured_symmetry_map-') if args.p != '0' else 'no_pmap-'
        else:
            log_fname += 'no_pmap-'
        if args.minor:
            log_fname += 'minor-'
        else:
            log_fname += 'no_minor-'
	if args.a:
	    log_fname += 'removed={0}-'.format('support' if args.a == '1' else 'lookahead')
	else:
	    log_fname += 'removed=none-'
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
        log_list.append(log_fname)
        fxn.append(out)
        fxn.append(label)
        if args.minor:
            minor = '../data/CrossValidation/' + fname + '.minor'
            fxn.append(minor)
        print ' '.join(fxn)
        if (not args.parallel):
            proc = subprocess.check_call(fxn)
	    #proc.wait()
            print
            train_name = args.fname + '_' + str(i) + '_train'
            (len_opt, train_acc, ct) = run_model(train_name, log_list[i])
            accuracies.append(train_acc)
            ctables.append(ct)
            print '---- Calculating Validation Accuracy For Fold {0} -----'.format(i)
            print
            test_name = args.fname + '_' + str(i) + '_test'
            (len_opt, acc, ct) = run_model(test_name, log_list[i])
            test_accuracies.append(acc)
            test_ctables.append(ct)
            if args.sparsity:
                cv_fold = args.fname + '_' + str(i)
                with open(args.sparsity, 'a') as f:
                    f.write("{0},CORELS,0,0,{1},{2},{3},{4}\n".format(cv_fold, args.r, acc, len_opt, train_acc))
        else:
            plist.append(subprocess.Popen(fxn))

    if (args.parallel):
        for i in range(num_folds):
            plist[i].wait()
            train_name = args.fname + '_' + str(i) + '_train'
            test_name = args.fname + '_' + str(i) + '_test'
            (len_opt, acc, ct) = run_model(test_name, log_list[i])
            test_accuracies.append(acc)
            test_ctables.append(ct)
            if args.sparsity:
                cv_fold = args.fname + '_' + str(i)
                with open(args.sparsity, 'a') as f:
                    f.write("{0},CORELS,0,0,{1},{2},{3},{4}\n".format(cv_fold, args.r, acc, len_opt, train_acc))

    print
    if (not args.parallel):
        print 'Train contingency tables', ctables
    print 'Test contingency tables', test_ctables
    if (not args.parallel):
        ctables = np.array(ctables)
    test_ctables = np.array(test_ctables)
    print 'True Positive, False Negative, False Positive, True Negative'
    if (not args.parallel):
        print 'Train contingency table means', np.round(np.mean(ctables, axis=0).reshape(2, 2))
        print 'Train contingency table std', np.round(np.std(ctables, axis=0).reshape(2, 2))
    print
    print 'Test contingency table means', np.round(np.mean(test_ctables, axis=0).reshape(2, 2))
    print 'Test contingency table std', np.round(np.std(test_ctables, axis=0).reshape(2, 2))
    print
    if (not args.parallel):
        print 'Train accuracies', accuracies
        print 'Train accuracies mean, std', np.mean(accuracies), np.std(accuracies)
    print
    print 'Test accuracies', test_accuracies
    print 'Test accuracies mean, std', np.mean(test_accuracies), np.std(test_accuracies)
