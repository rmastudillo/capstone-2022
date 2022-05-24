import pandas as pd
import csv
from collections import defaultdict

data_original = pd.read_csv(
    'pacientes_generados.csv', encoding='UTF-8', sep=',')
data = data_original.copy()
# Cambiamos el nombre de las columnas del archivo datos
data.columns = ['Case ID', 'Area', 'Num_area']
# Cambiamos el tipo de las fechas a date time
datos = defaultdict(dict)
codigos_interes = [
    'URG101_003', 'DIV101_703', 'DIV101_603',
    'DIV101_604', 'DIV102_203', 'DIV103_107',
    'DIV104_602', 'DIV103_204', 'OPR102_001',
    'OPR101_011', 'OPR102_003', 'OPR101_033',
    'Otro',
    'End'
]
codigos_otros = []
index = 0  # Contador para saber donde están las cosas
for row in data.iterrows():
    area = row[1]['Area']
    if not(area in datos.keys()):
        datos[area]['index'] = []
        datos[area]['siguiente_destino'] = defaultdict(dict)
        datos[area]['numero_arribos'] = 0
    datos[area]['index'].append(index)
    datos[area]['numero_arribos'] += 1
    if area == 'End':
        index += 1
        continue
    if not (data.iloc[index+1]['Area'] in datos[area]['siguiente_destino'].keys()):
        datos[area]['siguiente_destino'][data.iloc[index+1]['Area']] = 0
    datos[area]['siguiente_destino'][data.iloc[index+1]['Area']] += 1
    index += 1

# Cuantos pacientes llegaron desde el area A al area B
for boxes in codigos_interes:
    datos[boxes]['siguiente_destino_porcentual'] = defaultdict(dict)
    for lugares in datos[boxes]['siguiente_destino'].keys():
        if lugares in codigos_interes:
            datos[boxes]['siguiente_destino_porcentual'][lugares] = round(
                datos[boxes]['siguiente_destino'][lugares]/datos[boxes]['numero_arribos'], 3)
            if lugares == 'Otro':
                print(datos[boxes]
                      ['siguiente_destino_porcentual'][lugares])


fieldnames = ['Area'] + codigos_interes[:-1] + [codigos_interes[-1]]

with open('matriz_t_g.csv', 'w', encoding='UTF8', newline="") as f:
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    for boxes in codigos_interes[:-1]:
        _flujo = defaultdict(float)
        _flujo['Area'] = boxes
        for key in datos[boxes]['siguiente_destino_porcentual'].keys():
            _flujo[key] = datos[boxes]['siguiente_destino_porcentual'][key]
        writer.writerows([_flujo])
    _flujo = defaultdict(float)
    _flujo['Area'] = 'End'
    _flujo['End'] = 1.0
    writer.writerows([_flujo])
