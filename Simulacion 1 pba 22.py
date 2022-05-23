from bdb import Breakpoint
from statistics import NormalDist
from tkinter.ttk import Progressbar
import ciw
from matplotlib import pyplot as plt

N = ciw .create_network(

    arrival_distributions=[
        ciw.dists.Exponential(rate=(0.00569)),  # Adm
        ciw.dists.NoArrivals(),  # BOXES
        ciw.dists.NoArrivals(),  # salas hosp
        ciw.dists.NoArrivals(),  # opr
        ciw.dists.NoArrivals(),  # opr
        ciw.dists.NoArrivals(),  # opr
        ciw.dists.NoArrivals(),  # opr
        ciw.dists.NoArrivals()  # Otros
    ],

    service_distributions=[
        ciw.dists.Gamma(shape=26.14, scale=(1/4.735)),  # Adm
        ciw.dists.Gamma(shape=2.289, scale=(1/0.056)),  # Boxes
        ciw.dists.Weibull(scale=68.13, shape=0.65),  # salas hosp

        ciw.dists.Weibull(scale=152.74, shape=4.64),  # opr101_011 ; EXCL
        ciw.dists.Normal(mean=143.40, sd=35.06),  # opr102_001 ; EXCL

        ciw.dists.Normal(mean=148.72, sd=32.18),  # opr101_033 ; Gral
        ciw.dists.Normal(mean=148.42, sd=27.95),  # opr102_003 ; Gral

        ciw.dists.Normal(mean=148.96, sd=28.51)  # OTROS ;

    ],

    routing=[

        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0],  # Adm
        [0.0, 0.0, 0.39, 0.0, 0.001, 0.001, 0.03, 0.35],  # BOXES
        [0.0, 0.0, 0.0325, 0.001, 0.0762, 0.0077, 0.1214, 0.1326],  # salas hosp
        [0.0, 0.0, 0.55, 0.0, 0.0, 0.0, 0.45, 0.0],  # opr101_011 ; EXCL
        [0.0, 0.0, 0.034, 0.95, 0.0, 0.0, 0.0, 0.016],  # opr102_001 ; EXCL
        [0.0, 0.148, 0.563, 0.0, 0.0, 0.0, 0.0, 0.282],  # opr101_033 ; Gral
        [0.0, 0.02, 0.119, 0.0, 0.0, 0.829, 0.0, 0.032],  # opr102_003 ; Gral
        [0.0, 0.002, 0.091, 0.0, 0.044, 0.009, 0.058, 0.288]  # otro
    ],

    number_of_servers=[3, 5, 61, 2, 2, 2, 2, 10]
)

# routing= [

#     [0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], #Adm
#     [0.0, 0.0, 0.3870, 0.0, 0.001, 0.001, 0.030, 0.346],#BOXES
#     [0.0, 0.0, 0.0325, 0.00133, 0.076167, 0.00767, 0.1214, 0.1326], # salas hosp
#     [0.0, 0.0, 0.55, 0.0, 0.0, 0.0, 0.45, 0.0], # opr101_011 ; EXCL
#     [0.0, 0.0, 0.034, 0.95, 0.0, 0.0, 0.0, 0.0160], # opr102_001 ; EXCL
#     [0.0, 0.148, 0.563, 0.0, 0.0, 0.0, 0.0, 0.282], # opr101_033 ; Gral
#     [0.0, 0.02, 0.119, 0.0, 0.0, 0.8290, 0.0, 0.032], # opr102_003 ; Gral
#     [0.0, 0.002, 0.091, 0.0, 0.044, 0.009, 0.058, 0.2880] # otro
# ]


# Por ahora, la probabilidad de ir al nodo otro se descartara solo para probar.
# Hay que crear el nodo otros. implica que tengo que generar una distribucion especifica a ese nodo, como de
# Transicion para modelar si de otro entra nuevamente o se va.
# Vamos a tener que tratar por separado cada sala de opr.

# Orden de nodos y parametros:
# 1) Adm.
# 2) Boxes : Gamma(shape 2.203685, rate  3.045886) ; LogNorm(meanlog -0.5674463, sdlog 0.7201865) Ambas en HRS
# 3) Salas Hosp. : WEI(shape  0.6485264, scale 68.1353693) En Horas
# 4) Opr. : Vamos  a tomarlas por separado.
# 4.1) opr101_011: WEI(shape 4.703116, scale 2.547516), EXCL URG ; p-value = 0.8319
# 4.2) opr102_001: WEI(shape 4.572325, scale 2.617678), EXCL URG ; p-value = 0.7948
# 4.3) opr101_033: NORM( mean 2.4626761, sd 0.5254923); Gral ; p-value = 0.2613
# 4.4) opr102_003: NORM(mean 2.4826667, sd 0.4752188) ; Gral ; p-value = 0.3544
# 5)Otros :
# 0) Salida

# https://ciw.readthedocs.io/en/latest/Guides/server_schedule.html


# https://ciwpython.github.io/CiwVis/ : Para visualizar la data altoque !

# https://ciw.readthedocs.io/en/latest/Guides/processor-sharing.html
# https://ciw.readthedocs.io/en/latest/Guides/behaviour/server_dependent_dist.html hay un ploteo bueno
# https://ciw.readthedocs.io/en/latest/Guides/process_based.html#process-based
# https://scikit-learn.org/stable/supervised_learning.html#supervised-learning

if __name__ == '__main__':
    print("hla")
    average_waits = []
    average_service_times = []
    service_times2 = []
    i = 0
    for trial in range(100):
        ciw.seed(trial)
        Q = ciw.Simulation(N, node_class=ciw.PSNode)
        Q.simulate_until_max_time(10080*4)  # Aca se calibra el programa
        recs = Q.get_all_records()
        waits = [r.waiting_time for r in recs]
        services_times = [
            s.service_time for s in recs if s.node == 6 if s.arrival_date > 5500]
        for i in services_times:
            service_times2.append(i)
        mean_service_times = sum(services_times)/len(services_times)
        average_service_times.append(mean_service_times)
        # Tpo promedio de espera del sistema (en cola)
        mean_wait = sum(waits) / len(waits)
        average_waits.append(mean_wait)  # Tpo
    plt.hist(service_times2, density=True)
    Q.write_records_to_file(f'rep1_shared{trial}.csv', headers=True)
    print(Q.statetracker.history )

    # breakpoint()


# DEBERIA HACER 20 ARCHIVOS DE DATA DE REPLICAS, PARA ASI ANALIZAR.
# AHORA ESTOY IMPRIMIENDO LOS DATOS EN UN SOLO ARCHIVO, DEBEMOS COMPARAR POR SEPARADO CADA REPLICA.
