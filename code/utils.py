import numpy as np


def mpz_to_string(x):
    # skip leading 1
    return "{0}".format(x.digits(2))[1:]

def mpz_to_array(x):
    return np.cast['uint8']([i for i in mpz_to_string(x)])

def array_to_string(x):
    return ''.join(np.cast[str](x))
