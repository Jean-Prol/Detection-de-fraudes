import matplotlib.pyplot as plt
import numpy as np
from affectation import dangerosite



### on étudie n cas de fraudes dont les données seraient pour chaque cas : (gain_potentiel, probabilité de fraude) où la probabilité serait obtenu 
# grâce à l'algo 
### On considère qu'on ne peut traiter que k < n cas 

### On veut une liste de cas de la forme [(gain, proba, id)]

def cas(liste) : 
    cas = []
    for mister in liste : 
        cas.append((liste[mister][2]*dangerosite(liste[mister], liste), liste[mister][3], liste[mister][0]))
    return cas


### L'objectif est de trouver une alternative à notre fonction sous_ensemble pour ne pas avoir à tracer les k parmi n courbes et ainsi 
### diminué la complexité de manière conséquente 

## on peut trier notre liste de cas dans l'ordre décroissant sur le critère des probabilité de gain puis sur le crtière du gain 
## on évalue ensuite ceux qui se trouvent dans les k premières positions de chacune des deux listes : ces gens sont très intéressants ils rapportent beaucoup et ont de grandes chances d'être fraudeurs 

def tri(cas) : 
    return (sorted(cas, key=lambda x: x[0], reverse = True), sorted(cas, key=lambda x:x[1], reverse = True)) 


## on identifie les gens dangereux : 

def dangereux(tri_gain, tri_proba, k) :
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

def negligeable(w, tri_gain, tri_proba) : 

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

    

def nouveau(liste, k) : 
    tri_gain, tri_proba = tri(cas(liste))
    danger = dangereux(tri_gain, tri_proba, k)
    k_new = k - len(danger)
    neg = negligeable(k_new, tri_gain, tri_proba)
    n = len(tri_gain)
    return danger, neg, tri_gain, n, k_new





