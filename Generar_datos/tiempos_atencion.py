import random
from statistics import mean
from turtle import shape
from types import NoneType
import numpy as np
import matplotlib.pyplot as plt
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
        a = np.random.gamma(shape = 1.33548, scale = 18.86)
        while a > float(72) or a < 0.1:
            a = np.random.gamma(shape = 1.33548, scale = 18.86)
            
        return a

    else:
        a = np.random.normal(loc = 179.259, scale = 45.22 )
        while a < float(72) or a > 290:
            a = np.random.normal(loc = 179.259, scale = 45.22 )
        
        return a

def dist_desde_opr_033():
    p = random.random()
    if p <= 0.389:
        a = np.random.normal(loc = 35.96, scale = 21.34)
        while a > 72 or a <= 0:
            a = np.random.normal(loc = 35.96, scale = 21.34)
        
        return a
    
    else:
        a =  np.random.normal(loc = 178.35, scale = 46.88)
        while a < 72 or a > 290:
            a =  np.random.normal(loc = 178.35, scale = 46.88)

        return a

def dist_desde_opr102_003():
    p = random.random()
    if p <= 0.9:
        a = np.random.gamma(shape = 0.797, scale = 14.038)
        while a > 24 or a <= 0:
            a = np.random.gamma(shape = 0.797, scale = 14.038)

        return a
    
    else:
        a = np.random.normal(loc = 167.61, scale = 30)
        while a < 24 or a > 210:
            a = np.random.normal(loc = 167.61, scale = 30)
        return a

def dist_desde_div103_204():
    a = 0
    while a <= 0.05 or a  >= 500: #min y max de los datos 
        a = np.random.lognormal(mean = 4.992, sigma = 0.819)
    
    return a 

def dist_desde_div101_703():
    p = random.random()
    if p <= 0.24: #prop de gente q se queda menos de 9 hrs
        a = 0
        while a < 0.4 or a >= 9:
            a = np.random.lognormal(mean = 0.8061370, sigma = 0.6801976)
        return a

    elif p > 0.24 and p <= 0.532:
        a = 0
        while a < 9 or a >= 34.13:
            a = np.random.gamma(shape = 10.8779044, scale = 1.66477)
        return a
    
    else:
        a = 0
        while a < 36.62 or a >= 720.0:
            a = np.random.lognormal(mean = 4.92, sigma = 0.94)
            return a

def dist_desde_otros_prom():
    a = 0
    while a < 0.1 or a > 3.5:
        a = np.random.normal(loc = 2.64, scale = 1.8)
    return a


def func_pers_tpos_hosp(u_actual= ""):

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

def t_llegada_entre_pacientes(tpo_actual_aux):

    tpo_actual_aux = 0
    
    return np.random.exponential(0.3845)
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
    # if tpo_actual_aux % 24 < 7.0:  # Hora valle
    #     # parametro para horario entre 00 y 6:59, calculado con ventana de 16 horas
    #     return np.random.exponential(7.31)

    # else:
    #     # parametro para horario entre 7 y 23:59
    #     return np.random.exponential(3.935)




def t_urg101003():
    # --> scale = 1/rate.
    return np.random.gamma(shape=27.33998, scale=0.003347065)


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






# tiempo = 0
# tpos = []
# for i in range(24*30):
#     tpos.append(tiempo)
#     tiempo2 = round(t_llegada_entre_pacientes(tiempo), 4)
#     tiempo += tiempo2
# l = []
# for i in range(len(tpos)-1):

#     j = i+1
#     k = j-1

#     t1 = tpos[j]
#     t0 = tpos[k]

#     l.append(t1-t0)


