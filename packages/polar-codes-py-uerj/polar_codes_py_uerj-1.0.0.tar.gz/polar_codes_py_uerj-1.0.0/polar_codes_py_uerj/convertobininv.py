import numpy as np


def convertobininv(sbin):
    aux = len(sbin)
    bin2 = np.zeros(aux, dtype=int)
    for i in range(aux):
        if sbin[i] == '0':
            bin2[aux - i - 1] = 0
        else:
            bin2[aux - i - 1] = 1
    return bin2
