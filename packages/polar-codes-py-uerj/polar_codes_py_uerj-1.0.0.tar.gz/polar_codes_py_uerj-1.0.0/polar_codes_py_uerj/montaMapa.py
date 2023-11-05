import numpy as np

from polar_codes_py_uerj.fbitreversed import fbitreversed
from polar_codes_py_uerj.convertobininv import convertobininv


def montaMapa(N):
    N = int(2**np.ceil(np.log2(N)))
    n = int(np.log2(N))
    mp = np.zeros((N, n), dtype=int)
    sequencia_W = fbitreversed(np.arange(N), n)

    for j in range(N):
        i = sequencia_W[j]
        mp[j, :] = convertobininv(format(i-1, f'0{n}b'))

    return mp
