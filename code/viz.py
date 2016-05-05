import matplotlib.pyplot as plt
import numpy as np

from branch_bound import print_rule_list
import utils


def data_redundancy(prefix, cache, ndata=None, rules=None, ones=None, fs=14, lw=3):
    n = len(prefix) + 1
    ones = utils.mpz_to_array(ones)
    rules = utils.rules_to_array(rules)
    x = np.vstack((ones, rules))
    num_uncaptured = np.zeros(n, int)
    num_unique = np.zeros(n, int)
    for i in range(n):
        pfx = prefix[:i]
        c = cache[pfx]
        not_captured_ind = np.nonzero(utils.mpz_to_array(c.not_captured))[0]
        num_uncaptured[i] = len(not_captured_ind)
        num_unique[i] = len(set([tuple(col) for col in (x.T)[not_captured_ind]]))
        # print i, num_uncaptured[i], num_unique[i]
    plt.figure(1, figsize=(6, 4.5))
    plt.clf()
    plt.plot(range(n), num_uncaptured / float(ndata), ':', marker='o', linewidth=lw)
    plt.plot(range(n), num_unique / float(ndata), '-', marker='o', linewidth=lw)
    plt.axis([0, n - 1, 0, 1])
    plt.legend(('uncaptured', 'uncaptured unique'))
    plt.xlabel('prefix length', fontsize=fs)
    plt.ylabel('fraction', fontsize=fs)
    plt.xticks(fontsize=fs)
    plt.yticks(fontsize=fs)
    return

def data_points(prefix, rule_names=None, ndata=None, rules=None, ones=None,
                m=150, quiet=True, fs=14):
    n = len(prefix)
    labels = utils.mpz_to_array(ones)[:m].reshape((1, m))
    data = np.array([utils.mpz_to_array(rules[p]) for p in prefix])[:,:m]
    plt.figure(3, figsize=(14, 7.5))
    plt.subplot2grid((11, 1), (0, 0))
    plt.pcolor(labels, cmap='coolwarm', vmin=0, vmax=3)
    plt.axis('tight')
    plt.xlabel('data index', fontsize=fs)
    plt.ylabel('label', fontsize=fs)
    plt.xticks(fontsize=fs)
    plt.yticks([])
    plt.subplot2grid((11, 1), (2, 0), rowspan=9)
    plt.pcolor(data[::-1], cmap='coolwarm', vmin=0, vmax=3)
    plt.axis('tight')
    plt.xlabel('data index', fontsize=fs)
    plt.ylabel('prefix index', fontsize=fs)
    plt.xticks(fontsize=fs)
    plt.yticks(np.arange(n) + 0.5, np.arange(1, n+1)[::-1], fontsize=fs)
    return

def prefix_trace(prefix, cache, rule_names=None, ndata=None, rules=None,
                 ones=None, m=150, quiet=True, fs=14, lw=3):
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
    if not quiet:
        print
        print '0 = not captured'
        print '1 = captured'
        for i in range(1, n):
            c = cache[prefix[:i]]
            captured = 1 - utils.mpz_to_array(c.not_captured)
            print utils.array_to_string(captured[:m])
    if (rules is not None):
        labels = utils.mpz_to_array(ones)
        if not quiet:
            print
            print '0 = not captured'
            print '1 = captured and not correct'
            print '3 = captured and correct'
            state = np.zeros(ndata, dtype='uint8')
            for i in range(n):
                pfx = prefix[:i]
                c = cache[pfx]
                captured = 1 - utils.mpz_to_array(c.not_captured)
                if i:
                    rule = utils.mpz_to_array(rules[pfx[-1]])
                    correct = (labels == c.prediction[-1])
                    new_captured = (state == 0) & (captured == 1)
                    state[new_captured & np.invert(correct)] = 1
                    state[new_captured & correct] = 3
                print utils.array_to_string(state[:m])
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
            captured = 1 - utils.mpz_to_array(c.not_captured)
            captured_viz[i,:] = captured[:m].copy()
            if i:
                rule = utils.mpz_to_array(rules[pfx[-1]])
                correct = (labels == c.prediction[-1])
                new_captured = (state == 0) & (captured == 1)
                state[new_captured & np.invert(correct)] = 1
                state[new_captured & correct] = 3
                correct_viz[i,:] = state[:m].copy()
            with_default = state.copy()
            with_default[(state == 0) & (labels == c.default_rule)] = 2
            complete_viz[i,:] = with_default[:m].copy()
            if not quiet:
                print utils.array_to_string(with_default[:m])
        plt.figure(4, figsize=(14, 6))
        plt.clf()
        plt.pcolor(captured_viz[::-1], cmap='coolwarm', vmin=0, vmax=3)
        plt.title('(dark blue) uncaptured, (light blue) captured', fontsize=fs)
        plt.xlabel('data index', fontsize=fs)
        plt.figure(5, figsize=(14, 6))
        plt.clf()
        plt.pcolor(correct_viz[::-1], cmap='coolwarm', vmin=0, vmax=3)
        plt.title('(dark blue) uncaptured, (red) captured & correct\n' +
                  '(light blue) captured & incorrect', fontsize=fs)
        plt.figure(6, figsize=(14, 6))
        plt.clf()
        plt.pcolor(complete_viz[::-1], cmap='coolwarm', vmin=0, vmax=3)
        plt.title('(pink) uncaptured & correct by default, ' +
                  '(red) captured & correct\n' +
                  '(dark blue) uncaptured & incorrect by default, ' +
                  '(light blue) captured & incorrect', fontsize=fs)
        for fig in [4, 5, 6]:
            plt.figure(fig)
            plt.xlabel('data index', fontsize=fs)
            plt.ylabel('prefix length', fontsize=fs)
            plt.xticks(fontsize=fs)
            plt.yticks(np.arange(n) + 0.5, range(n)[::-1], fontsize=fs)
            plt.axis('tight')
            # plt.colorbar(ticks=range(-1, 4), format='%d')

    c = cache[prefix]
    print c
    if (rule_names is not None):
        print_rule_list(prefix, c.prediction, c.default_rule, rule_names)    
    plt.figure(2, figsize=(12, 4))
    plt.clf()
    plt.subplot(1, 2, 1)
    plt.plot(range(n), upper_bound, ':', marker='o', linewidth=lw)
    plt.plot(range(n), accuracy, '-', marker='o', linewidth=lw)
    plt.plot(range(n), curiosity, '--', marker='o', linewidth=lw)
    plt.legend(('upper bound', 'accuracy', 'curiosity'), loc='best')
    plt.subplot(1, 2, 2)
    plt.plot(range(n), num_captured / float(ndata), ':', marker='o', linewidth=lw)
    plt.plot(range(n), num_captured_correct / float(ndata), '-', marker='o', linewidth=lw)
    a = list(plt.axis('tight'))
    plt.legend(('fraction captured', 'fraction captured & correct'), loc='best')
    for j in [1, 2]:
        plt.subplot(1, 2, j)
        plt.axis([0, n - 1, 0, 1])
        plt.xlabel('prefix length', fontsize=fs)
        plt.xticks(fontsize=fs)
        plt.yticks(fontsize=fs)
    return
