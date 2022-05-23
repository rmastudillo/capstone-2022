# capstone-2022
# Pasos
  - Crear los datos para alimentar la simulación, con destinos en la red definidos y acorde a la matriz de transición.
  - Verificar el comportamiento de la red en el codigo de la simulación.

#Para las llegadas:
#https://ciw.readthedocs.io/en/latest/Guides/process_based.html
Creo una funcion de ruta para cada nodo, en el cual le entrego un diccionario, la llave es el número del paciente, y el resultado es al nodo que se dirije, de esta manera determino el camino de antemano.
- Tengo que crear una función que genere estas llegadas y las exporte a un archivo. Luego, cargo estas llegadas en el main para asegurarme que siempre son las mismas.