import numpy as np


def mpz_to_string(x):
    # skip leading 1
    return "{0}".format(x.digits(2))[1:]

def mpz_to_array(x):
    return np.cast['uint8']([i for i in mpz_to_string(x)])

def array_to_string(x):
    return ''.join(np.cast[str](x))

def rules_to_array(x):
    return np.array([mpz_to_array(r) for r in x])

def relationships(x):
    n = x.shape[0]
    num_pairs = (n * (n - 1)) / 2
    d = np.dot(x, x.T)
    num_commuting_pairs = (d == 0).sum() / 2
    print num_pairs, num_commuting_pairs
    mask = np.triu(np.ones(d.shape, int))
    mask = mask - np.identity(d.shape[0], int)
    return zip(((d == 0) & mask).nonzero())
