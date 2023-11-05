import numpy as np
import math

from polar_codes_py_uerj.fbitreversed import fbitreversed


def GeraIndexRETRO(N):
    N = 2**math.ceil(math.log2(N))
    n = int(math.log2(N))
    ind_retro = np.zeros((N//2, n), dtype=int)
    aux_ind_retro = ind_retro.copy()

    for i in range(1, n+1):
        aux_ind_retro[:2**(n-i), i-1] = np.arange(1, 2**(n-i)+1)

    for i in range(1, n+1):
        aux = aux_ind_retro[:2**(n-i), i-1] - 1
        ind_retro[:2**(n-i), i-1] = fbitreversed(aux, n-i)

    return ind_retro
