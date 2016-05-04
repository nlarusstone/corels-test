import matplotlib.pyplot as plt
import numpy as np

from branch_bound import print_rule_list


def mpz_to_string(x):
    # skip leading 1
    return "{0}".format(x.digits(2))[1:]

def mpz_to_array(x):
    return np.cast['uint8']([i for i in mpz_to_string(x)])

def array_to_string(x):
    return ''.join(np.cast[str](x))

def prefix_trace(prefix, cache, rule_names=None, ndata=None, rules=None, ones=None, m=100):
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
    print
    print '0 = not captured'
    print '1 = captured'
    for i in range(1, n):
        c = cache[prefix[:i]]
        captured = 1 - mpz_to_array(c.not_captured)
        print array_to_string(captured[:m])
    if (rules is not None):
        labels = mpz_to_array(ones)
        print
        print '0 = not captured'
        print '1 = captured and not correct'
        print '3 = captured and correct'
        state = np.zeros(ndata, dtype='uint8')
        for i in range(n):
            pfx = prefix[:i]
            c = cache[pfx]
            captured = 1 - mpz_to_array(c.not_captured)
            if i:
                rule = mpz_to_array(rules[pfx[-1]])
                correct = (labels == c.prediction[-1])
                new_captured = (state == 0) & (captured == 1)
                state[new_captured & np.invert(correct)] = 1
                state[new_captured & correct] = 3
            print array_to_string(state[:m])
        print
        print '0 = not captured and incorrect by default'
        print '1 = captured and not correct'
        print '2 = not captured and correct by default'
        print '3 = captured and correct'
        state = np.zeros(ndata, dtype='uint8')
        captured_viz = np.zeros((n, m), int)
        correct_viz = np.zeros((n, m), int)
        complete_viz = np.zeros((n, m), int)
        for i in range(n):
            pfx = prefix[:i]
            c = cache[pfx]
            captured = 1 - mpz_to_array(c.not_captured)
            captured_viz[i,:] = captured[:m].copy()
            if i:
                rule = mpz_to_array(rules[pfx[-1]])
                correct = (labels == c.prediction[-1])
                new_captured = (state == 0) & (captured == 1)
                state[new_captured & np.invert(correct)] = 1
                state[new_captured & correct] = 3
                correct_viz[i,:] = state[:m].copy()
            with_default = state.copy()
            with_default[(state == 0) & (labels == c.default_rule)] = 2
            complete_viz[i,:] = with_default[:m].copy()
            print array_to_string(with_default[:m])
        plt.figure(2, figsize=(14, 6))
        plt.clf()
        plt.pcolor(captured_viz[::-1], cmap='coolwarm', vmin=0, vmax=3)
        plt.axis('tight')
        plt.colorbar(ticks=range(-1, 4), format='%d')
        plt.figure(3, figsize=(14, 6))
        plt.clf()
        plt.pcolor(correct_viz[::-1], cmap='coolwarm', vmin=0, vmax=3)
        plt.axis('tight')
        plt.colorbar(ticks=range(-1, 4), format='%d')
        plt.figure(4, figsize=(14, 6))
        plt.clf()
        plt.pcolor(complete_viz[::-1], cmap='coolwarm', vmin=0, vmax=3)
        plt.axis('tight')
        plt.colorbar(ticks=range(-1, 4), format='%d')

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
