import random
from statistics import mean
from turtle import shape
from types import NoneType
import numpy as np
import matplotlib.pyplot as plt
from math import log
# ejemplo


def dist_promedio():
    """
    Comportamiento promedio de paciente que sale de una opr. Lo modelamos asi
    por la falta de datos (que quedan en 0 por el end...), lo cual nos llevaria a sub estimar los tiempos.
    Se modela segmentando la permanencia de los pacientes en: 
        1) menos de 72 hrs (3 dias), lo cual ocurre el 51% de las veces
        2) mas de 72 hrs, lo cual representa el resto de posibilidades (entre 72 y 290 hrs)
    """
    p = random.random()
    if p <= 0.51:
        a = np.random.gamma(shape=1.33548, scale=18.86)
        while a > float(72) or a < 0.1:
            a = np.random.gamma(shape=1.33548, scale=18.86)

        return a

    else:
        a = np.random.normal(loc=179.259, scale=45.22)
        while a < float(72) or a > 290:
            a = np.random.normal(loc=179.259, scale=45.22)

        return a


def dist_desde_opr_033():
    p = random.random()
    if p <= 0.389:
        a = np.random.normal(loc=35.96, scale=21.34)
        while a > 72 or a <= 1.1:
            a = np.random.normal(loc=35.96, scale=21.34)

        return a

    else:
        a = np.random.normal(loc=178.35, scale=46.88)
        while a < 93 or a > 290:  # Sacando el min y max del intervalo
            a = np.random.normal(loc=178.35, scale=46.88)

        return a


def dist_desde_opr102_003():
    p = random.random()
    if p <= 0.9:
        a = np.random.gamma(shape=0.797, scale=14.038)
        while a > 24 or a <= 0.05:
            a = np.random.gamma(shape=0.797, scale=14.038)

        return a

    else:
        a = np.random.normal(loc=167.61, scale=30)
        while a < 24 or a > 210:
            a = np.random.normal(loc=167.61, scale=30)
        return a


def dist_desde_div103_204():
    p = random.random()
    a = 0
    if p <= 0.29:
        while a <= 0.05 or a >= 24:  # min y max de los datos
            a = np.random.normal(loc=11.675, scale=6.44)
    else:
        while a <= 90.5 or a >= 547:  # min y max de los datos
            a = np.random.normal(loc=11.675, scale=6.44)
        return a


def dist_desde_div101_703():
    p = random.random()
    if p <= 0.24:  # prop de gente q se queda menos de 9 hrs
        a = 0
        while a < 0.4 or a >= 9:
            a = np.random.lognormal(mean=0.8061370, sigma=0.6801976)
        return a

    elif p > 0.24 and p <= 0.49:
        a = 0
        while a < 9 or a >= 23.55:
            a = np.random.gamma(shape=16.5012, scale=0.994)
        return a

    else:
        a = 0
        while a < 24 or a >= 720.0:
            a = np.random.lognormal(mean=4.79, sigma=1.0312)
            return a


def dist_desde_otros_prom():
    a = 0
    while a < 0.1 or a > 3.5:
        a = np.random.normal(loc=2.64, scale=1.8)
    return a


def func_pers_tpos_hosp(u_actual=""):

    if u_actual == "OPR102_001":
        a = dist_promedio()
        return a

    elif u_actual == 'OPR101_033':
        a = dist_desde_opr_033()

        return a

    elif u_actual == "OPR102_003":
        a = dist_desde_opr102_003()

        return a

    elif u_actual == "OPR101_011":
        """
        Dado que solo cuenta con 2 datos, asumimos que tendra distribucion promedio
        """
        a = dist_promedio()

        return a

    elif u_actual == 'DIV101_703':
        a = dist_desde_div101_703()

        return a

    elif u_actual == 'DIV103_204':
        """
        Dado que tiene solo 7 datos, modelamos asi:
        """
        a = dist_desde_div103_204()

        return a

    else:
        a = dist_desde_otros_prom()
        return a


def lista_t_entre_llegadas(tiempo_simulacion):
    """ 
    b: el intervalo de tiempo que se simulara, (0, b]
    """

    b = tiempo_simulacion

    def tasa_no_homo(t):
        hora = t % 24
        if hora >= 0 and hora <= 7:
            return 0.13677

        elif hora > 7 and hora <= 12:
            r = 0.02346*hora - 0.02752
            return r

        elif hora > 12 and hora <= 21.5:
            return 0.254

        else:
            r = -0.046892*hora + 1.2621
            return r

    """
    Parte Homogenea:
    1) crear los intervalos y los visualizamos
    """

    i = 0
    y = []
    dt = []

    while i <= b:
        pto = tasa_no_homo(i)
        y.append(pto)
        dt.append(round(i, 3))
        i += 0.1

    """
    Lamda_plus representa el maximo de la tasa de llegada variable
    m: representa el numero de datos que generaremos, el cual debe ser
       mayor que la cantidad de personas esperadas entre (0,b]
    """
    lamda_plus = 0.254
    # hacemos un numero que sea mas grande que el valor esperado de pacientes al dia.
    m = round(lamda_plus*b*3)

    u = np.random.uniform(0, 1, m)
    t = [round((-1/lamda_plus)*log(i), 3) for i in u]

    p = 0
    s1 = []
    for i in t:
        p += i
        s1.append(p)
        pass

    s2 = [n for n in s1 if n <= b]
    nstar = len(s2)

    w = np.random.uniform(0, 1, size=nstar)

    lol = []
    t_entre_llegadas = []
    for i in range(len(w)):
        lam = s2[i]
        lam1 = tasa_no_homo(lam)/lamda_plus
        k = w[i]
        # print('lam', lam1)
        # print('k', k)

        bul = (k <= lam1)
        lol.append(bul)
        if bul:
            t_entre_llegadas.append(t[i])

    ind = [i*1 for i in lol]

    x = sum(ind)
    Nt1 = [i for i in range(x)]

    j = [i for i in range(len(ind)) if ind[i] == 1]

    horas_llegada_pacientes = [s2[i] for i in j]

    eje_y = [0] + Nt1 + [max(Nt1)]
    eje_x = [0] + horas_llegada_pacientes + [b]
    plt.step(eje_x, eje_y)

    # plt.hist(t_entre_llegadas)
    # plt.show()

    return t_entre_llegadas


def t_urg101003():
    # --> scale = 1/rate.
    return np.random.gamma(shape=28.1626, scale=0.0032)


def t_div101703():
    return np.random.gamma(shape=2.289, scale=0.2999213)


""" 
    opr: esta variable indica si el paciente proviene de opr
    Para esta sala de hosp, la probabilidad de que el paciente provenga de una opr es 0. por lo que
    opr siempre sera False
    
"""


def t_div101603(u_actual=''):
    return func_pers_tpos_hosp(u_actual)


def t_div101604(u_actual=''):

    return func_pers_tpos_hosp(u_actual)


def t_div102203(u_actual=''):
    return func_pers_tpos_hosp(u_actual)


def t_div103107(u_actual=''):
    return func_pers_tpos_hosp(u_actual)


def t_div104602(u_actual=''):
    return func_pers_tpos_hosp(u_actual)


def t_div103204(u_actual=''):
    return func_pers_tpos_hosp(u_actual)


def t_opr102001():
    return random.weibullvariate(2.618, 4.572)


def t_opr101011():
    return random.weibullvariate(alpha=2.546, beta=4.644)


def t_opr102003():
    return random.weibullvariate(2.678, 5.733)


def t_opr101033():
    return random.weibullvariate(2.67, 5.37)


def t_otro():
    return 0


def t_end():
    return 0


def random_gama():
    return np.random.gamma(shape=25.155, scale=4.542125)
