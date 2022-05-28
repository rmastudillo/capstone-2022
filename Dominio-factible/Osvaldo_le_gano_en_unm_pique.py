import itertools
import numpy

Pr_24=[25000,800]
Pr_Box=[12500,450]
Pr_Vent=[0, 150]
Pr_Cama = [3500,250]
Presup_Op = 4500
Presup_Ca = 50000
#2 VENTANILLAS, 3 BOXES, 16 CAMAS, QUIROFANO
lst = list(map(list, itertools.product([0, 1], repeat=22)))
lst_costCAP = [Pr_Vent[0],Pr_Vent[0],Pr_Box[0],Pr_Box[0],Pr_Box[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0],Pr_Cama[0], Pr_24[0]]
lst_costOP = [Pr_Vent[1],Pr_Vent[1],Pr_Box[1],Pr_Box[1],Pr_Box[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1],Pr_Cama[1], Pr_24[1]]
lst_fact = []
for i in range(len(lst)):
   a = numpy.dot(lst[i], lst_costCAP, out=None)
   b = numpy.dot(lst[i], lst_costOP, out=None)
   if a <= Presup_Ca and b <= Presup_Op:
       lst_fact.append(lst[i])
i = 0
while i < 10:
    print(lst_fact[i])
    i+=1


