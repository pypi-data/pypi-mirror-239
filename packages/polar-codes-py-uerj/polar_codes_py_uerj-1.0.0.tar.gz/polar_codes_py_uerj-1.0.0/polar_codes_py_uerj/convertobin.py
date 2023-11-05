import numpy as np


def convertobin(sbin):
    bin = np.zeros(len(sbin), dtype=int)
    for i in range(len(sbin)):
        if sbin[i] == '0':
            bin[i] = 0
        else:
            bin[i] = 1
    return bin
