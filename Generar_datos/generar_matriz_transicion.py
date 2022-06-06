import pandas as pd
import csv
from collections import defaultdict
data_original = pd.read_csv('Datos/Datos.csv', encoding='UTF-8', sep=';')
todos_las_areas = ['URG101_003', 'BRU101_201', 'OPR102_003', 'OPR101_033', 'SPE104_201',
                   'DIV101_703', 'End', 'DIV103_204', 'DIV105_207', 'DIV104_602', 'DIV104_601',
                   'DIV201_206', 'INT200_902', 'DIV100_605', 'DIV101_604', 'OPR102_002', 'OPR101_022',
                   'DIV101_603', 'DAY101_101', 'OUT3190', 'OPR102_001', 'OPR101_011', 'DIV105_105',
                   'SPE101_401', 'DIV105_108', 'DIV102_203', 'SPE101_601', 'DIV104_201', 'DIV103_107',
                   'DIV200_109', 'DIV104_102', 'DIV100_109', 'DIV104_101', 'SPE103_202', 'OUT3170', 'DIV201_110',
                   'DIV200_701', 'OPR200_004', 'OPR200_044', 'DIV200_106', 'DIV200_104', 'DIV200_208', 'DAY100_201',
                   'DIV200_202', 'DIV200_209', 'DIV200_401']
data = data_original.copy()
# Cambiamos el nombre de las columnas del archivo datos
data.columns = ['ID', 'Area', 'Datetime']
# Cambiamos el tipo de las fechas a date time
data['Datetime'] = pd.to_datetime(data['Datetime'])
# Formato de la fecha es año-mes-dia
# Separamos la fecha de la hora
data['Date'] = data['Datetime'].dt.date
data['Time'] = data['Datetime'].dt.time
datos = defaultdict(dict)
codigos_interes = [
    'URG101_003', 'DIV101_703', 'DIV101_603',
    'DIV101_604', 'DIV102_203', 'DIV103_107',
    'DIV104_602', 'DIV103_204', 'OPR102_001',
    'OPR101_011', 'OPR102_003', 'OPR101_033',
    'End'
]
codigos_otros = list(set(todos_las_areas).difference(codigos_interes))[:]

index = 0  # Contador para saber donde están las cosas
for row in data.iterrows():
    area = row[1]['Area']

    if not(area in datos.keys()):
        datos[area]['index'] = []
        datos[area]['hora'] = []
        datos[area]['siguiente_destino'] = defaultdict(dict)
        datos[area]['numero_arribos'] = 0
    datos[area]['index'].append(index)
    datos[area]['hora'].append(row[1]['Time'])
    datos[area]['numero_arribos'] += 1
    if area == 'End':
        index += 1
        continue
    if index == 4242:
        break
    if not (data.iloc[index+1]['Area'] in datos[area]['siguiente_destino'].keys()):
        datos[area]['siguiente_destino'][data.iloc[index+1]['Area']] = 0
    datos[area]['siguiente_destino'][data.iloc[index+1]['Area']] += 1

    index += 1
total = 0
for boxes in codigos_otros:
    total += datos[boxes]['numero_arribos']
datos['Otro']['numero_arribos'] = total
# Cuantos pacientes llegaron desde el area A al area B
for boxes in codigos_interes:
    datos[boxes]['siguiente_destino_porcentual'] = defaultdict(dict)
    for lugares in datos[boxes]['siguiente_destino'].keys():
        if lugares in codigos_interes:
            datos[boxes]['siguiente_destino_porcentual'][lugares] = round(
                datos[boxes]['siguiente_destino'][lugares]/datos[boxes]['numero_arribos'], 3)
            datos['Otro']['siguiente_destino'] = defaultdict(dict)
for boxes in codigos_otros:
    siguiente = list(set(codigos_interes) & set(
        datos[boxes]['siguiente_destino'].keys()))[:]
    for index in siguiente:
        if not(index in (datos['Otro']['siguiente_destino'].keys())):
            datos['Otro']['siguiente_destino'][index] = 0
        datos['Otro']['siguiente_destino'][index] += datos[boxes]['siguiente_destino'][index]
        # Otro porcentual
datos['Otro']['siguiente_destino_porcentual'] = defaultdict(dict)
for lugares in datos['Otro']['siguiente_destino'].keys():
    if lugares in codigos_interes:
        datos['Otro']['siguiente_destino_porcentual'][lugares] = round(
            datos['Otro']['siguiente_destino'][lugares]/datos['Otro']['numero_arribos'], 3)
for boxes in codigos_otros:
    datos[boxes]['siguiente_destino_porcentual'] = defaultdict(dict)
    for lugares in datos[boxes]['siguiente_destino'].keys():
        if lugares in codigos_interes:
            datos[boxes]['siguiente_destino_porcentual'][lugares] = round(
                datos[boxes]['siguiente_destino'][lugares]/datos[boxes]['numero_arribos'], 3)
fieldnames = ['Area'] + codigos_interes[:-1] + ['Otro'] + [codigos_interes[-1]]





with open('matrizT.csv', 'w', encoding='UTF8', newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for boxes in codigos_interes[:-1]:
        otro = 1
        _flujo = defaultdict(float)
        _flujo['Area'] = boxes
        for key in datos[boxes]['siguiente_destino_porcentual'].keys():
            _flujo[key] = datos[boxes]['siguiente_destino_porcentual'][key]
            otro -= datos[boxes]['siguiente_destino_porcentual'][key]
        otro = round(otro, 3)
        _flujo['Otro'] = otro
        writer.writerows([_flujo])
    otro = 1
    _flujo = defaultdict(float)
    _flujo['Area'] = 'Otro'
    for boxes in datos['Otro']['siguiente_destino_porcentual'].keys():
        _flujo[boxes] = datos['Otro']['siguiente_destino_porcentual'][boxes]
        otro -= datos['Otro']['siguiente_destino_porcentual'][boxes]
        _flujo['Otro'] = round(otro, 3)
    writer.writerows([_flujo])
    _flujo = defaultdict(float)
    _flujo['Area'] = 'End'
    _flujo['End'] = 1.0
    writer.writerows([_flujo])
