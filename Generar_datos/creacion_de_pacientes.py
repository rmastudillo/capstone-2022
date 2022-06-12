from cargar_matriz import Matriz_procesada
from collections import namedtuple
from random import choices
from tiempos_atencion import *
import csv



"""
Cada vez que se corra este codigo se van a crear dos archivos con los pacientes simulados
N_pacientes es el numero de pacientes a generar
"""
N_pacientes = 300
"""
"""
posibilidades = ['URG101_003', 'DIV101_703', 'DIV101_603', 'DIV101_604', 'DIV102_203', 'DIV103_107',
                 'DIV104_602', 'DIV103_204', 'OPR102_001', 'OPR101_011', 'OPR102_003', 'OPR101_033', 'Otro', 'End']
areas = {'URG101_003': [], 'DIV101_703': [], 'DIV101_603': [], 'DIV101_604': [], 'DIV102_203': [], 'DIV103_107': [],
         'DIV104_602': [], 'DIV103_204': [], 'OPR102_001': [], 'OPR101_011': [], 'OPR102_003': [], 'OPR101_033': [],
         'Otro': [], 'End': [],
         }
t_atencion = {'URG101_003': t_urg101003,
              'DIV101_703': t_div101703,
              'DIV101_603': t_div101603,
              'DIV101_604': t_div101604,
              'DIV102_203': t_div102203,
              'DIV103_107': t_div103107,
              'DIV104_602': t_div104602,
              'DIV103_204': t_div103204,
              'OPR102_001': t_opr102001,
              'OPR101_011': t_opr101011,
              'OPR102_003': t_opr102003,
              'OPR101_033': t_opr101033,
              'Otro': t_otro, 'End': t_end,
              }
t_atencion_areas = {'URG101_003': [], 'DIV101_703': [], 'DIV101_603': [], 'DIV101_604': [], 'DIV102_203': [], 'DIV103_107': [],
                    'DIV104_602': [], 'DIV103_204': [], 'OPR102_001': [], 'OPR101_011': [], 'OPR102_003': [], 'OPR101_033': [],
                    'Otro': [], 'End': [],
                    }
"""
Agregando los supuestos de que todos pasan de admision al box y que de otro a salida
"""
Matriz_procesada[0] = [0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
Matriz_procesada[12] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
                        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]

"""
Fin de agregación de supuestos
"""
_indice_dic = 1  # Aqui se define si el primer nodo es el 0 o el 1, en este caso es el 1
for key in areas.keys():
    areas[key].append(_indice_dic)
    areas[key].append(Matriz_procesada[_indice_dic-1])
    _indice_dic += 1

"""
Comienzo a crear los pacientes
"""


def seleccionar_siguiente_paso(posibilidades, u_actual):
    camino_elegido = choices(posibilidades, weights=areas[u_actual][1], k=1)
    return camino_elegido[0]


def calcular_tiempo_atencion(u_actual):
    """
    retorna el tiempo de atención en horas
    """

    tiempo = 0
    return tiempo


def crear_pacientes(N_pacientes, posibilidades):
    b = round(N_pacientes/0.2) #Este es el tiempo estimado en que lleguen N_pacientes. Es decir, el tiempo esperado en que lleguen N_pacientes será b.
    l_tiempo_entre_llegadas = lista_t_entre_llegadas(N_pacientes)
    print(b/24)
    print(len(l_tiempo_entre_llegadas), N_pacientes)
    breakpoint()
    pacientes = []
    tiempo = 0
    for _i in range(0, N_pacientes):
        u_actual = 'URG101_003'
        paciente = namedtuple(
            'Paciente', ['n_recorrido', 'i_recorrido', 't_llegada', 't_atencion'])
        # Aca, se genera un intervalo de tiempo entre llegadas, segun la hora actual
        tiempo = l_tiempo_entre_llegadas[_i]
        paciente.t_llegada = tiempo  # Aca, se le asigna la hora de llegada al paciente
 
        l_tpo_pers = ['OPR102_001', 'OPR101_011', 'OPR102_003', 'OPR101_033', 'DIV103_204', 'DIV101_703']
        l_hosp = ['DIV101_603', 'DIV101_604', 'DIV102_203', 'DIV103_107', 'DIV104_602', 'DIV103_204']

        paciente.n_recorrido = [u_actual]
        paciente.i_recorrido = [areas[u_actual][0]]
        tiempo_atendido = t_atencion[u_actual]()
        paciente.t_atencion = [tiempo_atendido]
        t_atencion_areas[u_actual].append(tiempo_atendido)
        while u_actual != 'End':
            print(f"act: { u_actual}")
            siguiente_destino = seleccionar_siguiente_paso(
                posibilidades, u_actual) # u_actual = OPR, sgt sala hosp
            print(f"sgte{siguiente_destino}")
            paciente.n_recorrido.append(siguiente_destino)
            paciente.i_recorrido.append(areas[siguiente_destino][0])

            if siguiente_destino in l_hosp:
                act = u_actual
                print(act)
                print(f"sgte: {siguiente_destino}")
                if act in l_tpo_pers:
                    tiempo_atendido = t_atencion[siguiente_destino](act)

                else:
                    tiempo_atendido = t_atencion[siguiente_destino]()

            else:
                tiempo_atendido = t_atencion[siguiente_destino]()

            paciente.t_atencion.append(tiempo_atendido)
            t_atencion_areas[siguiente_destino].append(tiempo_atendido)
            u_actual = siguiente_destino
        pacientes.append(paciente)
    return(pacientes)


pacientes = crear_pacientes(N_pacientes, posibilidades)

with open('pacientes_generados.csv', 'w', encoding='UTF8', newline="") as f:
    writer = csv.DictWriter(f, fieldnames=['Case ID', 'Area', 'Num_area'])
    writer.writeheader()
    _index = 0
    for paciente in pacientes:
        recorridos = paciente.n_recorrido
        _i = 0
        for recorrido in recorridos:
            contenido = {'Case ID': _index, 'Area': recorrido,
                         'Num_area': paciente.i_recorrido[_i]}
            _i += 1
            writer.writerow(contenido)
        _index += 1
with open('pacientes_generados_ruta.csv', 'w', encoding='UTF8', newline="") as f:
    writer = csv.DictWriter(
        f, fieldnames=['Case ID', 'Area', 'Num_area', 'Tiempo_atencion', 'Tiempo_llegada'])
    writer.writeheader()
    _index = 0
    for paciente in pacientes:
        contenido = {'Case ID': _index, 'Area': paciente.n_recorrido,
                     'Num_area': paciente.i_recorrido, 'Tiempo_atencion': paciente.t_atencion[:-1], 'Tiempo_llegada': paciente.t_llegada}  # paciente.i_recorrido[:-1]}

        writer.writerow(contenido)
        _index += 1
with open('pacientes_generados_ruta.csv', 'w', encoding='UTF8', newline="") as f:
    writer = csv.DictWriter(
        f, fieldnames=['Case ID', 'Area', 'Num_area', 'Tiempo_atencion', 'Tiempo_llegada'
                       ])
    writer.writeheader()
    _index = 0
    for paciente in pacientes:
        contenido = {'Case ID': _index, 'Area': paciente.n_recorrido,
                     'Num_area': paciente.i_recorrido, 'Tiempo_atencion': paciente.t_atencion[:-1], 'Tiempo_llegada': paciente.t_llegada}  # paciente.i_recorrido[:-1]}
        writer.writerow(contenido)
        _index += 1

print(len(t_atencion_areas['URG101_003']))




