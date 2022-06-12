## Parte 1:
#entre 00 y 7 hrs--> lambda = 0,136775059, entre 7 y 23:59-> lambda = 0,254
from math import log
from operator import index
from random import seed
from matplotlib import pyplot as plt
import numpy as np


def tasa_no_homo(t):
    hora = t % 24
    if hora >= 0 and hora <= 7:
        return 0.13677

    elif hora > 7 and hora <= 12:
        r = 0.02346*hora - 0.02752
        return r

    elif hora > 12 and hora <= 21.5:        
        return 0.254

    else:
        r = -0.046892*hora + 1.2621
        return r

#Simular la parte homogenea:
"""
1) crear los intervalos y los visualizamos
"""
i = 0
y = []
dt = []
b = 24*10
while i <= b:
    pto = tasa_no_homo(i)
    y.append(pto)
    dt.append(round(i,3))
    i += 0.1



#np.random.seed(1010)
lamda_plus = 0.254 # tasa no homo maxima, tpo entre llegadas maximo

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
        pass

ind = [i*1 for i in lol]

x = sum(ind)
Nt1 = [i for i in range(x)]

j = [i for i in range(len(ind)) if ind[i] == 1]

s3 = [s2[i] for i in j]

t_entre = [s3[i]-s3[i-1] for i in range(1,len(s3))]

eje_y = [0] + Nt1 + [max(Nt1)]
eje_x = [0] + s3 + [b]
plt.step(eje_x, eje_y)


breakpoint()









