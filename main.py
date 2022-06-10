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
import os
from media_movil import media_movil_ayudantia

my_path = os.path.abspath(os.path.dirname(__file__))

"""
Cargando los pacientes
"""
pacientes = []



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

"""
rutas_sin_procesar = pd.read_csv(
    my_path+'/pacientes_generados_ruta.csv', encoding='UTF-8', sep=',').fillna(0).reset_index()

for index, row in rutas_sin_procesar.iterrows():
    num = ast.literal_eval(row['Num_area'])
    n_time = ast.literal_eval(row['Tiempo_atencion'])
    p = Paciente(index, row['Area'], num, n_time)
    if not p.hora_llegada:
        p.hora_llegada = row['Tiempo_llegada']
    pacientes.append(p)
"""

"""
Pacientes cargados
"""
"""
Defino función para elegir la ruta de los pacientes
"""


nodo_tiempo = defaultdict(int)


class Service_times(ciw.dists.Distribution):

    def sample(self, t=None, ind=None):
        # Esto es porque la simulacion partqe con ind=1
        index = int(str(ind)[11:]) - 1
        global pacientes
        global nodo_tiempo
        #print(index,"AAA")
        tiempo = pacientes[index].tiempo_atencion[nodo_tiempo[index]]
        nodo_tiempo[index]+= 1
        return tiempo


class Arrival_time(ciw.dists.Distribution):
    def __init__(self):
        self.ind = 0

    def sample(self, t=None, ind=None):
        index = self.ind
        self.ind += 1
        try:
            tiempo = pacientes[index].hora_llegada
        except:
            print("mesalieen ",index)
        return round(tiempo, 4)


"""
Esta funcion es global porque la simulacion molesta mucho
"""
def define_route(ind):
    index = int(str(ind)[11:]) - 1
    return pacientes[index].ruta_num[:-1]
pacientes = []
"""
Comienza la simulacion
"""
class Simulacion:
    """
    set up:

    configuracion = es el pi de variables de decisión
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
    historial_replicas = []
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
    historial_replicas_nodos = []
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

    def __init__(self, transi=24*30*6, horario=0, tiempo_simulando=24*30*24, enfriamiento=0):
        """
        Cargar los pacientes
        """
        self.todos_los_pacientes = [] # aca se van a ir guardando los pacientes
        self.pacientes = None # son los pacientes actuales

        
        self.base_actual = 0
        self.bdd_pacientes_actual = 0 # esto es para recorrer todos los pacientes
        
        """
        Aqui se registra la simulacion actual
        Q contendra todos los registros
        configuracion es la nueva configuracion
        Estos set ups tienen que estar antes de comenzar a simular
        """
        self.N = None
        self.Q = None
        self.configuracion = None
        self.simulacion_actual = -1
        """
        Tiempo de simulacion
        transitorio es el periodo transitorio
        tiempo_simulando es el tiempo que durará la recolección de datos
        ultimopedazo es la cola de los datos, no se considerarán
        """
        self.transitorio = transi
        self.tiempo_simulando = tiempo_simulando
        self.ultimopedazo = tiempo_simulando + transi
        self.tiempo_total = transi + tiempo_simulando + enfriamiento

        """
        Listas para guardar datos
        """
        self.datos_tiempo = []
        self.datos_trial = []


        
        self.horario = horario
        self.tiempos_espera_simulacion = []
        # Datos estadisticos
        # Lista con la media del sistema
        self.mean = int
        # Lista con la desviacion del sistema
        self.sd = int
        self.paciente = 0

    def cargar_pacientes(self,n_bdd):
        p_path = my_path + '/Generar_datos/Pacientes_sim'
        try:
            self.pacientes=self.todos_los_pacientes[n_bdd]
            return self.pacientes
        except:
            rutas_sin_procesar = pd.read_csv(p_path+
                '/pacientes_generados_ruta_{}.csv'.format(n_bdd),
                encoding='UTF-8', sep=',').fillna(0).reset_index()
            pacientes = []
            for index, row in rutas_sin_procesar.iterrows():
                num = ast.literal_eval(row['Num_area'])
                n_time = ast.literal_eval(row['Tiempo_atencion'])
                p = Paciente(index, row['Area'], num, n_time)
                if not p.hora_llegada:
                    p.hora_llegada = row['Tiempo_llegada']
                pacientes.append(p)
            self.pacientes=pacientes
            self.todos_los_pacientes.append(pacientes)
            print(self.pacientes[:3])
            return self.pacientes




    def definir_estructura(self, nueva_config,pacientes):
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



    def crear_simulacion(self,N):
        self.Q = ciw.Simulation(N,
                            node_class=[ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode,
                                        ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode,
                                        ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode,
                                        ciw.PSNode],
                            tracker=trackers.NodePopulation(),exact=5)


    def simular(self,nueva_configuracion=np.zeros(13),ini=0, rep=2):
        """
        Defino la estructura a simular
        """
        

        """
        rep es el numero de veces que se hace la simulación
        se recolectan los datos de cada simulación con la configuración dada
        """
        if not ini:
            self.datos_tiempo = []
            self.datos_trial = []
            self.simulacion_actual+=1
        for trial in range(ini,rep+ini):
            print("COMENCE LA ITERACION {}".format(trial))
            
            """
            Acá cargo los pacientes para no usar tanta ram
            """
            global pacientes
            pacientes = self.cargar_pacientes(trial)
            self.N = self.definir_estructura(nueva_configuracion,pacientes)
            """
            Pacientes cargados
            """
            """
            Aqui se crea la simulación
            Parametro N que es la estructura
            """
            self.crear_simulacion(self.N)

            """
            Se simula hasta tiempo_total
            """
            self.Q.simulate_until_max_time(self.tiempo_total)
            self.base_actual+=1 # ya simule en el archivo trial
            global nodo_tiempo
            nodo_tiempo = defaultdict(int)
            """
            # Comienza el registro de datos, la simulacion actual
            está en self.Q
            """
            
            recs = self.Q.get_all_records()
            waits = []
            for r in recs:
                """
                Filtros
                """

                if not (r.node == 14 or r.node == 13) and (r.arrival_date > self.transitorio and r.arrival_date < self.ultimopedazo):
                    self.datos_tiempo.append(r.waiting_time)
                    self.espera_por_nodo[str(
                        r.node)].append(r.waiting_time)
                    self.espera_sim_por_nodo[str(trial)][str(
                        r.node)].append(r.waiting_time)
                    waits.append(r.waiting_time)

            stadisticas = {"media": np.mean(waits),
                           "sd": np.std(waits)}
            self.datos_trial.append(stadisticas)
            print("TERMINE LA ITERACION")

        """
        1) a)
        """
        if ini == 0:
            self.historial_replicas.append(self.datos_trial)
        """
        1) b)
        """
        estadisticas_total = {"media": np.mean(
            self.datos_tiempo), "sd": np.std(self.datos_tiempo)}
        if ini==0:
            self.historial_simulacion.append(estadisticas_total)
        else:
            self.historial_simulacion[self.simulacion_actual] = estadisticas_total
        """
        2) a)
        """
        self.historial_replicas_nodos.append(
            self.tem_por_nodo(self.espera_por_nodo))

        """
        2) b)
        """
        lista_datos_trial = []
        for i in range(0, rep):
            lista_datos_trial.append(self.tem_por_nodo(
                self.espera_sim_por_nodo[str(i)]))
        if ini == 0:
            self.historial_simulacion_nodos.append(lista_datos_trial)
        else:
            self.historial_simulacion_nodos[self.simulacion_actual]=lista_datos_trial

        """
        Registro media y desviacion para accede mas rapido
        """
        self.mean = np.mean(
            self.datos_tiempo)
        self.sd = np.std(self.datos_tiempo)
        """
        Guardo la ultima trial para revisar a mano
        """

    def cambiar_configuracion(self, nueva_config):
        self.configuracion = nueva_config
        self.definir_estructura()
        self.reiniciar_registros()

    def tem_por_nodo(self, espera_nodo=espera_por_nodo):
        datos = defaultdict(dict)
        for nodo in espera_nodo.keys():
            datos[nodo]['media'] = np.mean(espera_nodo[nodo])
            datos[nodo]['sd'] = np.std(espera_nodo[nodo])
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


sim = Simulacion()
# sim.transciente()


sim.simular(rep=2)
# Una nueva simulacion NO DEBE TENER INI
recs = sim.Q.get_all_records()
# sim.tem_por_nodo()
print(sim.mean,sim.sd)
breakpoint()
