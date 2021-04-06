import matplotlib.pyplot as plt
import numpy as np

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

#### L'objectif est de trouver une alternative à notre fonction sous_ensemble pour ne pas avoir à tracer les k parmi n courbes et ainsi 
### diminué la complexité de manière conséquente 

## on peut trier notre liste de cas dans l'ordre décroissant sur le critère des probabilité de gain puis par gain 
## on évalue ensuite ceux qui se trouvent dans les k premières positions de chacune des deux listes : ces gens sont très intéressants ils rapportent beaucoup et ont de grandes chances d'être fraudeurs 

def tri(cas = cas) : 
    return (sorted(cas, key=lambda x: x[0], reverse = True), sorted(cas, key=lambda x:x[1], reverse = True)) 

tri_gain, tri_proba = tri()

## on identifie les gens dangereux : 

def dangereux() :
    danger = [] 
    tri1 = tri_gain[:k]
    tri2 = tri_proba[:k]
    for cas in tri1 : 
        if cas in tri2 : 
            danger.append(cas)

    ## on retire les gens dangereux : ils seront traités 
    for cas in danger : 
        tri_gain.remove(cas)
        tri_proba.remove(cas)
    
    return danger



## on va chercher mtn à retirer les cas qui ne sont de toute façon pas intéressant

def negligeable(w) : 

    negligeable = [] 
    v = len(tri_gain)
    tri1 = tri_gain[v-w:v]
    tri2 = tri_proba[v-w:v]
    for cas in tri1 : 
        if cas in tri2 : 
            negligeable.append(cas)
    
    ## on retire les cas négligeables : ils ne seront pas traités 
    for cas in negligeable : 
        tri_gain.remove(cas)
        tri_proba.remove(cas)
    
    return negligeable

    

def nouveau() : 
    danger = dangereux()
    k_new = k - len(danger)
    neg = negligeable(k_new)
    n = len(tri_gain)
    return danger, neg, tri_gain, n, k_new



