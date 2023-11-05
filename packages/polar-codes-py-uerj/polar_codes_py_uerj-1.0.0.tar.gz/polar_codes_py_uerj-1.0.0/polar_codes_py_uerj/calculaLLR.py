import numpy as np

from polar_codes_py_uerj.funcao_F import funcao_F
from polar_codes_py_uerj.funcao_G import funcao_G


def calculaLLR(N, mapa, retro, aux_col, LLR, IndexRETRO):
    colunas = int(np.log2(N))
    linhas = N
    inic_colunas = (colunas + 1) - aux_col

    for i in range(inic_colunas, colunas + 2):
        aux = linhas // 2 ** (i - 1)
        pos_linha = 0
        for j in range(1, aux+1):
            if mapa[i - 2] == 0:
                LLR[j-1, i-1] = funcao_F(LLR[pos_linha, i - 2],
                                         LLR[pos_linha + 1, i - 2])
            else:
                r = IndexRETRO[j-1, i-2] - 1
                LLR[j-1, i-1] = funcao_G(LLR[pos_linha + 1, i - 2],
                                         LLR[pos_linha, i - 2], retro[r, i - 2])
            pos_linha += 2
    return LLR
