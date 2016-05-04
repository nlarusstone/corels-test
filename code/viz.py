import matplotlib.pyplot as plt
import numpy as np

from branch_bound import print_rule_list

def prefix_trace(prefix, cache, rule_names=None, ndata=None):
    n = len(prefix) + 1
    accuracy = np.zeros(n)
    upper_bound = np.zeros(n)
    curiosity = np.zeros(n)
    num_captured = np.zeros(n, int)
    num_captured_correct = np.zeros(n, int)
    for i in range(n):
        c = cache[prefix[:i]]
        accuracy[i] = c.accuracy
        upper_bound[i] = c.upper_bound
        curiosity[i] = c.curiosity
        num_captured[i] = c.num_captured
        num_captured_correct[i] = c.num_captured_correct
    c = cache[prefix]
    print c
    if (rule_names is not None):
        print_rule_list(prefix, c.prediction, c.default_rule, rule_names)    
    plt.figure(1, figsize=(10, 4))
    plt.clf()
    plt.subplot(1, 2, 1)
    plt.plot(range(n), upper_bound, ':', marker='.')
    plt.plot(range(n), accuracy, '-', marker='.')
    plt.plot(range(n), curiosity, '--', marker='.')
    plt.axis('tight')
    plt.legend(('upper bound', 'accuracy', 'curiosity'), loc='best')
    plt.subplot(1, 2, 2)
    plt.plot(range(n), num_captured, ':', marker='.')
    plt.plot(range(n), num_captured_correct, '-', marker='.')
    a = list(plt.axis('tight'))
    plt.legend(('num captured', 'num captured correct'), loc='best')
    if (ndata is not None):
        a[3] = ndata
        plt.axis(a)
    return
