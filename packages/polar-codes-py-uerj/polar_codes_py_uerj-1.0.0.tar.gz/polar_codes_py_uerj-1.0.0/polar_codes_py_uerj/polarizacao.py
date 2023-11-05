import numpy as np

from polar_codes_py_uerj.fbitreversed import fbitreversed


def polarizacao(N, K, designSNRdB=0):
    colunas = int(np.log2(N))
    linhas = N
    W = np.zeros((linhas, colunas + 1))
    designSNR = 10**(designSNRdB/10)
    W[0, 0] = -designSNR

    for i in range(2, colunas + 2):
        aux = 2**(i - 1) // 2
        pos_linha = 0
        for j in range(int(aux)):
            W[pos_linha, i-1] = np.log(2) + W[j, i - 2] + np.log(
                1 - np.exp(2 * W[j, i - 2] - (np.log(2) + W[j, i - 2])))
            W[pos_linha + 1, i-1] = 2 * W[j, i - 2]
            pos_linha += 2

    aux = fbitreversed(np.arange(N), colunas)
    W0 = W[:, colunas]

    W_aux = np.zeros(N, dtype=float)
    for r in range(N):
        W_aux[r] = W0[aux[r]-1]

    rank = np.argsort(W_aux, axis=0)

    P = np.zeros(N, dtype=int)
    for j in range(K):
        P[rank[j]] = 2

    return P
