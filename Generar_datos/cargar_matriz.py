import pandas as pd

Matriz_sin_procesar = pd.read_csv(
    'matrizT.csv', encoding='UTF-8', sep=',').fillna(0).reset_index()
Matriz_procesada = []
for index, row in Matriz_sin_procesar.iterrows():
    fila = [row['URG101_003'],
            row['DIV101_703'],
            row['DIV101_603'],
            row['DIV101_604'],
            row['DIV102_203'],
            row['DIV103_107'],
            row['DIV104_602'],
            row['DIV103_204'],
            row['OPR102_001'],
            row['OPR101_011'],
            row['OPR102_003'],
            row['OPR101_033'],
            row['Otro'],
            row['End']]
    Matriz_procesada.append(fila)
