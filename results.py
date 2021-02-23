import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import TextBox
import pandas as pd

res_3 = pd.read_csv("/Users/jeanprolhac/Desktop/Projet/Projet 16 - IA et fraude/Detection-de-fraudes/res_3.tsv", sep="\t")
res_4 = pd.read_csv("/Users/jeanprolhac/Desktop/Projet/Projet 16 - IA et fraude/Detection-de-fraudes/res_4.tsv", sep="\t")
res_5 = pd.read_csv("/Users/jeanprolhac/Desktop/Projet/Projet 16 - IA et fraude/Detection-de-fraudes/res_5.tsv", sep="\t")

data_3 = res_3.loc[0:26]
data_3_cat = list(data_3["Epoch"])
data_3_sal = list(data_3["Indicateur"])
data_3_dep = list(data_3["Temps"])
data_3_pat = list(data_3["Accuracy"])
data_4 = res_4.loc[0:26]
data_4_cat = list(data_4["Epoch"])
data_4_sal = list(data_4["Indicateur"])
data_4_dep = list(data_4["Temps"])
data_4_pat = list(data_4["Accuracy"])
data_5 = res_5.loc[0:26]
data_5_cat = list(data_5["Epoch"])
data_5_sal = list(data_5["Indicateur"])
data_5_dep = list(data_5["Temps"])
data_5_pat = list(data_5["Accuracy"])

def affichage(indicateur):
    E = [1, 2, 3, 4, 5]
    T3 = []
    A3 = []
    T4 = []
    A4 = []
    T5 = []
    A5 = []
    k = 3 + indicateur
    for i in range(1,6):
        T3.append(data_3_dep[k])
        A3.append(data_3_pat[k])
        T4.append(data_4_dep[k])           
        A4.append(data_4_pat[k])
        T5.append(data_5_dep[k])
        A5.append(data_5_pat[k])  
        k += 4
    fig, ax = plt.subplots()
    ax1 = plt.subplot(121)
    ax1.plot(E, T3, label="3 couches")
    ax1.plot(E, T4, label="4 couches")
    ax1.plot(E, T5, label="5 couches")
    ax2 = plt.subplot(122)
    ax2.plot(T3, A3, label="3 couches")
    ax2.plot(T4, A4, label="4 couches")
    ax2.plot(T5, A5, label="5 couches")
    plt.show()

def affichage2(indicateur):
    X = [3,4,5]
    Y = [data_3_pat[3+indicateur], data_4_pat[3+indicateur], data_5_pat[3+indicateur]]
    plt.plot(X,Y)
    plt.show()

affichage2(4)