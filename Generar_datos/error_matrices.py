import numpy as np
import csv
Matriz_original = []
Matriz_generada = []
with open('matrizT.csv', 'r') as f:
    data = list(csv.reader(f, delimiter=","))
    data = data[1:]
for fila in data:
    contador = 0
    fila = fila[1:]
    for x in fila:
        if not x:
            fila[contador] = 0
        contador += 1
    Matriz_original.append(fila)
with open('matriz_t_g.csv', 'r') as f:
    data = list(csv.reader(f, delimiter=","))
data = data[1:]
for fila in data:
    contador = 0
    fila = fila[1:]
    for x in fila:
        if not x:
            fila[contador] = 0
        contador += 1
    Matriz_generada.append(fila)

Matriz_original = np.array(Matriz_original).astype(float)
Matriz_generada = np.array(Matriz_generada).astype(float)
# Error cuadratico medio entre las matrices
mse = ((Matriz_original - Matriz_generada)**2).mean()
print("Error cuadratico medio entre las matrices de transición =",
      round(mse*100, 2), "%")
