from bdb import Breakpoint
from collections import defaultdict
from email.policy import default
from statistics import NormalDist
from tkinter.ttk import Progressbar
import ciw
from ciw import trackers
from matplotlib import pyplot as plt
from funcion_generadora_data import generacion_data_replica_n
import random
import numpy as np
import pandas as pd
from optparse import OptionParser
import inspect
import ast

"""
Cargando los pacientes
"""
pacientes = []


class Paciente:
    def __init__(self, id, ruta_id, ruta_num):
        self.id = id
        self.ruta_id = ruta_id
        self.ruta_num = ruta_num
        self.locacion_actual = None
        self.hora_llegada = None
        self.hora_salida = None

    def __repr__(self):
        string = "Paciente num={}, ruta={}".format(self.id, self.ruta_id)
        return(string)


rutas_sin_procesar = pd.read_csv(
    'pacientes_generados_ruta.csv', encoding='UTF-8', sep=',').fillna(0).reset_index()
for index, row in rutas_sin_procesar.iterrows():
    num = ast.literal_eval(row['Num_area'])
    p = Paciente(index, row['Area'], num)
    pacientes.append(p)

"""
Pacientes cargados
"""
"""
Defino función para elegir la ruta de los pacientes
"""


def repeating_route(ind):
    index = int(str(ind)[11:])
    return pacientes[index].ruta_num[:-1]


"""
"""


class Distribution(object):
    """
    A general distribution from which all other distirbutions will inherit.
    """

    def __repr__(self):
        return 'Distribution'

    def sample(self, t=None, ind=None):
        pass

    def _sample(self, t=None, ind=None):
        """
        Performs vaildity checks before sampling.
        """
        s = self.sample(t=t, ind=ind)
        if (isinstance(s, float) or isinstance(s, int)) and s >= 0:
            return s
        else:
            raise ValueError('Invalid time sampled.')

    def __add__(self, dist):
        """
        Add two distributions such that sampling is the sum of the samples.
        """
        return CombinedDistribution(self, dist, add)

    def __sub__(self, dist):
        """
        Subtract two distributions such that sampling is the difference of the samples.
        """
        return CombinedDistribution(self, dist, sub)

    def __mul__(self, dist):
        """
        Multiply two distributions such that sampling is the product of the samples.
        """
        return CombinedDistribution(self, dist, mul)

    def __truediv__(self, dist):
        """
        Divide two distributions such that sampling is the ratio of the samples.
        """
        return CombinedDistribution(self, dist, truediv)


class CustomDistribution(Distribution):
    def __init__(self):
        self.__init__ = super().__init__
        pass

    def sample(self, t=None, ind=None):
        prob = random.random()
        if prob <= 0.79:
            a = False
            while a == False:
                b = random.gammavariate(5.76, 1/0.016)
                if b > 100 and b < 400:
                    a = True

            return b

        elif 0.79 < prob:
            a = False
            while not a:
                b = random.gammavariate(5.76, 1/0.016)
                if b > 100 and b < 400:
                    a = True
            return b


class Simulacion:
    """
    nueva_configuracion = es el pi de variables de decisión
    formato: lista

    transi = es el periodo transiente en horas, por defecto son 30 días = 30*24 horas

    horario = 0 significa que no se considera que se exitende el horario

    tiempo_simulando es el tiempo en que corre la simulación desde que se termina el periodo transiente,
    por defecto son 120 días

    enfriamiento = es el tiempo en que va limpiando la simulación, es necesario para la librería,
    no se considera en la recolección de datos
    """

    base = [3, 5, 5, 12, 8, 14, 10, 12, 2, 2, 2, 2, 1]
    espera_por_nodo = defaultdict(list)
    espera_por_nodo_total = defaultdict(list)
    espera_sim_por_nodo = []

    def __init__(self, nueva_configuracion=np.zeros(13), transi=30*24, horario=0, tiempo_simulando=120*24, enfriamiento=30*24):
        self.nueva_configuracion = nueva_configuracion
        self.transitorio = transi
        self.tiempo_simulando = tiempo_simulando
        self.enfriamiento = enfriamiento
        self.horario = horario
        self.tiempos_espera_simulacion = []
        self.medias_simulacion = []
        self.desviacion_standard = []
        self.ultimasim = None
        self.tiempo_total = self.transitorio + \
            self.tiempo_simulando + self.enfriamiento
        self.N = self.definir_estructura()

    def definir_estructura(self):
        N = ciw .create_network(
            arrival_distributions=[
                ciw.dists.Exponential(rate=(1)),  # Adm
                ciw.dists.NoArrivals(),  # BOXES
                ciw.dists.NoArrivals(),  # salas hosp 1
                ciw.dists.NoArrivals(),  # salas hosp 2
                ciw.dists.NoArrivals(),  # salas hosp 3
                ciw.dists.NoArrivals(),  # salas hosp 4
                ciw.dists.NoArrivals(),  # salas hosp 5
                ciw.dists.NoArrivals(),  # salas hosp 6
                ciw.dists.NoArrivals(),  # opr_urg
                ciw.dists.NoArrivals(),  # opr_urg_lim
                ciw.dists.NoArrivals(),  # opr_ urg_gen
                ciw.dists.NoArrivals(),  # opr_urg_gen2
                ciw.dists.NoArrivals()  # Otros
            ],
            service_distributions=[
                ciw.dists.Gamma(shape=27.34, scale=(1/298.77)),  # Adm
                ciw.dists.Weibull(scale=0.733, shape=1.66),  # Boxes
                ciw.dists.Gamma(shape=0.43, scale=(1/0.0037)),  # salas hosp1
                ciw.dists.Gamma(shape=0.43, scale=(1/0.0037)),  # salas hosp2
                ciw.dists.Gamma(shape=0.43, scale=(1/0.0037)),  # salas hosp3
                ciw.dists.Gamma(shape=0.43, scale=(1/0.0037)),  # salas hosp4
                ciw.dists.Gamma(shape=0.43, scale=(1/0.0037)),  # salas hosp5
                ciw.dists.Gamma(shape=0.43, scale=(1/0.0037)),  # salas hosp6
                # ] opr101_011 ; EXCL
                ciw.dists.Weibull(scale=2.55, shape=4.64),
                ciw.dists.Normal(mean=2.39, sd=0.584),  # opr102_001 ; EXCL
                ciw.dists.Normal(mean=2.48, sd=0.54),  # opr101_033 ; Gral
                ciw.dists.Normal(mean=2.47, sd=0.46),  # opr102_003 ; Gral
                ciw.dists.Deterministic(value=0)  # OTROS ;
            ],

            routing=[repeating_route, ciw.no_routing, ciw.no_routing, ciw.no_routing,
                     ciw.no_routing, ciw.no_routing, ciw.no_routing, ciw.no_routing, ciw.no_routing, ciw.no_routing, ciw.no_routing, ciw.no_routing, ciw.no_routing],
            number_of_servers=[int(x + y)
                               for (x, y) in zip(self.base, self.nueva_configuracion)]

        )
        return N

    def simular(self, rep=10):
        """
        rep es el numero de veces que se hace la simulación
        se recolectan los datos de cada simulación con la configuración dada
        """
        for trial in range(rep):
            ciw.seed(trial)
            Q = ciw.Simulation(self.N,
                               node_class=[ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode,
                                           ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode,
                                           ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode,
                                           ciw.PSNode],
                               tracker=trackers.NodePopulation())
            # Aca se calibra el programa
            tiempo_simulando = self.transitorio + self.tiempo_simulando + self.enfriamiento
            Q.simulate_until_max_time(tiempo_simulando)
            recs = Q.get_all_records()

            # guardo los tiempos de espera del sistema y los guardo por nodo
            waits = []
            for r in recs:
                if (r.arrival_date > self.transitorio and
                        r.arrival_date < self.tiempo_total-self.enfriamiento):
                    waits.append(r.waiting_time)
                    self.espera_por_nodo_total[str(
                        r.node)].append(r.waiting_time)
                    self.espera_por_nodo[str(r.node)].append(r.waiting_time)
            self.espera_sim_por_nodo.append(self.espera_por_nodo)
            self.espera_por_nodo = defaultdict(list)
            # guardo los tiempos de espera del sistema
            self.tiempos_espera_simulacion.append(waits)
            # guardo las medias
            mean_wait = np.mean(waits)
            self.medias_simulacion.append(mean_wait)
            # guardo desviacion
            desviacion_standard = np.std(waits)
            self.desviacion_standard.append(desviacion_standard)
        self.ultimasim = Q

    def cambiar_configuracion(self, nueva_config):
        self.nueva_configuracion = nueva_config
        self.definir_estructura()

    def tem_por_nodo(self):
        datos = defaultdict(dict)
        for nodo in self.espera_por_nodo_total.keys():
            datos[nodo]['media'] = np.mean(self.espera_por_nodo_total[nodo])
            datos[nodo]['sd'] = np.std(self.espera_por_nodo_total[nodo])
        print("Datos tiempo de espera por nodo en el total de las simulaciones")
        for i in range(0, 14):
            print("Nodo {} = ".format(i), datos[str(i)])
        return datos


sim = Simulacion()
sim.simular()
sim.tem_por_nodo()
breakpoint()
