import matplotlib.pyplot as plt
import numpy as np
from optimisation_2 import *

### on étudie n cas de fraudes dont les données seraient pour chaque cas : (gain_potentiel, probabilité de fraude) où la probabilité serait obtenu 
# grâce à l'algo 
### On considère qu'on ne peut traiter que k < n cas 

n = 14
k = 10

### On suppose la liste cas rangé dans l'ordre croissant de gain_potentiel

cas = [(100, 0.9), 
        (200, 0.95),
        (600, 0.8),
        (1000, 0.5), 
        (1100, 0.1), 
        (1100, 0.5),
        (1200, 0.6), 
        (1250, 0.4), 
        (1600, 0.05), 
        (100, 0.01), 
        (70, 0.03),
        (2000, 0.65), 
        (90, 0.3),
        (1700, 0.8)
        ]

pas = 50

danger, neg, cas, n, k = nouveau()

### On cherche à écrire une fonction qui donne tous les sous-ensembles de cardinal k de l'ensemble [[0, n]]

def sous_ensemble(k, n) : 
        if k == 1 : 
                return [[i] for i in range (0, n+1)]
        else : 
                L = sous_ensemble(k-1, n)
                M = []
                for l in L : 
                        for j in range (0, n+1) : 
                                if (j not in l and j > max(l)): 
                                        M.append(l+[j])
        return M 

### X est notre axe des abscisses et Y la liste de nos listes d'ordonnées correspondant à chaque cas 
### Y est la proba P(gain >= x) pour une cmbinaison k donnée

tot = 0 

for j in range (0, k) : 
        tot += cas[-1-j][0]

total = int(tot/pas)

X = [(i * pas) for i in range (total + 1 )] 

combinaisons = sous_ensemble(k,n-1)

Y = [[] for i in range (len(combinaisons))] 
z = 0
w = len(combinaisons[0])

### Ecrire une fonction qui étant donné une combinaison, la liste des cas et un entier x, donne la probabilité que le gain potentiel associé à cette combinaison 
### soit >= à x 

def proba(combinaison, x, cas) : 
        n = len(combinaison)
        p = 0

        for j in range (1, n+1) :
                L = sous_ensemble(j, n-1)
                for l in L : 
                        S = 0 
                        u = 1
                        for i in l : 
                                S += cas[combinaison[i]][0]

                        if S >= x : 
                                M = [combinaison[w] for w in l]
                                for i in combinaison : 
                                        if i in M : 
                                               u *= cas[i][1]
                                        else : 
                                               u *= (1 - cas[i][1])
                                p += u

        return p 

#print(proba((0,1), 101, cas) )                       
      

for t in combinaisons : 

        for i in X : 
                p = proba(t, i, cas)
                Y[z].append(p)
        z += 1 


print("nombre de courbes =", len(Y))
print(danger)

for j in range (len(Y)) : 
        plt.plot(X, Y[j])


plt.show()






    



