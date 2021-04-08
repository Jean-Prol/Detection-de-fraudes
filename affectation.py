from math import *
import random
import numpy as np


# On représente une personne par une liste [salaire, patrimoine, cat_socio_pro, proba_fraude]
# On représente les différentes données par une liste L=[Salaire,Patrimoine,...]
# Chaque liste comporte les données de la catégories socio-professionnelle : Salaire = [S1,S2...]

# On note p la proba de fraude
# Toutes les données sont stockées dans un tableau Donnee

# Donnee est un dictionnaire comportant pour chaque catégorie socio-pro, la liste des valeurs individuelles pour chaque donnée

# On définit des fonctions qui nous seront utiles

def salaire(fraudeur) : 
    return fraudeur[1]

def patrimoine(fraudeur) : 
    return fraudeur[2]

def cat_socio(fraudeur) : 
    return fraudeur[4]

def probabilite(fraudeur) : 
    return fraudeur[3]

# Définition de l'indice de dangérosité

def indice_dangerosite(fraudeur):
    """L = Donnee[cat_socio(fraudeur)]
    F = fraudeur 
    Moyennes = [np.mean(d) for d in L]
    Ecart_type = [np.std(d) for d in L]
    res = [abs((F[i]-Moyennes[i])/Ecart_type[i]) for i in range(len(F))]
    return (2/np.pi)*np.arctan(max(res))"""
    return 1 
     

# définition de la dangerosité

def dangerosite(fraudeur):
    return probabilite(fraudeur)*indice_dangerosite(fraudeur)

# On cherche à mesurer la difficulté d'un cas à traiter, ici simplement en terme de niveau de difficulté
# les paramètres pouvant influer sont : la probabilité de fraude, le patrimoine, le salaire, (les indicateurs)

def difficult(fraudeur) : 
    p = probabilite(fraudeur)
    pat = patrimoine(fraudeur)
    rev = salaire(fraudeur)
    def f(x) : 
        return 20*(x*x - x + 0.3)
    indice = pat * rev / f(p) # on considère que plus la proba est proche de 0.5 plus le dossier est délicat (forte incertitude)
    return (2/np.pi)*np.arctan(indice/(100000*100000)) # on divise par 100 000 * 100 000 pour "normaliser" par un produit salaire-patrioine moyen 



# On peut estimer le temps que prendra la vérification en fonction de la difficulté et de l'expérience. 
# les paramètres pouvant influer sont : la probabilité de fraude, le patrimoine, les revenus, les indicateurs mais en plus l'expérience du vérificateur

def time(fraudeur, id_verif, equipe) : 
    indice = difficult(fraudeur)/equipe[id_verif][1]
    return (2/np.pi)*np.arctan(indice)


# Equipes contient la liste des équipes de détection de fraude. Chaque vérificateur devrait faire 10 contrôles
# Chaque équipe est une liste de couples : [id_verif : exprience] 
# Fraudes est une liste de couples [fraudeur, dangerosité, difficulté]



### Nous allons essayer une nouvelle façon de répartir les tâches : ici, nous allons prendre en compte la difficulté et le temps en plus de 
### la dangerosité. Dans une première approximation, nous pouvons considérer que le temps pris pour une tâche ne dépend pas de l'expérience de la 
### personne mais dépend seulement de la difficulté. Ainsi, chaque personne a une capacité maximale de traitement. 

# On considère que chaque personne a une capcité de difficulté maximale

"""charge_max = 5
cardinal_equipe = 10 #On considère que les équipes ont toutes le même cardinal"""


def repartition_difficult(equipes, fraudes, cardinal_equipe = 10, charge_max = 5) : #charge_max à 5 : totalement arbitraire
    fraudes.sort(key = lambda x:x[1])
    for e in equipes : 
        e.sort(key = lambda x: x[1], reverse = True)    # On trie les équipes par ordre décroissant d'expérience
    Affectations = {}

    for k in range(cardinal_equipe) : 
        lnext = [e[k][0] for e in equipes] # on prend les k eme plus expérimentés éléments de chaque équipe
        while len(lnext) > 0 and len(fraudes) > 0 :
            for e in equipes : 

                if e[k][0] in lnext and len(fraudes) > 0 : 

                    id_verif = e[k][0] 

                    if id_verif not in Affectations : 
                        case = fraudes.pop()
                        Affectations[id_verif] = ([case], case[2])  # on affecte à une personne un cas et une charge de travail
            
                    else : 
                        
                        # on va chercher à savoir si le vérificateur a encore une capacité suffisante de travail et on lui attribue le cas le plus 
                        # dangereux possible
                        
                        d = len(fraudes)
                        a = d-1
                        cap = charge_max - Affectations[id_verif][1]
                        while a >= 0 and fraudes[a][2] > cap : 
                            a -= 1                         
                        if a >= 0 : 
                            case = fraudes.pop(a)
                            Affectations[id_verif] = (Affectations[id_verif][0] + [case], Affectations[id_verif][1] + case[2])
                        else : 
                            lnext.remove(id_verif)
       
    return Affectations

