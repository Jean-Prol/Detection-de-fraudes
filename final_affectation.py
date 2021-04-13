from affectation import repartition_difficult, dangerosite, difficult
from optimisation_2 import nouveau 
"""from optimisation import * """
from tkinter import *


# on veut pouvoir écrire un algo qui étant donné une liste de cas, une liste d'équipes de vérificateurs, nous donne : 
# - dictionnaire des cas à traiter {Monsieur A : [id, salaire, patrimoine, proba_de_fraude, cat_socio_pro]}
# - le nombre de cas que l'on veut traiter (de manière raisonable)
# - le type d'affectation que l'on veut
# - l'affectation au personnel des équipes de ces différents cas 
# - un détail des diffrentes statistiques sur ces cas 

# Nos entrées : 

    ###Le dictionnaire de nos cas à traiter

#nb_cas = int(float(entrée1.get()))


liste_cas = { "Mister_1" : [1, 100000, 100000, 0.95, 1],
                "Mister_2" : [2, 200000, 100000, 0.85, 2],
                "Mister_3" : [3, 100000, 200000, 0.75, 1],
                "Mister_4" : [4, 100000, 10000, 0.65, 2],
                "Mister_5" : [5, 10000, 100000, 0.55, 1],
                "Mister_6" : [6, 150000, 100000, 0.45, 2],
                "Mister_7" : [7, 100000, 150000, 0.35, 1],
                "Mister_8" : [8, 1000, 1000, 0.25, 2],
                "Mister_9" : [9, 10000000, 10000, 0.15, 1],
                "Mister_10" : [10, 10000, 10000000, 0.05, 2],
                "Mister_11": [11, 10000, 10000, 0.5, 1],
            }

    ### Nos équipes de vérificateurs : équipes = { "team" : [(id_1, experience), (id_2, experience)]}, 1 <= experience <= 3

Equipes = {"equipe 1" : [(11, 3), (12, 1)],
            "equipe 2" : [(21, 2), (22, 2)]
            }

équipes = [[(11, 3), (12, 1)],
            [(21, 2), (22, 2)]]
    ### on définit la fonction qui nous donne l'ensemble des entréres du problème : liste des cas, équipes, nb de cas à traiter, 
    ### montant visé, taux de réussite minimal espérer 

def entree(ent1, ent2, ent3) : 
    return liste_cas, équipes, int(float(ent1.get())), int(float(ent2.get())), int(float(ent3.get()))/100

    ### on définit la fonction qui nous donne le choix des équipes. La fontction retourne un sous-dicionnaire de liste_cas et une 
    ### chaîne de caractère qui liste les dangers pour le moement

def choix_des_cas(liste = liste_cas, k = len(liste_cas)) : 
    danger = nouveau(liste, k)[0]
    sous_dico = {}
    txt = ""
    for cas in danger : 
        txt += str(cas[2])+ ", "

    # on reconstruit le sous-dico de liste_cas dont nous avons besoin
    for cas in danger : 
        id = cas[2]
        for case in liste_cas : 
            if liste_cas[case][0] == id : 
                sous_dico[case] = liste_cas[case]
            
    return sous_dico, txt



    ### on définit la fonction qui nous donne la répartition des équipes 

def repartition(cas = choix_des_cas()[0], teams = équipes) : 

    repartitions = { ekip : {verif : [] for verif in Equipes[ekip]} for ekip in Equipes}
    
    # On a un dictionaire cas qu'on veut transformer en une liste pour utiliser la fonction repartition_difficult
    fraude = [[cas[mister][0], dangerosite(cas[mister]), difficult(cas[mister])] for mister in cas]
    Affectations = repartition_difficult(teams, fraude, 2, 1)

    # On donne à chaque verificateur une liste de personne, ça ne doit pas être trop dur en sql  : 
    """repartitions ... """
            

    return Affectations


    ### on définit une fonction qui nous donnera les résultats 

def statistiques() : 

    return 





### AFFICHAGE 

# fonctions 

def changeText() : 

    # récupération des entrées : 
    nb_entree = entrée1.get()
    nb_target = entrée2.get()
    nb_ent = int(float(nb_entree))
    nb_target = int(float(nb_target))

    # ouverture d'une nouvelle fenêtre
    fenetre_2 = Tk()
    fenetre_2.geometry('500x500')

    # Ajout d'un texte dans la fenêtre pour rien pour le moment :
    blabla = choix_des_cas(liste_cas, nb_ent)[1]
    texte3 = Label (fenetre_2, text = "Les identifiants des personnes les plus dangereuses sont : "+blabla)
    texte3.pack()    

    # Ajout d'un texte dans la fenêtre pour rien pour le moment :
    Affectations = repartition(choix_des_cas(liste_cas, nb_ent)[0], équipes)
    final = ""
    for affectation in Affectations : 
        final += "\n"+str(affectation)+" : "
        for case in Affectations[affectation][0]:
            final += str(case[0])+ " "
    texte4 = Label (fenetre_2, text = "La répartition se fera de la manière suivante : "+final)
    texte4.pack() 

    # Affichage de la fenêtre créée :
    fenetre_2.mainloop()





# ouverture de la fenêtre
fenetre = Tk()
fenetre.geometry('500x500')

# Ajout d'un texte dans la fenêtre pour indiquer le nombre de cas à traiter :
nb = str(len(liste_cas))
texte1 = Label (fenetre, text = "Nous avons au total "+nb+" cas à traiter actuellement")
texte1.pack()

# Ajout d'un texte dans la fenêtre pour demander le nombre de cas à traiter :
texte1 = Label (fenetre, text = "Indiquez le nombre de cas que vous souhaitez traiter :")
texte1.pack()

# Création d'un champ de saisie de l'utilisateur dans la fenêtre pour saisir le nombre de cas souhaité :

def verifie(*args):
    entry = entrée1.get().strip()
    entry_2 = entrée2.get().strip()
    entry_3 = entrée3.get().strip()

    if entry.isdigit() and entry_2.isdigit() and int(float(entry)) <= int(float(nb)) and int(float(entry_2)) <= montant(liste_cas) and entry_3.isdigit() and int(float(entry_3)) <= 100:
        label.configure(text='')
        bouton1.configure(state="active")
    elif entry.isdigit() and  int(float(entry)) <= int(float(nb)) : 
        label.configure(text = '')
    elif entry.isdigit() and int(float(entry)) > int(float(nb)):
        label.configure(text="Vous ne pouvez pas traiter autant de cas")
        bouton1.configure(state="disabled")
    elif not entry.isdigit():
        label.configure(text="Renseignez un nombre svp")
        bouton1.configure(state="disabled")       

entry_var = StringVar("")
entry_var.trace('w', verifie)
entrée1 = Entry (fenetre, textvariable = entry_var)
entrée1.pack()
label = Label(fenetre, text="", foreground="red")
label.pack()

# Ajout d'un texte dans la fenêtre pour demander la façon dont on veut répartir les cas :
texte2 = Label (fenetre, text = "Indiquez la manière dont vous souhaitez répartir les cas à vos équipes")
texte2.pack()

# Création des cases à cocher dans la fenêtre pour choisir la manière de répartir les cas :

def active_function(index):
    if case_var[index][1].get()==0:
        reset_bouton()
    else:
        for i in range(len(case_var)):
            if i!= index:
                case_var[i][0].configure(state="disabled")

def reset_bouton():
    for i in range(len(case_var)):
        case_var[i][0].configure(state="active")
        case_var[i][1].set(0)

case_var1 = IntVar()
case_var2 = IntVar()
case_var3 = IntVar()
case_cocher1 = Checkbutton (fenetre, text = "équilibrée", variable = case_var1, command = lambda:active_function((0)))
case_cocher2 = Checkbutton (fenetre, text = "optimisée", variable = case_var2, command = lambda:active_function((1)))
case_cocher3 = Checkbutton (fenetre, text = "hybride", variable = case_var3, command = lambda:active_function((2)))
case_cocher1.pack()
case_cocher2.pack()
case_cocher3.pack()
case_var = [[case_cocher1, case_var1], [case_cocher2, case_var2], [case_cocher3, case_var3]]

# Ajout d'un texte dans la fenêtre pour annoncer le montant maximal possible :
def montant(l) : 
    S = 0
    for mister in l : 
        S += liste_cas[mister][2]*dangerosite(liste_cas[mister])
    
    return S

montant_max = str(montant(liste_cas))
texte1 = Label (fenetre, text = "\nLe montant maximal estimé à récupérer est de "+montant_max+" €")
texte1.pack()

# Ajout d'un texte dans la fenêtre pour demander le montant minimal objectif de l'équipe :
texte1 = Label (fenetre, text = "Saisissez le montant objectif de votre équipe :")
texte1.pack()

# Création d'un champ de saisie de l'utilisateur dans la fenêtre pour saisir le montant objectif souhaiter :
def verifie_2(*args):
    entry = entrée1.get().strip()
    entry_2 = entrée2.get().strip()
    entry_3 = entrée3.get().strip()

    if entry.isdigit() and entry_2.isdigit() and int(float(entry_2)) <= montant(liste_cas) and int(float(entry)) <= int(float(nb)) and entry_3.isdigit() and int(float(entry_3)) <= 100:
        label_2.configure(text='')
        bouton1.configure(state="active")
    elif entry_2.isdigit() and int(float(entry_2)) <= montant(liste_cas) : 
        label_2.configure(text='')
    elif entry_2.isdigit() and int(float(entry_2)) > montant(liste_cas) : 
        label_2.configure(text="Renseignez un montant inférieur au montant maximal svp")
        bouton1.configure(state="disabled")    
    elif not entry_2.isdigit():
        label_2.configure(text="Renseignez un nombre svp")
        bouton1.configure(state="disabled")       

entry_var_2 = StringVar("")
entry_var_2.trace('w', verifie_2)
entrée2 = Entry (fenetre, textvariable = entry_var_2)
entrée2.pack()
label_2 = Label(fenetre, text="", foreground="red")
label_2.pack()

# Ajout d'un texte dans la fenêtre pour demander le taux de réussite minimum souhaité :
texte1 = Label (fenetre, text = "Saisissez le  taux de réussite minimum souhaité par vos équipes :")
texte1.pack()

# Création d'un champ de saisie de l'utilisateur dans la fenêtre pour donner un taux de réussite minimum souhaité :
def verifie_3(*args):
    entry = entrée1.get().strip()
    entry_2 = entrée2.get().strip()
    entry_3 = entrée3.get().strip()

    if entry.isdigit() and entry_2.isdigit() and entry_3.isdigit() and int(float(entry_3)) <= 100 and int(float(entry_2)) <= montant(liste_cas) and int(float(entry)) <= int(float(nb)):
        label_3.configure(text='')
        bouton1.configure(state="active")
    elif entry_3.isdigit() and int(float(entry_3)) <= 100 : 
        label_3.configure(text='') 
    elif entry_2.isdigit() and int(float(entry_2)) > 100 : 
        label_3.configure(text="Renseignez un taux inférieur à 100% svp")
        bouton1.configure(state="disabled")    
    elif not entry_2.isdigit():
        label_3.configure(text="Renseignez un nombre svp")
        bouton1.configure(state="disabled")       

entry_var_3 = StringVar("")
entry_var_3.trace('w', verifie_3)
entrée3 = Entry (fenetre, textvariable = entry_var_3)
entrée3.pack()
label_3 = Label(fenetre, text="", foreground="red")
label_3.pack()

# Ajout d'un bouton dans la fenêtre :
bouton1 = Button (fenetre, text = "Valider mes choix", command=lambda: changeText())
bouton1.pack()
bouton1.configure(state='disabled')



# Affichage de la fenêtre créée :
fenetre.mainloop()