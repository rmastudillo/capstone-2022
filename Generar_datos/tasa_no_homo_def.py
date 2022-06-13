from math import log
from random import seed
from matplotlib import pyplot as plt
import numpy as np


def lista_t_entre_llegadas(N_pacientes):
    """ 
    b: el intervalo de tiempo que se simulara, (0, b]
    
    """
    b = N_pacientes/0.13677
    
    def tasa_no_homo(t):
        hora = t % 24
        
        if hora >= 0 and hora <= 7:
            return 0.254

        elif hora > 7 and hora <= 12:
            r = 0.02346*hora - 0.02752
            return r

        elif hora > 12 and hora <= 21.5:        
            return 0.13677

        else:
            r = -0.046892*hora + 1.2621
            return r
    
    """
    Parte Homogenea:
    1) crear los intervalos y los visualizamos
    """

    i = 0
    y = []
    dt = []
    while i <= b:
        pto = tasa_no_homo(i)
        y.append(pto)
        dt.append(round(i,3))
        i += 0.1

    """
    Lamda_plus representa el maximo de la tasa de llegada variable
    m: representa el numero de datos que generaremos, el cual debe ser
       mayor que la cantidad de personas esperadas entre (0,b]
    """
    lamda_plus = 0.254 
    m = round(lamda_plus*b*5) # hacemos un numero que sea mas grande que el valor esperado de pacientes al dia.
    
    u = np.random.uniform(0,1,m)
    t = [round((-1/lamda_plus)*log(i), 3) for i in u]

    p = 0
    s1 = []
    for i in t:
        p += i
        s1.append(p)
        pass

    s2 = [n for n in s1 if n <= b]
    nstar = len(s2)

    w = np.random.uniform(0,1,size = nstar)

    lol = []
    t_entre_llegadas = []
    for i in range(len(w)):
        lam = s2[i]
        lam1 = tasa_no_homo(lam)/lamda_plus
        k = w[i]
        # print('lam', lam1)
        # print('k', k)

        bul = (k <= lam1)
        lol.append(bul)
        if bul:
            t_entre_llegadas.append(t[i])
            

    ind = [i*1 for i in lol]

    x = sum(ind)
    Nt1 = [i for i in range(x)]

    j = [i for i in range(len(ind)) if ind[i] == 1]

    horas_llegada_pacientes = [s2[i] for i in j]

    eje_y = [0] + Nt1 + [max(Nt1)]
    eje_x = [0] + horas_llegada_pacientes + [b]
    #plt.step(eje_x, eje_y)

    # plt.hist(t_entre_llegadas)
    # plt.show()

    return t_entre_llegadas


if __name__=="__main__":
    medias = []
    desviaciones = []
    for i in range(200):
        l = lista_t_entre_llegadas(300)
        media = np.mean(l)
        sd = np.std(l)
        medias.append(media)
        desviaciones.append(sd)
    
    media_todo = np.mean(medias)
    desviaciones_todo = np.mean(desviaciones)
    breakpoint()
    