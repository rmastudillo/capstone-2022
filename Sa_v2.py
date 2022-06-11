from distutils.command.config import config
import numpy as np
import random as random
import itertools as iter
import csv
import os
from main import *

my_path = os.path.abspath(os.path.dirname(__file__))
factibless = []
"""

with open(my_path+"/data_fact.csv", "r") as read_obj:
    csv_reader = csv.reader(read_obj)
    list_csv_1 = tuple(csv_reader)
    factibless += list_csv_1
with open(my_path+"/data_fact_2.csv", "r") as read_obj2:
    csv_reader2 = csv.reader(read_obj2)
    list_csv_2 = tuple(csv_reader2)
    factibless += list_csv_2
with open(my_path+"/data_fact_3.csv", "r") as read_obj3:
    csv_reader3 = csv.reader(read_obj3)
    list_csv_3 = tuple(csv_reader3)
    factibless += list_csv_3
with open(my_path+"/data_fact_4.csv", "r") as read_obj4:
    csv_reader4 = csv.reader(read_obj4)
    list_csv_4 = tuple(csv_reader4)
    factibless += list_csv_4
"""


def factos(conf, fact):
    conf = tuple(conf)
    print(conf)
    print(len(fact), len(fact[0]))
    breakpoint()
    for i in range(len(fact)):
        print(i)
        print(fact[i])
        if conf in fact[i]:
            return True
    return False


def factibilidad(configuracion):
    Pr_24 = [25000, 800]
    Pr_Box = [12500, 450]
    Pr_Vent = [0, 150]
    Pr_Cama = [3500, 250]
    Presup_Op = 4500
    Presup_Ca = 50000
    lst = list(map(list, iter.product([0, 1], repeat=22)))
    lst_costCAP = [Pr_Vent[0], Pr_Vent[0], Pr_Box[0], Pr_Box[0], Pr_Box[0], Pr_Cama[0], Pr_Cama[0], Pr_Cama[0], Pr_Cama[0], Pr_Cama[0],
                   Pr_Cama[0], Pr_Cama[0], Pr_Cama[0], Pr_Cama[0], Pr_Cama[0], Pr_Cama[0], Pr_Cama[0], Pr_Cama[0], Pr_Cama[0], Pr_Cama[0], Pr_Cama[0], Pr_24[0]]
    lst_costOP = [Pr_Vent[1], Pr_Vent[1], Pr_Box[1], Pr_Box[1], Pr_Box[1], Pr_Cama[1], Pr_Cama[1], Pr_Cama[1], Pr_Cama[1], Pr_Cama[1], Pr_Cama[1],
                  Pr_Cama[1], Pr_Cama[1], Pr_Cama[1], Pr_Cama[1], Pr_Cama[1], Pr_Cama[1], Pr_Cama[1], Pr_Cama[1], Pr_Cama[1], Pr_Cama[1], Pr_24[1]]
    for i in range(len(lst)):
        a = np.dot(lst[i], lst_costCAP, out=None)
        b = np.dot(lst[i], lst_costOP, out=None)
        if a <= Presup_Ca and b <= Presup_Op:
            return True
    else:
        return False


def generar_vecino(configuration):
    n = len(configuration)
    fact = False
    while not fact:
        casilla = random.randint(0, n-1)
        vecino_sa = np.copy(configuration)
        if vecino_sa[casilla] == 0:
            vecino_sa[casilla] = 1
        else:
            vecino_sa[casilla] = 0
        # corroborar si lo haremos así o no
        fact = factibilidad(vecino_sa)
    vecino_sim = [vecino_sa[0]+vecino_sa[1], vecino_sa[2] + vecino_sa[3] + vecino_sa[4], vecino_sa[5] + vecino_sa[6] + vecino_sa[7], vecino_sa[8], vecino_sa[9] + vecino_sa[10] +
                  vecino_sa[11], vecino_sa[12] + vecino_sa[13], vecino_sa[14] + vecino_sa[15] + vecino_sa[16] + vecino_sa[17], vecino_sa[18] + vecino_sa[19] + vecino_sa[20], vecino_sa[21]]
    return vecino_sa, vecino_sim


def simulacion(configuracion, escenarios, sim=Simulacion, n_sim=0):
    resultado = []
    configuracion = configuracion[:-1] + [0, 0, 0, 0, 0]
    sim.simular(nueva_configuracion=configuracion, rep=escenarios)
    for i in range(len(sim.historial_replicas[n_sim])):
        resultado.append(float(sim.historial_replicas[n_sim][i]["media"]))
    return resultado


def SA(NITER=10, Tk=1000, configuracion_inicial=[0, 0, 0, 0, 0, 0, 0, 0, 0], alpha=0.99, beta=0.5, sim=Simulacion):

    accept = 0

    configuracion = [0, 0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    print(len(configuracion))
    # lista de largo cantidad de réplicas
    valor_actual = simulacion(configuracion_inicial, 3, sim)

    configuracion_ideal = [2, 3, 3, 1, 3, 2, 4, 3, 1]
    valor_ideal = simulacion(configuracion_ideal, 3, sim, n_sim=1)
    best_configuracion = np.copy(configuracion)
    best_valor = valor_actual
    iteracion = 0
    """
    Reinicio la simulacion
    """
    sim = Simulacion()

    """
    Numero de replicas
    """
    n_replicas = 2
    replicas_adicionales = 2

    breakpoint()

    """
    Comienza SA
    """
    for i in range(NITER):
        valor_old = valor_actual
        # es de esa o de best_configuracion ????

        vecino = generar_vecino(configuracion)
        vecino_sa = vecino[0]
        vecino_sim = vecino[1]
        valor_vecino = simulacion(vecino_sim, n_replicas, sim, n_sim=i)
        mu = np.mean(list(map(lambda x, y: x-y, valor_vecino, valor_old)))
        # quizas hay que cambiar ddof a 1
        s = np.std(list(map(lambda x, y: x-y, valor_vecino, valor_old)), ddof=1)
        # cantidad de réplicas, el largo de la lista
        ancho = 1.96*s/np.sqrt(len(valor_vecino))
        intervalo = [mu - ancho, mu + ancho]

        if intervalo[1] < 0:
            configuracion = vecino_sa
            valor_actual = valor_vecino
            accept = 1
            probT = 1
            if valor_actual < best_valor:
                best_configuracion = np.copy(configuracion)
                best_valor = valor_actual
                iteracion = i+1
        elif intervalo[0] > 0:
            probT = np.exp(-mu/(beta*Tk))
            if probT >= np.random.uniform(0, 1):
                configuracion = np.copy(vecino_sa)
                valor_actual = valor_vecino
                accept = 1
            else:
                accept = 0

        else:
            # fijar cuantas réplicas más y como la simulaciñon elige las extras distintas

            replicas_actual = n_replicas
            while intervalo[0] < 0 and intervalo[1] > 0:

                valor_vecino_ext = simulacion(vecino_sim, replicas_actual, sim)
                # ver cúantas replicas extras y cómo se lo pedimos a la simulacion
                valor_actual_ext = simulacion(
                    configuracion, replicas_actual, sim)
                valor_vecino = valor_vecino + valor_vecino_ext
                valor_actual = valor_actual + valor_actual_ext
                mu = np.mean(
                    list(map(lambda x, y: x-y, valor_vecino, valor_actual)))
                # quizas hay que cambiar ddof a 1
                s = np.std(
                    list(map(lambda x, y: x-y, valor_vecino, valor_actual)), ddof=1)
                # cantidad de réplicas, el largo de la lista
                ancho = 1.64*s/np.sqrt(len(valor_vecino))
                intervalo = [mu - ancho, mu + ancho]
                if intervalo[1] < 0:
                    configuracion = vecino_sa
                    valor_actual = valor_vecino
                    accept = 1
                    probT = 1
                    if valor_actual < best_valor:
                        best_configuracion = np.copy(configuracion)
                        best_valor = valor_actual
                        iteracion = i+1
                elif intervalo[0] > 0:
                    probT = np.exp(-mu/(beta*Tk))
                    if probT >= np.random.uniform(0, 1):
                        configuracion = np.copy(vecino_sa)
                        valor_actual = valor_vecino
                        accept = 1
                    else:
                        accept = 0
                else:
                    replicas_actual += replicas_adicionales

        # if np.mean(best_valor) <= 1.2 * np.mean(valor_ideal):  # tenemos que ver dd va
        #    break
        Tk = alpha*Tk
    media_best = np.mean(best_valor)
    return best_valor, best_configuracion, media_best


h = generar_vecino([0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                   0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

print(h[0])
print(h[1])
sim = Simulacion()
sa = SA(sim=sim)
breakpoint()
