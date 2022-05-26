from bdb import Breakpoint
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
    index = int(str(ind)[-1])
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


N = ciw .create_network(

    arrival_distributions=[
        ciw.dists.Exponential(rate=(0.341)),  # Adm
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
        ciw.dists.Weibull(scale=2.55, shape=4.64),  # ] opr101_011 ; EXCL
        ciw.dists.Normal(mean=2.39, sd=0.584),  # opr102_001 ; EXCL
        ciw.dists.Normal(mean=2.48, sd=0.54),  # opr101_033 ; Gral
        ciw.dists.Normal(mean=2.47, sd=0.46),  # opr102_003 ; Gral
        ciw.dists.Deterministic(value=1)  # OTROS ;
    ],

    routing=[repeating_route, ciw.no_routing, ciw.no_routing, ciw.no_routing,
             ciw.no_routing, ciw.no_routing, ciw.no_routing, ciw.no_routing, ciw.no_routing, ciw.no_routing, ciw.no_routing, ciw.no_routing, ciw.no_routing],
    number_of_servers=[3, 5, 5, 12, 8, 14, 10, 12, 2, 2, 2, 2, 1]
)

warmtime = 500
for trial in range(100):
    ciw.seed(trial)
    Q = ciw.Simulation(N, node_class=[ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode,
                       ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode], tracker=trackers.NodePopulation())
    # Aca se calibra el programa
    Q.simulate_until_max_time(168*8 + warmtime)
    recs = Q.get_all_records()
