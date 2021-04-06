from math import *
import random
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

def dangerosite(cat_socio_pro, fraudeur):
    return probabilite(fraudeur)*indice_dangerosite(cat_socio_pro,fraudeur)



# Equipes contient la liste des équipes de détection de fraude. Chaque vérificateur devrait faire 10 contrôles
# Chaque équipe est une liste de couples : [id_verif : exprience] 
# Fraudes est une liste de couples [fraudeur, dangerosité]




def repartition_fraudes(equipes, fraudes):
    liste_fraudes = fraudes.sort(key = lambda x:x[1])
    cardinal_equipe = len(equipes[0]) #On considère que les équipes ont toutes le même cardinal
    equipes = [e.sort(key = lambda x:x[1]) for e in equipes] # On trie les équipes par ordre croissant d'expérience
    Affectations = {}

    for k in range(cardinal_equipe) :
        for j in range(10): #Chaque vérificateur fait 10 checks
            for e in equipes :
                
                id_verif = e[-k-1][0]
                
                if id_verif not in Affectations :
                    Affectations[id_verif] = [liste_fraudes.pop[-1]]
                else :
                    Affectations[id_verif].append(liste_fraudes.pop[-1])
    
    return Affectations