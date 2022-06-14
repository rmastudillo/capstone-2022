import random
from statistics import mean
from turtle import shape
from types import NoneType
import numpy as np
import matplotlib.pyplot as plt
from math import log
# ejemplo

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
        dt.append(round(i,3))
        i += 0.1

    """
    Lamda_plus representa el maximo de la tasa de llegada variable
    m: representa el numero de datos que generaremos, el cual debe ser
       mayor que la cantidad de personas esperadas entre (0,b]
    """
    lamda_plus = 0.254 
    m = round(lamda_plus*b*3) # hacemos un numero que sea mas grande que el valor esperado de pacientes al dia.
    
    u = np.random.uniform(0,1,m)
    t = [round((-1/lamda_plus)*log(i), 3) for i in u]

    p = 0
    s1 = []
    for i in t:
        p += i
        s1.append(p)
        pass

    s2 = [n for n in s1 if n <= b]
    nstar = len(s2)

    w = np.random.uniform(0,1,size = nstar)

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

def t_div101603():
    p = round(np.random.uniform(low= 48.27, high=483.05), 4)
    return p

def t_div101604():
    p = round(np.random.uniform(low= 6.45, high= 420), 4)
    return p

def t_div102203(u_actual=''):
    prob = random.random()
    p = 0
    if prob <= 0.853:
        while p < 1 or p > 51:
            p = round(np.random.gamma(shape = 0.953, scale = 9.75), 4)
            
    else:
        while p < 133 or p > 291:
            p = round(np.random.uniform(low= 133.55, high=  239.90), 4)

    return p

def t_div103107():
    prob = random.random()
    p = 0

    if prob <= 0.364:
        while p < 3.48 or p > 25.2:
            p = round(np.random.gamma(shape = 1.483, scale = 6.374 ), 4)

    else:
        while p < 100 or p > 690:
            p = round(np.random.uniform(low= 117.6833, high = 691.35), 4)

    return p

def t_div103204():
    prob = random.random()
    p = 0

    if prob <= 0.45:
        while p < 0.1 or p > 24:
            p = round(np.random.gamma(shape = 1.096, scale = 9.04 ), 4)
            
    elif prob > 0.45 and prob <= 0.63:
        while p <= 24 or p >= 47.37:
            p = round(np.random.uniform(low= 24.3, high=  47.37), 4)

    else:
        while p < 48 or p >= 400:
            p = round(random.weibullvariate(alpha = 172.61, beta = 2.071))

    return p

def t_div104602():
    prob = random.random()
    p = 0

    if prob <= 0.4:
        while p <0.6 or p >51:
            p = round(np.random.uniform(low= 0.6, high=  50.8), 4)

    else:
        while p < 90 or p > 572:
            p = round(random.weibullvariate(alpha = 360.9318, beta = 2.1249))

    return p

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



    breakpoint()