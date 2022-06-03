import numpy as np
# ejemplo


def t_llegada_entre_pacientes():
    """
    Esto retorna cuanto tiempo se demora el siguiente paciente en llega
    no necesita saber el tiempo actual
    ejemplo:
    el primer paciente llega en t=0
    -> se llama t_llegada_entre_pacientes para determinar la llegada del paciente 2
    retorna 1.5 -> entonces llega en t=1.5 (lo calcula la simulacion)
    se llama t_llegada_entre_pacientes para determinar la llegada del paciente 3
    retorna 1.5 -> entonces llega en t=3 (lo calcula la simulacion)
    """
    return 3


def t_urg101003():
    return 0.1


def t_div101703():
    return 0.2


def t_div101603():
    return 0.3


def t_div101604():
    return 0.4


def t_div102203():
    return 0.5


def t_div103107():
    return 0.6


def t_div104602():
    return 0.7


def t_div103204():
    return 0.8


def t_opr102001():
    return 0.9


def t_opr101011():
    return 0.11


def t_opr102003():
    return 0.12


def t_opr101033():
    return 0.13


def t_otro():
    return 20


def t_end():
    return 0


def random_gama():
    return np.random.gamma(shape=25.155, scale=4.542125)
