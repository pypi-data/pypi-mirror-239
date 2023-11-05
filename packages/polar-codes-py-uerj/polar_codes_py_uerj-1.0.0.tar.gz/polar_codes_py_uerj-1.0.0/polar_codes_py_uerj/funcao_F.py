from polar_codes_py_uerj.logF import logF


def funcao_F(la, lb):
    F = logF(la + lb, 0) - logF(la, lb)
    return F
