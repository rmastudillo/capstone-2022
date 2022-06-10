from pydoc import cram
from cargar_matriz import Matriz_procesada
from collections import namedtuple
from random import choices
from tiempos_atencion import *
import csv
import os

"""
Cada vez que se corra este codigo se van a crear dos archivos con los pacientes simulados
N_pacientes es el numero de pacientes a generar, N_datos es el Numero de archivos con N_pacientes generados
"""
N_pacientes = 100000
N_bdd = 30

"""
Crear carpetas
"""

dir_path = os.path.dirname(os.path.realpath(__file__))+"/Pacientes_sim"
dir_path_old = os.path.dirname(os.path.realpath(__file__))+"/Pacientes_old"
os.makedirs(dir_path, exist_ok=True)
os.makedirs(dir_path_old, exist_ok=True)

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


def uniquify(path):
    """
    Retorna un nuevo path para que se creen los pacientes
    """
    filename, extension = os.path.splitext(path)
    counter = 1

    while os.path.exists(path):
        path = filename[:-1] + str(counter) + extension
        counter += 1

    return path


def crear_pacientes(N_pacientes, posibilidades):
    pacientes = []
    tiempo = 0
    tpo_actual_aux = 0
    for _i in range(0, N_pacientes):
        u_actual = 'URG101_003'
        paciente = namedtuple(
            'Paciente', ['n_recorrido', 'i_recorrido', 't_llegada', 't_atencion'])
        # Aca, se genera un intervalo de tiempo entre llegadas, segun la hora actual
        tiempo = t_llegada_entre_pacientes(tpo_actual_aux)
        paciente.t_llegada = tiempo  # Aca, se le asigna la hora de llegada al paciente
        # Aqui, avanzaremos la variable auxiliar de tpo actual, para decidir cuando cambiar la tasa de atencion.
        tpo_actual_aux += tiempo
        # if tpo_actual_aux esta entre 00 y 6:59 am, generar tiempo con tasa x
        # en otro caso, la otra tasa
 
        l_tpo_pers = ['OPR102_001', 'OPR101_011', 'OPR102_003', 'OPR101_033', 'DIV103_204', 'DIV101_703']
        l_hosp = ['DIV101_603', 'DIV101_604', 'DIV102_203', 'DIV103_107', 'DIV104_602', 'DIV103_204']

        paciente.n_recorrido = [u_actual]
        paciente.i_recorrido = [areas[u_actual][0]]
        tiempo_atendido = t_atencion[u_actual]()
        paciente.t_atencion = [tiempo_atendido]
        t_atencion_areas[u_actual].append(tiempo_atendido)
        while u_actual != 'End':
            siguiente_destino = seleccionar_siguiente_paso(
                posibilidades, u_actual) # u_actual = OPR, sgt sala hosp
            paciente.n_recorrido.append(siguiente_destino)
            paciente.i_recorrido.append(areas[siguiente_destino][0])

            if siguiente_destino in l_hosp:
                act = u_actual

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


def crear_bdd(N_pacientes, N_bdd):
    for _i in range(0, N_bdd):
        pacientes = crear_pacientes(N_pacientes, posibilidades)
        with open(uniquify(dir_path_old+'/pacientes_generados_0.csv'), 'w', encoding='UTF8', newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=['Case ID', 'Area', 'Num_area'])
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
        with open(uniquify(dir_path+'/pacientes_generados_ruta_0.csv'), 'w', encoding='UTF8', newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=['Case ID', 'Area', 'Num_area', 'Tiempo_atencion', 'Tiempo_llegada'])
            writer.writeheader()
            _index = 0
            for paciente in pacientes:
                contenido = {'Case ID': _index, 'Area': paciente.n_recorrido,
                             'Num_area': paciente.i_recorrido, 'Tiempo_atencion': paciente.t_atencion[:-1], 'Tiempo_llegada': paciente.t_llegada}  # paciente.i_recorrido[:-1]}

                writer.writerow(contenido)
                _index += 1


crear_bdd(N_pacientes, N_bdd)
