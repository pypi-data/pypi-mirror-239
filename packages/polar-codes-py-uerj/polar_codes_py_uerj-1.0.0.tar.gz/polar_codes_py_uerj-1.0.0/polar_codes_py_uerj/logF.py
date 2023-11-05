import numpy as np


def logF(ra, rb):
    if ra < rb:
        r = rb + np.log(1 + np.exp(ra - rb))
    else:
        r = ra + np.log(1 + np.exp(rb - ra))
    return r
