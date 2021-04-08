from affectation import repartition_difficult, dangerosite, difficult



# on veut pouvoir écrire un algo qui étant donné une liste de cas, une liste d'équipes de vérificateurs, nous donne : 
# - dictionnaire des cas à traiter {Monsieur A : [id, salaire, patrimoine, proba_de_fraude, cat_socio_pro]}
# - 
# - l'affectation au personnel des équipes de ces différents cas 
# - un détail des diffrentes statistiques sur ces cas 

# Nos entrées : 

    ###Le dictionnaire de nos cas à traiter

liste_cas = { "Mister_1" : [1, 100000, 100000, 0.95, 1],
                "Mister_2" : [2, 200000, 100000, 0.85, 2],
                "Mister_3" : [3, 100000, 200000, 0.75, 1],
                "Mister_4" : [4, 100000, 10000, 0.65, 2],
                "Mister_5" : [5, 10000, 100000, 0.55, 1],
                "Mister_6" : [6, 150000, 100000, 0.45, 2],
                "Mister_7" : [7, 100000, 150000, 0.35, 1],
                "Mister_8" : [8, 1000, 1000, 0.25, 2],
                "Mister_9": [9, 10000000, 10000, 0.15, 1],
                "Mister_10" : [10, 10000, 10000000, 0.05, 2],
                "Mister_11": [11, 10000, 10000, 0.5, 1],
            }

    ### Nos équipes de vérificateurs : équipes = { "team" : [(id_1, experience), (id_2, experience)]}, 1 <= experience <= 3

Equipes = {"equipe 1" : [(11, 3), (12, 1)],
            "equipe 2" : [(21, 2), (22, 2)]
            }

équipes = [[(11, 3), (12, 1)],
            [(21, 2), (22, 2)]]
    ### on définit la fonction qui nous donne l'ensemble des entréres du problème

def entree() : 
    return liste_cas, équipes

    ### on définit la fonction qui nous donne le choix des équipes. La fontction retourne un sous-dicionnaire de liste_cas. 

def choix_des_cas(liste = liste_cas) : 
    

    return liste



    ### on définit la fonction qui nous donne la répartition des équipes 

def repartition(cas = choix_des_cas(), teams = équipes) : 

    repartitions = { ekip : {verif : [] for verif in Equipes[ekip]} for ekip in Equipes}
    
    # On a un dictionaire cas qu'on veut transformer en une liste pour utiliser la fonction repartition_difficult
    fraude = [[cas[mister][0], dangerosite(cas[mister]), difficult(cas[mister])] for mister in cas]
    Affectations = repartition_difficult(teams, fraude, 2, 3)

    # On donne à chaque verificateur une liste de personne, ça ne doit pas être trop dur en sql  : 
    """repartitions ... """
            

    return Affectations

print(repartition())

    ### on définit une fonction qui nous donnera les résultats 

def statistiques() : 

    return 