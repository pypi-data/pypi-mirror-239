import numpy as np


def codificador(m, P, G, tipo=1):
    if tipo == 1:     # codificação não sistemática (padrão)
        pre_c = np.zeros(G.shape[1], dtype=int)
        pre_c[P == 2] = m
        c = np.mod(np.dot(pre_c, G), 2)
    elif tipo == 2:   # codificação sistemática (ver referência [3] figura 01)
        mascara = np.ones(G.shape[1], dtype=int)
        mascara[P == 2] = 0
        pre_c = np.logical_and(m, mascara).astype(int)
        c = np.mod(np.dot(pre_c, G), 2)
    else:
        raise ValueError(
            "O valor de 'tipo' deve ser 1 (codificação não sistemática) ou 2 (codificação sistemática).")

    return c
