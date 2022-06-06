import random
from turtle import shape
import numpy as np
# ejemplo


def t_llegada_entre_pacientes(tpo_actual_aux):
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
    """Ahora, recibe tpo_actual_aux, el cual en base al tiempo actual de llegada """
    if tpo_actual_aux % 24 < 7.0:  # Hora valle
        # parametro para horario entre 00 y 6:59, calculado con ventana de 16 horas
        return round(np.random.exponential(7.3112745), 4)

    else:
        # parametro para horario entre 7 y 23:59
        return round(np.random.exponential(3.93550), 4)


def t_urg101003():
    # --> scale = 1/rate.
    return round(np.random.gamma(shape=27.33998, scale=0.003347065), 4)


def t_div101703():
    return round(np.random.gamma(shape=2.289, scale=0.2999213), 4)


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
    return round(random.weibullvariate(2.618, 4.572), 3)


def t_opr101011():
    return round(random.weibullvariate(alpha=2.546, beta=4.644), 3)


def t_opr102003():
    return round(random.weibullvariate(2.678, 5.733), 3)


def t_opr101033():
    return round(random.weibullvariate(2.67, 5.37), 3)


def t_otro():
    return 0


def t_end():
    return 0


def random_gama():
    return np.random.gamma(shape=25.155, scale=4.542125)
