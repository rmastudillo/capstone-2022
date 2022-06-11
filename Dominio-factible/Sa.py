import numpy as np
import random as random
import itertools as iter

def factibilidad (configuracion):
    Pr_24=[25000,800]
    Pr_Box=[12500,450]
    Pr_Vent=[0, 150]
    Pr_Cama = [3500,250]
    Presup_Op = 4500
    Presup_Ca = 50000   
    lst = list(map(list, iter.product([0, 1], repeat=22)))
    lst_costCAP = [Pr_Vent[0],Pr_Vent[0],Pr_Box[0],Pr_Box[0],Pr_Box[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0], Pr_24[0]]
    lst_costOP = [Pr_Vent[1],Pr_Vent[1],Pr_Box[1],Pr_Box[1],Pr_Box[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1], Pr_24[1]]
    a = np.dot(lst[i], lst_costCAP, out=None)
    b = np.dot(lst[i], lst_costOP, out=None)
    if a <= Presup_Ca and b <= Presup_Op:
        return True
    else:
        return False

def generar_vecino(configuration):
    n=len(configuration)
    fact = False
    while not fact:
        casilla= random.randint(0,n-1)
        vecino_sa = np.copy(configuration)
        if vecino_sa[casilla]==0:
            vecino_sa[casilla] = 1
        else:
            vecino_sa[casilla] = 0 
        fact = factibilidad(vecino_sa)  #corroborar si lo haremos así o no 
    vecino_sim = [vecino_sa[0]+vecino_sa[1], vecino_sa[2] + vecino_sa[3]+  vecino_sa[4], vecino_sa[5] + vecino_sa[6] + vecino_sa[7], vecino_sa[8], vecino_sa[9]+ vecino_sa[10]+ vecino_sa[11], vecino_sa[12]+ vecino_sa[13], vecino_sa[14]+ vecino_sa[15]+ vecino_sa[16]+ vecino_sa[17], vecino_sa[18]+ vecino_sa[19]+ vecino_sa[20], vecino_sa[21]]
    return vecino_sa, vecino_sim

def simulacion (configuracion, escenarios):

    return 

def SA(NITER=100, Tk=1000, configuracion_inicial, alpha=0.99, beta=0.5):
    accept = 0

    configuracion = configuracion_inicial
    valor_actual = simulacion(configuracion_inicial, 30) #lista de largo cantidad de réplicas

    configuracion_ideal = [2,3,3,1,3,2,4,3,1]
    valor_ideal = simulacion(configuracion_ideal, 30)


    best_configuracion= np.copy(configuracion)
    best_valor = valor_actual
    iteracion = 0

    for i in range(NITER):
        valor_old = valor_actual
        vecino = generar_vecino(configuracion) # es de esa o de best_configuracion ???? 
        vecino_sa =vecino[0]
        vecino_sim = vecino[1]
        valor_vecino = simulacion(vecino_sim, 30)
        mu = np.mean(list(map(lambda x,y: x-y ,valor_vecino,valor_old)))
        s = np.std(list(map(lambda x,y: x-y ,valor_vecino,valor_old)), ddof = 1) # quizas hay que cambiar ddof a 1
        ancho = 1.96*s/np.sqrt(len(valor_vecino)) ## cantidad de réplicas, el largo de la lista
        intervalo= [mu - ancho, mu + ancho]
        if intervalo[1] < 0:
            configuracion = vecino_sa
            valor_actual = valor_vecino
            accept=1
            probT=1
            if valor_actual < best_valor:
                best_configuracion = np.copy(configuracion)
                best_valor = valor_actual
                iteracion = i+1
        elif intervalo[0] > 0:
            probT=np.exp(-mu/(beta*Tk))
            if probT >= np.random.uniform(0,1):
                configuracion=np.copy(vecino_sa)
                valor_actual=valor_vecino
                accept = 1
            else:
                accept=0

        else:
            while intervalo[0] < 0 and intervalo[1]>0: #fijar cuantas réplicas más y como la simulaciñon elige las extras distintas
                valor_vecino_ext = simulacion(vecino_sim, 10)
                valor_actual_ext = simulacion(configuracion, 10) #ver cúantas replicas extras y cómo se lo pedimos a la simulacion
                valor_vecino = valor_vecino + valor_vecino_ext
                valor_actual = valor_actual +valor_actual_ext
                mu = np.mean(list(map(lambda x,y: x-y ,valor_vecino,valor_actual)))
                s = np.std(list(map(lambda x,y: x-y ,valor_vecino,valor_actual)), ddof = 1) # quizas hay que cambiar ddof a 1
                ancho = 1.96*s/np.sqrt(len(valor_vecino)) ## cantidad de réplicas, el largo de la lista
                intervalo= [mu - ancho, mu + ancho]
            if intervalo[1] < 0:
                configuracion = vecino_sa
                valor_actual = valor_vecino
                accept=1
                probT=1
                if valor_actual < best_valor:
                    best_configuracion = np.copy(configuracion)
                    best_valor = valor_actual
                    iteracion = i+1
            elif intervalo[0] > 0:
                probT=np.exp(-mu/(beta*Tk))
                if probT >= np.random.uniform(0,1):
                    configuracion=np.copy(vecino_sa)
                    valor_actual=valor_vecino
                    accept = 1
                else:
                    accept=0
        if np.mean(best_valor) <= 1.2 * np.mean(valor_ideal): #tenemos que ver dd va 
            break
        Tk = alpha*Tk
    media_best = np.mean(best_valor)
    return best_valor, best_configuracion, media_best


h = generar_vecino([0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0])

print(h[0])
print(h[1])
