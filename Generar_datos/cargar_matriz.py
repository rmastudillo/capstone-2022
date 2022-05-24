import pandas as pd


Matriz_sin_procesar = pd.read_csv(
    'matrizT.csv', encoding='UTF-8', sep=',').fillna(0).reset_index()
Matriz_cambiofila = Matriz_sin_procesar.reindex(
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 13, 12])
Matriz_procesada = []
for index, row in Matriz_cambiofila.iterrows():
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
    if index == 13:
        fila = [0.00, 0.00, 0.02, 0.02, 0.01, 0.00,
                0.03, 0.02, 0.04, 0.00, 0.06, 0.01, 0.29, 0.51]
    elif index == 12:
        fila[-1] = 1.0
        fila[12] = 0.0
    Matriz_procesada.append(fila)
print(Matriz_procesada)