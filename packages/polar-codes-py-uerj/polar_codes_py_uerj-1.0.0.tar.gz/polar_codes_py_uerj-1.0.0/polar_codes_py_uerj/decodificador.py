import numpy as np


from . import codificador
from polar_codes_py_uerj.calculaRETRO import calculaRETRO
from polar_codes_py_uerj.calculaLLR import calculaLLR


def decodificador(y, N, Ec, N0, polarizacao, IndexRETRO, MatrizG, aux_col, mapa, sequencia_W, tipo=1):
    initialLRs = -(4 * np.sqrt(Ec) / N0) * y
    du = np.zeros(N, dtype=int)
    ru = np.zeros(N, dtype=int)
    n = int(np.log2(N))
    retro = np.zeros((N // 2, n), dtype=int)
    contador = 2**(np.arange(n-1, -1, -1))
    LLR = np.zeros((N, n+1))
    LLR[:, 0] = initialLRs
    aux_LLR = np.zeros(N, dtype=float)

    for j in range(N):
        i = sequencia_W[j]-1
        # calcula a evolução das LLR
        LLR = calculaLLR(N, mapa[j, :], retro, aux_col[j], LLR, IndexRETRO)
        aux_LLR[i] = LLR[0, n]

        if polarizacao[i] == 2:
            if LLR[0, n] > 0:
                du[i] = 0
            else:
                du[i] = 1
        else:
            du[i] = 0

        ru[j] = du[i]
        # calcula matriz de retroalimentação das LLR
        retro, contador = calculaRETRO(ru, j, MatrizG, retro, contador)

    u = du[polarizacao == 2]

    if tipo == 2:
        du = codificador(u, polarizacao, MatrizG, 1)
        u = du[polarizacao == 2]

    return u
