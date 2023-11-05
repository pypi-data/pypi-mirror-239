import numpy as np


def calculaRETRO(u, W, MatrizG, retro, contador):
    cont_canal = W+1
    N = len(u)
    n = int(np.log2(N))
    flag = np.ones(n, dtype=int)
    i = cont_canal
    contador -= 1
    aux = 0
    for s in range(n, 0, -1):
        aux += 1
        if contador[s-1] == 0:
            if flag[s-1] == 1:
                inicio = i - (2**(aux-1) - 1) - 1
                tempG = MatrizG[:2**(aux-1), :2**(aux-1)]
                tempu = u[inicio:i]
                tempr = np.mod(np.dot(tempu, tempG), 2)
                retro[:2**(aux-1), s-1] = tempr
                contador[s-1] = 2**(aux-1)
                flag[s-1] = 0
            else:
                contador[s-1] = 2**(aux-1)
                flag[s-1] = 1
    R = retro
    cont = contador
    return R, cont
