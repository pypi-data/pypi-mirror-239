import numpy as np
import math


def MatrizGeradora(N, tipo=1):
    # tipo = 1; Kronecker normal
    # tipo = 2; Kronecker com bitrevorder
    if N == 1:
        G = np.array([[1]])
        return G
    N = 2 ** math.ceil(math.log2(N))
    f = np.array([[1, 0], [1, 1]])
    G = f
    dimensao = int(np.log2(N))

    for i in range(1, dimensao):
        G = np.kron(G, f)

    if tipo == 2:
        indices_bitreversed = np.arange(N)
        indices_bitreversed = np.array(
            [int(format(i, f'0{dimensao}b')[::-1], 2) for i in indices_bitreversed])
        G = G[indices_bitreversed]

    return G
