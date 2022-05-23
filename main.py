from bdb import Breakpoint
from statistics import NormalDist
from tkinter.ttk import Progressbar
import ciw
from ciw import trackers
from matplotlib import pyplot as plt
from funcion_generadora_data import generacion_data_replica_n
import random


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
        ciw.dists.NoArrivals(),  # salas hosp
        ciw.dists.NoArrivals(),  # opr
        ciw.dists.NoArrivals(),  # opr
        ciw.dists.NoArrivals(),  # opr
        ciw.dists.NoArrivals(),  # opr
        ciw.dists.NoArrivals()  # Otros
    ],

    service_distributions=[
        ciw.dists.Gamma(shape=27.34, scale=(1/298.77)),  # Adm
        ciw.dists.Weibull(scale = 0.733, shape = 1.66),#Boxes
        #ciw.dists.Lognormal(-0.541, 0.7205),
        ciw.dists.Gamma(shape=0.43, scale=(1/0.0037)),  # salas hosp

        ciw.dists.Weibull(scale=2.55, shape=4.64),  # opr101_011 ; EXCL
        ciw.dists.Normal(mean=2.39, sd=0.584),  # opr102_001 ; EXCL

        ciw.dists.Normal(mean=2.48, sd=0.54),  # opr101_033 ; Gral
        ciw.dists.Normal(mean=2.47, sd=0.46),  # opr102_003 ; Gral

        ciw.dists.Deterministic(value=80000000000)  # OTROS ;

    ],

    routing=[

        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Adm
        [0.0, 0.0, 0.39, 0.0, 0.001, 0.001, 0.03, 0.35],  # BOXES
        [0.0, 0.0, 0.0325, 0.001, 0.0762, 0.0077, 0.1214, 0.1326],  # salas hosp
        [0.0, 0.0, 0.55, 0.0, 0.0, 0.0, 0.45, 0.0],  # opr101_011 ; EXCL
        [0.0, 0.0, 0.034, 0.95, 0.0, 0.0, 0.0, 0.016],  # opr102_001 ; EXCL
        [0.0, 0.148, 0.563, 0.0, 0.0, 0.0, 0.0, 0.282],  # opr101_033 ; Gral
        [0.0, 0.02, 0.119, 0.0, 0.0, 0.829, 0.0, 0.032],  # opr102_003 ; Gral
        [0.0, 0.002, 0.091, 0.0, 0.044, 0.009, 0.058, 0.5]  # otro
    ],

    number_of_servers=[3, 5, 61, 2, 2, 2, 2, 1]
)

if __name__ == '__main__':
    average_waits = []
    average_service_times = []

# Listas donde guarda data:
# 1) Services time por nodo:
    l_service_times_boxes = []
    l_services_times_admision = []
    l_services_times_hosp = []
    l_services_times_opr101_011 = []
    l_services_times_opr102_001 = []
    l_services_times_opr101_033 = []
    l_services_times_opr102_003 = []

# 2) Largo promedio cola por nodo:
    l_largo_admision = []
    l_largo_boxes = []
    l_largo_hosp = []
    l_largo_opr101_011 = []
    l_largo_opr102_001 = []
    l_largo_opr101_033 = []
    l_largo_opr102_003 = []

# 3) promedio espera por nodo:
    l_tiempo_promedio_espera_admision = []
    l_tiempo_promedio_espera_boxes = []
    l_tiempo_promedio_espera_hosp = []
    l_tiempo_promedio_espera_opr101_011 = []
    l_tiempo_promedio_espera_opr102_001 = []
    l_tiempo_promedio_espera_opr101_033 = []
    l_tiempo_promedio_espera_opr102_003 = []

# plt.hist(l_services_times_hosp)

    i = 0
    warmtime = 500
    for trial in range(100):
        ciw.seed(trial)
        Q = ciw.Simulation(N, node_class=[ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode,
                           ciw.PSNode, ciw.PSNode, ciw.PSNode, ciw.PSNode], tracker=trackers.NodePopulation())
        # Aca se calibra el programa
        Q.simulate_until_max_time(168*8 + warmtime)
        recs = Q.get_all_records()

        analisis_data_nodo_adm = generacion_data_replica_n(
            recs, 1, warmtime, trial)
        analisis_data_nodo_boxes = generacion_data_replica_n(
            recs, 2, warmtime, trial)
        analisis_data_nodo_hosp = generacion_data_replica_n(
            recs, 3, warmtime, trial)
        analisis_data_opr011 = generacion_data_replica_n(
            recs, 4, warmtime, trial)
        analisis_data_opr001 = generacion_data_replica_n(
            recs, 5, warmtime, trial)
        analisis_data_opr033 = generacion_data_replica_n(
            recs, 6, warmtime, trial)
        analisis_data_opr003 = generacion_data_replica_n(
            recs, 7, warmtime, trial)


# Calculo Tiempo de servicio Nodos:
        services_times_admision = analisis_data_nodo_adm.obtener_service_time_nodo()
        analisis_data_nodo_adm.guardar_datos_replica(
            services_times_admision, l_services_times_admision)
        services_times_boxes = analisis_data_nodo_boxes.obtener_service_time_nodo()
        analisis_data_nodo_boxes.guardar_datos_replica(
            services_times_boxes, l_service_times_boxes)
        services_times_hosp = analisis_data_nodo_hosp.obtener_service_time_nodo()
        analisis_data_nodo_hosp.guardar_datos_replica(
            services_times_hosp, l_services_times_hosp)
        services_times_opr101_011 = analisis_data_opr011.obtener_service_time_nodo()
        analisis_data_opr011.guardar_datos_replica(
            services_times_opr101_011, l_services_times_opr101_011)
        services_times_opr102_001 = analisis_data_opr001.obtener_service_time_nodo()
        analisis_data_opr001.guardar_datos_replica(
            services_times_opr102_001, l_services_times_opr102_001)
        services_times_opr101_033 = analisis_data_opr033.obtener_service_time_nodo()
        analisis_data_opr033.guardar_datos_replica(
            services_times_opr101_033, l_services_times_opr101_033)
        services_times_opr102_003 = analisis_data_opr003.obtener_service_time_nodo()
        analisis_data_opr003.guardar_datos_replica(
            services_times_opr102_003, l_services_times_opr102_003)

# Calculo Largo promedio Cola:

        largo_cola_admision = analisis_data_nodo_adm.largo_cola_nodo()
        analisis_data_nodo_adm.guardar_datos_replica(
            largo_cola_admision, l_largo_admision)
        largo_cola_boxes = analisis_data_nodo_boxes.largo_cola_nodo()
        analisis_data_nodo_boxes.guardar_datos_replica(
            largo_cola_boxes, l_largo_boxes)
        largo_cola_hosp = analisis_data_nodo_hosp.largo_cola_nodo()
        analisis_data_nodo_hosp.guardar_datos_replica(
            largo_cola_hosp, l_largo_hosp)
        largo_cola_opr101_011 = analisis_data_opr011.largo_cola_nodo()
        #breakpoint()
        analisis_data_opr011.guardar_datos_replica(
            largo_cola_opr101_011, l_largo_opr101_011)
        largo_cola_opr102_001 = analisis_data_opr001.largo_cola_nodo()
        analisis_data_opr001.guardar_datos_replica(
            largo_cola_opr102_001, l_largo_opr102_001)
        largo_cola_opr101_033 = analisis_data_opr033.largo_cola_nodo()
        analisis_data_opr033.guardar_datos_replica(
            largo_cola_opr101_033, l_largo_opr101_033)
        largo_cola_opr102_003 = analisis_data_opr003.largo_cola_nodo()
        analisis_data_opr003.guardar_datos_replica(
            largo_cola_opr102_003, l_largo_opr102_003)

# Calculo tiempo promedio en cola por nodo:
        tiempo_promedio_en_cola_admision = analisis_data_nodo_adm.obtener_tiempos_en_cola_nodo()
        analisis_data_nodo_adm.guardar_datos_replica(
            tiempo_promedio_en_cola_admision, l_tiempo_promedio_espera_admision)
        tiempo_promedio_en_cola_boxes = analisis_data_nodo_boxes.obtener_tiempos_en_cola_nodo()
        analisis_data_nodo_boxes.guardar_datos_replica(
            tiempo_promedio_en_cola_boxes, l_tiempo_promedio_espera_boxes)
        tiempo_promedio_en_cola_hosp = analisis_data_nodo_hosp.obtener_tiempos_en_cola_nodo()
        analisis_data_nodo_hosp.guardar_datos_replica(
            tiempo_promedio_en_cola_hosp, l_tiempo_promedio_espera_hosp)
        tiempo_promedio_en_cola_opr101_011 = analisis_data_opr011.obtener_tiempos_en_cola_nodo()
        analisis_data_opr011.guardar_datos_replica(
            tiempo_promedio_en_cola_opr101_011, l_tiempo_promedio_espera_opr101_011)
        tiempo_promedio_en_cola_opr102_001 = analisis_data_opr001.obtener_tiempos_en_cola_nodo()
        analisis_data_opr001.guardar_datos_replica(
            tiempo_promedio_en_cola_opr102_001, l_tiempo_promedio_espera_opr102_001)
        tiempo_promedio_en_cola_opr101_033 = analisis_data_opr033.obtener_tiempos_en_cola_nodo()
        analisis_data_opr033.guardar_datos_replica(
            tiempo_promedio_en_cola_opr101_033, l_tiempo_promedio_espera_opr101_033)
        tiempo_promedio_en_cola_opr102_003 = analisis_data_opr003.obtener_tiempos_en_cola_nodo()
        analisis_data_opr003.guardar_datos_replica(
            tiempo_promedio_en_cola_opr102_003, l_tiempo_promedio_espera_opr102_003)

        mean_service_times = sum(services_times_boxes) / \
            len(services_times_boxes)
        average_service_times.append(mean_service_times)

#        mean_wait = sum(waits) / len(waits) #Tpo promedio de espera del sistema (en cola)
#        average_waits.append(mean_wait) #Tpo

        if trial in (50, 90, 100):
            Q.write_records_to_file(f'rep1_shared{trial}.csv', headers=True)
    breakpoint()
            

