import math

import numpy as np
import pylab

def compute_max_prefix_length(nrules, min_objective, c):
    if (c == 0.):
        return nrules
    else:
        max_prefix_length = int(min_objective / c)
        if (max_prefix_length > nrules):
            return nrules
        else:
            return max_prefix_length

def state_space_size(nrules, min_objective=0.50, c=0.01):
    """
    min_objective = objective of the empty rule list <= 0.50

    """
    max_prefix_length = compute_max_prefix_length(nrules, min_objective, c)

    # sum_{k=0}^K ( M! / (M - k)! ), K = max_prefix_length, M = nrules
    Mf = math.factorial(nrules)
    return sum([Mf / math.factorial(nrules - k) for k in range(max_prefix_length + 1)])

def remaining_search_space(nrules, min_objective, c=0.01, prefix_lengths=[[0, 1]]):
    """
    min_objective = current best objective

    prefix_lengths[i] = the number of prefixes of length i in the queue

    """
    M = compute_max_prefix_length(nrules, min_objective, c)

    # sum_{j=0}^M Q_j sum_{k=1}^{K-j} (M - j)! / (M - j - k)!
    j_Qj_Mj = [(j, Qj, math.factorial(M - j)) for (j, Qj) in prefix_lengths]
    return sum([Qj * sum([Mj / math.factorial(M - j - k)
                for k in range(1, M - j + 1)]) for (j, Qj, Mj) in j_Qj_Mj])

def test_state_space():
    nrules = 100
    min_objective = 0.50
    c = 0.01
    print 'nrules:', nrules
    print 'min_objective:', min_objective
    print 'c:', c
    total_size = state_space_size(nrules, min_objective, c)
    size_after_init = remaining_search_space(nrules, min_objective, c)
    print 'total state space size:', total_size
    print 'after first evaluation:', size_after_init
    assert (total_size == (size_after_init + 1))
    print 'asserted: total state space size = (size after first eval) + 1'

    step = 0.01
    min_objective_vec = np.arange(0., 0.50 + step, step)
    remaining = [remaining_search_space(nrules, m, c) for m in min_objective_vec]
    fraction_remaining = [float(r) / float(total_size) for r in remaining]
    print fraction_remaining

    pylab.ion()
    pylab.figure(1)
    pylab.clf()
    pylab.semilogy(min_objective_vec, remaining, 'b-', marker='o', markerfacecolor='r')
    pylab.xlabel('current best objective')
    pylab.ylabel('size of remaining search space')
    
    pylab.figure(2)
    pylab.clf()
    pylab.semilogy(min_objective_vec[1:], fraction_remaining[1:], 'b-', marker='o', markerfacecolor='r')
    pylab.xlabel('current best objective')
    pylab.ylabel('fraction of search space remaining')
    return
