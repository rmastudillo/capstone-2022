from cargar_matriz import Matriz_procesada
from collections import namedtuple
from random import choices
import csv
"""
Cada vez que se corra este codigo se van a crear dos archivos con los pacientes simulados
N_pacientes es el numero de pacientes a generar
"""
N_pacientes = 800
"""
"""
posibilidades = ['URG101_003', 'DIV101_703', 'DIV101_603', 'DIV101_604', 'DIV102_203', 'DIV103_107',
                 'DIV104_602', 'DIV103_204', 'OPR102_001', 'OPR101_011', 'OPR102_003', 'OPR101_033', 'Otro', 'End']
areas = {'URG101_003': [], 'DIV101_703': [], 'DIV101_603': [], 'DIV101_604': [], 'DIV102_203': [], 'DIV103_107': [],
         'DIV104_602': [], 'DIV103_204': [], 'OPR102_001': [], 'OPR101_011': [], 'OPR102_003': [], 'OPR101_033': [],
         'Otro': [], 'End': [],
         }


"""
Agregando los supuestos de que todos pasan de admision al box y que de otro a salida
"""
Matriz_procesada[0] = [0.0, 1, 0.0, 0.0, 0.0, 0.0,
                       0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
# Matriz_procesada[12] = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
#                        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
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


def crear_pacientes(N_pacientes, posibilidades):
    pacientes = []
    for _i in range(0, N_pacientes):
        u_actual = 'URG101_003'
        paciente = namedtuple(
            'Paciente', ['n_recorrido', 'i_recorrido'])
        paciente.n_recorrido = [u_actual]
        paciente.i_recorrido = [areas[u_actual][0]]
        while u_actual != 'End':
            siguiente_destino = seleccionar_siguiente_paso(
                posibilidades, u_actual)
            paciente.n_recorrido.append(siguiente_destino)
            paciente.i_recorrido.append(areas[siguiente_destino][0])
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
    writer = csv.DictWriter(f, fieldnames=['Case ID', 'Area', 'Num_area'])
    writer.writeheader()
    _index = 0
    for paciente in pacientes:
        contenido = {'Case ID': _index, 'Area': paciente.n_recorrido,
                     'Num_area': paciente.i_recorrido}

        writer.writerow(contenido)
        _index += 1
