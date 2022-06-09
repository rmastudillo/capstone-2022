from bdb import Breakpoint
from collections import defaultdict
from email.policy import default
from msilib import sequence
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
import os
from media_movil import media_movil_ayudantia

my_path = os.path.abspath(os.path.dirname(__file__))

"""
Cargando los pacientes
"""
pacientes = []

tiempos_de_llegada = []


class Paciente:
    def __init__(self, id, ruta_id, ruta_num, ruta_time):
        self.id = id
        self.ruta_id = ruta_id
        self.ruta_num = ruta_num
        self.hora_llegada = None
        self.tiempo_atencion = ruta_time

    def __repr__(self):
        string = "Paciente num={}, ruta={}".format(self.id, self.ruta_id)
        return(string)


rutas_sin_procesar = pd.read_csv(
    my_path+'/pacientes_generados_ruta.csv', encoding='UTF-8', sep=',').fillna(0).reset_index()

for index, row in rutas_sin_procesar.iterrows():
    num = ast.literal_eval(row['Num_area'])
    n_time = ast.literal_eval(row['Tiempo_atencion'])
    p = Paciente(index, row['Area'], num, n_time)
    if not p.hora_llegada:
        p.hora_llegada = row['Tiempo_llegada']
        tiempos_de_llegada.append(row['Tiempo_llegada'])
    pacientes.append(p)


"""
Pacientes cargados
"""
"""
Defino función para elegir la ruta de los pacientes
"""


def define_route(ind):
    index = int(str(ind)[11:]) - 1
    print(pacientes[index].ruta_num[:-1])
    return pacientes[index].ruta_num[:-1]


class Service_times(ciw.dists.Distribution):
    def __init__(self):
        self.nodo = defaultdict(int)

    def sample(self, t=None, ind=None):
        # Esto es porque la simulacion parte con ind=1
        index = int(str(ind)[11:]) - 1
        tiempo = pacientes[index].tiempo_atencion[self.nodo[index]]
        self.nodo[index] += 1
        return tiempo


class Arrival_time(ciw.dists.Distribution):
    def __init__(self):
        self.ind = 0

    def sample(self, t=None, ind=None):
        index = self.ind
        self.ind += 1
        tiempo = pacientes[index].hora_llegada
        return round(tiempo, 4)


"""
"""


class Simulacion:
    """
    set up:

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

    """
    Datos:
    """
    """
    1)Sistema completo:
    """
    """
        - Todos los nodos juntos cada trial:
        historial_sistema es una lista con diccionarios que guarda
        media y distribucion calculada de todo el sistema
    """
    historial_sistema = []
    """
        - Todos los nodos juntos cada simulacion:
        historial_simulacion es una lista con diccionarios que guarda
        media y distribucion calculada de todo el sistema conjunto en las 
        n trials
        
    """
    historial_simulacion = []

    """
    2)Sistema parcial por nodo:
    """
    """
        - Todos los nodos separados en cada trial:
        historial_sistema es una lista con diccionarios que guarda
        media y distribucion calculada de todo el sistema
        historial_sistema_nodos[num_simulacion][num_trial][nodo]
        num_simulacion(int)
        num_trial(int)
        nodo(str(int))
    """
    historial_sistema_nodos = []
    """
        - Todos los nodos separados cada simulacion:
        historial_simulacion es una lista con diccionarios que guarda
        media y distribucion de cada nodo en todo el sistema conjunto en las 
        n trials
        historial_simulacion_nodos[num_simulacion][nodo]
        num_simulacion(int)
        nodo(str(int))
    """
    historial_simulacion_nodos = []

    """
    Transitorios 
    """
    espera_sim_por_nodo = defaultdict(lambda: defaultdict(list))

    espera_por_nodo = defaultdict(list)

    Y_bar_i = np.array
    _arrive_time = 0

    def __init__(self, nueva_configuracion=np.zeros(13), transi=24*30*12, horario=0, tiempo_simulando=24*30*24, enfriamiento=24*30*8):
        self.nueva_configuracion = nueva_configuracion
        self.transitorio = transi
        self.tiempo_simulando = tiempo_simulando
        self.enfriamiento = enfriamiento
        self.horario = horario
        self.tiempos_espera_simulacion = []
        # Datos estadisticos
        # Lista con la media del sistema
        self.media_simulacion = int
        # Lista con la desviacion del sistema
        self.desviacion_standard = int
        self.ultimasim = None
        self.tiempo_total = self.transitorio + \
            self.tiempo_simulando + self.enfriamiento
        self.N = self.definir_estructura(self.nueva_configuracion)
        self.paciente = 0

    def definir_estructura(self, nueva_config):
        N = ciw .create_network(
            arrival_distributions=[
                Arrival_time(),  # Adm
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
                ciw.dists.NoArrivals()   # Otros
            ],
            service_distributions=[
                Service_times(),  # Adm
                Service_times(),  # Boxes
                Service_times(),  # salas hosp1
                Service_times(),  # salas hosp2
                Service_times(),  # salas hosp3
                Service_times(),  # salas hosp4
                Service_times(),  # salas hosp5
                Service_times(),  # salas hosp6
                Service_times(),  # opr101_011 ; EXCL
                Service_times(),  # opr102_001 ; EXCL
                Service_times(),  # opr101_033 ; Gral
                Service_times(),  # opr102_003 ; Gral
                Service_times()   # OTROS ;
            ],

            routing=[define_route, ciw.no_routing, ciw.no_routing, ciw.no_routing,
                     ciw.no_routing, ciw.no_routing, ciw.no_routing, ciw.no_routing,
                     ciw.no_routing, ciw.no_routing, ciw.no_routing, ciw.no_routing,
                     ciw.no_routing],
            number_of_servers=[int(x + y)
                               for (x, y) in zip(self.base, nueva_config)]

        )
        return N

    def transciente(self):
        """
        Grafica el tiempo transciente 
        """
        Y_i_j = []
        total_replica = 34
        dias_sim = 700  # dias
        t = 24
        tiempo_simulando = t
        for _replica in range(0, total_replica):
            ciw.seed(_replica)
            Q = ciw.Simulation(self.N,
                               node_class=[ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode,
                                           ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode,
                                           ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode,
                                           ciw.PSNode],
                               tracker=trackers.NodePopulation())
            Y_i = []
            for _i in range(1, dias_sim):
                Q.simulate_until_max_time(tiempo_simulando)  # simula i dias
                waits = []
                recs = Q.get_all_records()
                for r in recs:
                    if r.node != 14:
                        waits.append(r.waiting_time)
                    else:
                        print("ACAA")
                # mi f(y) es el tiempo medio
                Y_i.append(round(np.mean(waits), 3))
                tiempo_simulando += t  # simulo otro día
            tiempo_simulando = t
            Y_i_j.append(Y_i)
        Y_i_j = np.array(Y_i_j)
        Y_bar_i = Y_i_j.mean(0)
        self.Y_bar_i = np.around(Y_bar_i, decimals=3)
        plt.plot(media_movil_ayudantia(self.Y_bar_i, 3))
        plt.ylabel('some numbers')
        plt.show()

    def simular(self, rep=1):
        """
        rep es el numero de veces que se hace la simulación
        se recolectan los datos de cada simulación con la configuración dada
        """
        datos_tiempo = []
        datos_trial = []
        for trial in range(rep):
            ciw.seed(trial)
            Q = ciw.Simulation(self.N,
                               node_class=[ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode,
                                           ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode,
                                           ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode,
                                           ciw.PSNode],
                               tracker=trackers.NodePopulation())
            # Aca se calibra el programa

            Q.simulate_until_max_time(20)
            Q.simulate_until_max_time(40)
            recs = Q.get_all_records()
            # guardo los tiempos de espera del sistema y los guardo por nodo
            comienza_enfriamiento = self.tiempo_total-self.enfriamiento
            waits = []
            for r in recs:
                if r.node != 14 or r.node != 13 and (r.arrival_date > self.transitorio and r.arrival_date < comienza_enfriamiento):
                    datos_tiempo.append(r.waiting_time)
                    self.espera_por_nodo[str(
                        r.node)].append(r.waiting_time)
                    self.espera_sim_por_nodo[str(trial)][str(
                        r.node)].append(r.waiting_time)
                    waits.append(r.waiting_time)

            stadisticas = {"media": np.mean(waits),
                           "sd": np.std(waits)}
            datos_trial.append(stadisticas)

            """
            Reinicio la info de los pacientes
            """
            for index, row in rutas_sin_procesar.iterrows():
                n_time = ast.literal_eval(row['Tiempo_atencion'])
                if index < len(pacientes):
                    pacientes[index].tiempo_atencion = n_time

        """
        1) a)
        """
        self.historial_sistema.append(datos_trial)
        """
        1) b)
        """
        estadisticas_total = {"media": np.mean(
            datos_tiempo), "sd": np.std(datos_tiempo)}

        self.historial_simulacion.append(estadisticas_total)

        """
        2) a)
        """
        self.historial_simulacion_nodos.append(
            self.tem_por_nodo(self.espera_por_nodo))

        """
        2) b)
        """
        lista_datos_trial = []
        for i in range(0, rep):
            lista_datos_trial.append(self.tem_por_nodo(
                self.espera_sim_por_nodo[str(i)]))
        self.historial_sistema_nodos.append(lista_datos_trial)

        """
        Registro media y desviacion para accede mas rapido
        """
        self.media_simulacion = np.mean(
            datos_tiempo)
        self.desviacion_standard = np.std(datos_tiempo)
        """
        Guardo la ultima trial para revisar a mano
        """
        self.ultimasim = Q

    def cambiar_configuracion(self, nueva_config):
        self.nueva_configuracion = nueva_config
        self.definir_estructura()
        self.reiniciar_registros()

    def tem_por_nodo(self, espera_nodo=espera_por_nodo):
        datos = defaultdict(dict)
        for nodo in espera_nodo.keys():
            datos[nodo]['media'] = round(
                np.mean(espera_nodo[nodo]), 4)
            datos[nodo]['sd'] = round(
                np.std(espera_nodo[nodo]), 4)
        #print("Datos tiempo de espera por nodo en el total de las simulaciones")
        # for i in range(1, 14):
        #    print("Nodo {} = ".format(i), datos[str(i)])
        return datos

    def print_datos_nodos(self, dict_nodos):
        print(
            "Datos tiempo de espera por nodo en el total de los trials en las simulaciones")
        for i in range(1, 14):
            print("Nodo {} = ".format(i), dict_nodos[str(i)])

    def reiniciar_registros(self):
        self.espera_sim_por_nodo = defaultdict(lambda: defaultdict(list))
        self.espera_por_nodo = defaultdict(list)

        self.desviacion_standard = 0
        self.medias_simulacion = 0


sim = Simulacion()
# sim.transciente()
sim.simular()
recs = sim.ultimasim.get_all_records()
arrival = [[r.arrival_date, r.id_number] for r in recs if r.node == 1]
arrival_1 = [[r.service_time, r.id_number] for r in recs if r.node == 1]
print(arrival)
print(arrival_1)
# sim.tem_por_nodo()
breakpoint()
