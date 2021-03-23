from math import *
import numpy as np



# On représente les différentes données par une liste L=[Salaire,Patrimoine,...]
# Chaque liste comporte les données de la catégories socio-professionnelle : Salaire = [S1,S2...]

# On note p la proba de fraude
# Toutes les données sont stockées dans un tableau Donnee

# Donnee est un dictionnaire comportant pour chaque catégorie socio-pro, la liste des valeurs individuelles pour chaque donnée

def indice_dangerosite(cat_socio_pro, fraudeur):
    L = Donnee[cat_socio_pro]
    F = fraudeur 
    Moyennes = [np.mean(d) for d in L]
    Ecart_type = [np.std(d) for d in L]
    res = [abs((F[i]-Moyennes[i])/Ecart_type[i]) for i in range(len(F))]
    return (2/np.pi)*np.atan(max(res))

