import numpy as np
import matplotlib.pyplot as plt

import math

import matplotlib.pyplot as plt
import time

from polar_codes_py_uerj import codificador
from polar_codes_py_uerj import decodificador

from polar_codes_py_uerj.GeraIndexRETRO import GeraIndexRETRO
from polar_codes_py_uerj.auxCol import auxCol
from polar_codes_py_uerj.fbitreversed import fbitreversed
from polar_codes_py_uerj.MatrizGeradora import MatrizGeradora
from polar_codes_py_uerj.montaMapa import montaMapa
from polar_codes_py_uerj.polarizacao import polarizacao


def run_simulation():
    designSNRdB = 0

    N = 8
    K = 4

    verbose_output_flag = 0

    EbN0dB = np.arange(0, 5, 1)

    Ec = 1
    N0 = 2

    MCsize = 1000

    BER = np.zeros(len(EbN0dB))
    FER = np.zeros(len(EbN0dB))

    Nout = N
    N_example = 8
    N = 2**int(math.ceil(math.log2(N_example)))

    IndexRETRO = GeraIndexRETRO(N)
    aux_col = auxCol(N)
    mapa = montaMapa(N)
    sequencia_W = fbitreversed(np.arange(
        2**int(math.ceil(math.log2(N_example)))), int(math.ceil(math.log2(N_example))))
    P = polarizacao(N, K, designSNRdB).T
    G = MatrizGeradora(N)

    if not verbose_output_flag:
        print(f'Completed SNR points (out of {len(EbN0dB)}): ')
    start_time = time.time()
    for j in range(len(EbN0dB)):
        Ec = (K / N) * N0 * 10 ** (EbN0dB[j] / 10)

        for l in range(MCsize):
            u = np.random.randint(0, 2, K)
            x = codificador(u, P, G, 1)
            txvec = (2 * x - 1) * np.sqrt(Ec)
            y = txvec + np.sqrt(N0 / 2) * np.random.randn(N)

            uhat = decodificador(y, N, Ec, N0, P, IndexRETRO,
                                 G, aux_col, mapa, sequencia_W, 1)

            nfails = np.sum(uhat != u)
            FER[j] += (nfails > 0)
            BER[j] += nfails

        FER[j] /= l + 1
        BER[j] /= (K * (l + 1))

    # Fim da contagem de tempo
    end_time = time.time()
    # Cálculo do tempo decorrido
    elapsed_time = end_time - start_time
    print("Tempo decorrido: ", elapsed_time, " segundos")

    # Imprimindo gráfico
    print('\n')
    titlestr = f'Polar Code (N={Nout}, R={K/Nout:.2f})'
    plt.figure(1, figsize=(12, 5))
    plt.subplot(121)
    plt.semilogy(EbN0dB, BER, '-k')
    plt.title(titlestr)
    plt.xlabel('E_b/N_0 in dB')
    plt.ylabel('Bit Error Rate')
    plt.grid(True)
    plt.subplot(122)
    plt.semilogy(EbN0dB, FER, '-k')
    plt.title(titlestr)
    plt.xlabel('E_b/N_0 in dB')
    plt.ylabel('Frame Error Rate')
    plt.grid(True)
    plt.tight_layout()
    plt.show()
