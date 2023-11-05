import numpy as np
import math

from polar_codes_py_uerj.convertobin import convertobin


def auxCol(N):
    N = int(2**np.ceil(np.log2(N)))
    aux = N - 1
    n = int(math.log2(N))
    col = np.zeros(N, dtype=int)
    for j in range(1, N+1):
        col[j-1] = np.sum(np.logical_xor(convertobin(format(j-1, 'b').zfill(n)),
                          convertobin(format(aux, 'b').zfill(n)))) - 1
        aux = j - 1
    return col
