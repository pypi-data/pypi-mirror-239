import numpy as np


def fbitreversed(j, n):
    i = np.zeros(len(j), dtype=int)

    if n == 0:
        n = 1

    for indx in range(len(j)):
        x = format(j[indx], f'0{n}b')
        y = x[::-1]
        i[indx] = int(y, 2) + 1

    return i
