import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
from matplotlib.widgets import TextBox
import pandas as pd
import math 
import numpy as np

class AnnoteFinder(object):
    """callback for matplotlib to display an annotation when points are
    clicked on.  The point which is closest to the click and within
    xtol and ytol is identified.
    
    Register this function like this:
    
    scatter(xdata, ydata)
    af = AnnoteFinder(xdata, ydata, annotes)
    connect('button_press_event', af)
    """

    def __init__(self, xdata, ydata, annotes, ax=None, xtol=None, ytol=None):
        self.data = list(zip(xdata, ydata, annotes))
        if xtol is None:
            xtol = ((max(xdata) - min(xdata))/float(len(xdata)))/2
        if ytol is None:
            ytol = ((max(ydata) - min(ydata))/float(len(ydata)))/2
        self.xtol = xtol
        self.ytol = ytol
        if ax is None:
            self.ax = plt.gca()
        else:
            self.ax = ax
        self.drawnAnnotations = {}
        self.links = []

    def distance(self, x1, x2, y1, y2):
        """
        return the distance between two points
        """
        return(math.sqrt((x1 - x2)**2 + (y1 - y2)**2))

    def __call__(self, event):

        if event.inaxes:

            clickX = event.xdata
            clickY = event.ydata
            if (self.ax is None) or (self.ax is event.inaxes):
                annotes = []
                # print(event.xdata, event.ydata)
                for x, y, a in self.data:
                    # print(x, y, a)
                    if ((clickX-self.xtol < x < clickX+self.xtol) and
                            (clickY-self.ytol < y < clickY+self.ytol)):
                        annotes.append(
                            (self.distance(x, clickX, y, clickY), x, y, a))
                if annotes:
                    annotes.sort()
                    distance, x, y, annote = annotes[0]
                    self.drawAnnote(event.inaxes, x, y, annote)
                    for l in self.links:
                        l.drawSpecificAnnote(annote)

    def drawAnnote(self, ax, x, y, annote):
        """
        Draw the annotation on the plot
        """
        if (x, y) in self.drawnAnnotations:
            markers = self.drawnAnnotations[(x, y)]
            for m in markers:
                m.set_visible(not m.get_visible())
            self.ax.figure.canvas.draw_idle()
        else:
            t = ax.text(x, y, " - %s" % (annote),)
            m = ax.scatter([x], [y], marker='d', c='r', zorder=100)
            self.drawnAnnotations[(x, y)] = (t, m)
            self.ax.figure.canvas.draw_idle()

    def drawSpecificAnnote(self, annote):
        annotesToDraw = [(x, y, a) for x, y, a in self.data if a == annote]
        for x, y, a in annotesToDraw:
            self.drawAnnote(self.ax, x, y, a)

def linkAnnotationFinders(afs):
        for i in range(len(afs)):
            allButSelfAfs = afs[:i]+afs[i+1:]
            afs[i].links.extend(allButSelfAfs)

cat_list = ["cadre", "profession intermédiaire", "employé", "ouvrier", "chef d'entreprise", "agriculteur"]

database = pd.read_csv("/Users/jeanprolhac/Desktop/Projet/Projet 16 - IA et fraude/Detection-de-fraudes/new_data_big.tsv", sep="\t")

data = database.loc[0:5972]
data_cat = list(data["catégorie"])
data_sal = list(data["salaire"])
data_dep = list(data["dépenses"])
data_pat = list(data["patrimoine"])

data_catm=[[],[],[],[],[],[]]

for i in range(len(data_cat)):
    elem=data_cat[i]
    if elem==0:
        data_catm[0].append(i)
    elif elem==1:
        data_catm[1].append(i)
    elif elem==2:
        data_catm[2].append(i)
    elif elem==3:
        data_catm[3].append(i)
    elif elem==4:
        data_catm[4].append(i)
    else:
        data_catm[5].append(i)

def affichage_indicateur1(cat):
    X = [data_sal[i] for i in data_catm[cat]]
    Y = [data_pat[i] for i in data_catm[cat]]
    Z = [data_dep[i] for i in data_catm[cat]]
    M=[i for i in range(int(min(X)), int(max(X))+1)]
    moy_X = sum(X)/len(X)
    moy_Y = sum(Y)/len(Y)
    fig, ax = plt.subplots()
    ax1=plt.subplot(121)
    ax1.scatter([moy_X for _ in range(int(min(Y)), int(max(Y)+1))], [i for i in range(int(min(Y)), int(max(Y))+1)], label="Salaire moyen")
    ax1.scatter(M, [moy_Y for _ in range(int(min(X)), int(max(X))+1)], label="Patrimoine moyen")
    ax1.scatter(X, Y)
    ax1.scatter(M, [(max(Y)-((max(Y)-moy_Y)/10)-moy_Y)/(max(X)-min(X))*(i-min(X))+ moy_Y for i in range(int(min(X)), int(max(X))+1)], label="Ratio limite")
    ax1.set_xlabel("Salaire")
    ax1.set_ylabel("Patrimoine")
    ax1.legend()
    af1 = AnnoteFinder(X,Y,data_catm[cat], xtol=1000, ytol=1000)
    fig.canvas.mpl_connect('button_press_event', af1)
    ax2=plt.subplot(122)
    ax2.scatter(M,M, label="Salaire = Dépenses")
    ax2.scatter(X, Z)
    ax2.set_xlabel("Salaire")
    ax2.set_ylabel("Dépenses")
    ax2.legend()
    af2 = AnnoteFinder(X,Z,data_catm[cat], xtol=1000, ytol=1000)
    fig.canvas.mpl_connect('button_press_event', af2)
    linkAnnotationFinders([af1, af2])
    fig.suptitle("Catégorie socio-professionnelle : {} – Indicateur 1".format(cat_list[cat]))
    plt.show()

#affichage_indicateur1(1)

## Premier critère : on sélectionne les personnes qui ont un patrimoine élevé par rapport à la moyenne, 
## (au-dessus de la ligne rouge) tout en dépensant plus que ce qu'elles gagnent !

def clusterise_indicateur1(cat):
    X = [data_sal[i] for i in data_catm[cat]]
    Y = [data_pat[i] for i in data_catm[cat]]
    Z = [data_dep[i] for i in data_catm[cat]]
    moy_X = sum(X)/len(X)
    moy_Y = sum(Y)/len(Y)
    i_val = []
    for i in range(len(X)):
        if Y[i]>=(max(Y)-((max(Y)-moy_Y)/10)-moy_Y)/(max(X)-min(X))*(X[i]-min(X))+ moy_Y:
            if Z[i]>=X[i]:
                i_val.append(i)
    fig, ax = plt.subplots()
    ax1 = plt.subplot(121)
    ax2 = plt.subplot(122)
    ax1.scatter(X,Y,label="Non fraudeur")
    ax1.scatter([X[i] for i in i_val], [Y[i] for i in i_val], label="Fraudeur")
    ax1.set_xlabel("Salaire")
    ax1.set_ylabel("Patrimoine")
    ax1.legend()
    ax2.scatter(X,Z,label="Non fraudeur")
    ax2.scatter([X[i] for i in i_val], [Z[i] for i in i_val], label="Fraudeur")
    ax2.set_xlabel("Salaire")
    ax2.set_ylabel("Dépenses")
    axprev = plt.axes([0.53, 0.02, 0.14, 0.04])
    TextBox(axprev, '', initial="{}/{} fraudeurs ({}%)".format(len(i_val), len(X), int(100*len(i_val)/len(X))))
    ax2.legend()
    fig.suptitle("Catégorie socio-professionnelle : {} – Indicateur 1".format(cat_list[cat]))
    plt.show()

#clusterise_indicateur1(3)

## Deuxième critère : on sélectionne les personnes qui dépensent plus que la moyenne

def affichage_indicateur23(cat):
    X = [data_sal[i] for i in data_catm[cat]]
    Y = [data_pat[i] for i in data_catm[cat]]
    Z = [data_dep[i] for i in data_catm[cat]]
    N = [Z[i]-X[i] for i in range(len(X))]
    P = [i for i in range(len(X))]
    M = [i for i in range(int(min(X)), int(max(X))+1)]
    moy_X = sum(X)/len(X)
    moy_Y = sum(Y)/len(Y)
    moy_N = sum(N)/len(N)
    quant = np.quantile(N,0.85)
    quant2 = np.quantile(Y, 0.15)
    print(quant)
    fig, ax = plt.subplots()
    ax1 = plt.subplot(222)
    ax1.scatter(P, N)
    ax1.scatter(P, [moy_N for _ in range(len(X))], label="Écart moyen")
    if moy_N<0:
        ax1.scatter(P, [moy_N+0.35*(max(N)+moy_N) for _ in range(len(X))], label="Écart max - 1.35*écart moyen")
    ax1.scatter(P, [quant for _ in range(len(X))], label="85ème centile")
    af1 = AnnoteFinder(P,N,data_catm[cat], xtol=50, ytol=50)
    ax1.set_xlabel("n° de dossier")
    ax1.set_ylabel("Dépenses - Salaire")
    ax1.legend()
    fig.canvas.mpl_connect('button_press_event', af1)
    ax2 = plt.subplot(121)
    ax2.scatter([moy_X for _ in range(int(min(Y)), int(max(Y)+1))], [i for i in range(int(min(Y)), int(max(Y))+1)], label="Salaire moyen")
    ax2.scatter(M, [moy_Y for _ in range(int(min(X)), int(max(X))+1)], label="Patrimoine moyen")
    ax2.scatter(X, Y)
    ax2.scatter(M, [moy_Y-0.35*(moy_Y-min(Y)) for _ in range(int(min(X)), int(max(X))+1)], label="Écart min + 0.65*écart moyen")
    ax2.scatter(M, [quant2 for _ in range(int(min(X)), int(max(X))+1)], label="15ème centile")
    ax2.set_xlabel("Salaire")
    ax2.set_ylabel("Patrimoine")
    ax2.legend()
    af2 = AnnoteFinder(X,Y,data_catm[cat], xtol=1000, ytol=1000)
    fig.canvas.mpl_connect('button_press_event', af2)
    ax3 = plt.subplot(224)
    ax3.scatter(M,M, label="Salaire = Dépenses")
    ax3.scatter(X, Z)
    ax3.set_xlabel("Salaire")
    ax3.set_ylabel("Dépenses")
    ax3.legend()
    af3 = AnnoteFinder(X,Z,data_catm[cat], xtol=1000, ytol=1000)
    fig.canvas.mpl_connect('button_press_event', af3)
    linkAnnotationFinders([af1, af2, af3])
    fig.suptitle("Catégorie socio-professionnelle : {} – Indicateurs 2 et 3".format(cat_list[cat]))
    plt.show()

#affichage_indicateur23(4)

def clusterise_indicateur23(cat):
    X = [data_sal[i] for i in data_catm[cat]]
    Y = [data_pat[i] for i in data_catm[cat]]
    Z = [data_dep[i] for i in data_catm[cat]]
    N = [Z[i]-X[i] for i in range(len(X))]
    P = [i for i in range(len(X))]
    M = [i for i in range(int(min(X)), int(max(X)+1))]
    moy_X = sum(X)/len(X)
    moy_Y = sum(Y)/len(Y)
    moy_N = sum(N)/len(N)
    quant = np.quantile(N,0.8)
    quant2 = np.quantile(Y, 0.2)
    i_val = []
    i_val2 = []
    for i in range(len(X)):
        if N[i]>moy_N+0.35*(max(N)+moy_N) and N[i]>0:
            if Y[i]<moy_Y-0.35*(moy_Y-min(Y)):
                i_val.append(i)
        if N[i]>quant and N[i]>0:
            if Y[i]<quant2:
                i_val2.append(i)
    fig, ax = plt.subplots()
    ax1 = plt.subplot(221)
    ax1.set_xlabel("Salaire")
    ax1.set_ylabel("Patrimoine")
    ax1.scatter(X,Y, label="Non fraudeur")
    ax1.scatter([X[i] for i in i_val], [Y[i] for i in i_val], label="Fraudeur")
    ax1.title.set_text("Indicateur 2")
    ax1.legend()
    ax2 = plt.subplot(223)
    ax2.set_xlabel("Salaire")
    ax2.set_ylabel("Dépenses")
    ax2.scatter(X,Z, label="Non fraudeur")
    ax2.scatter([X[i] for i in i_val], [Z[i] for i in i_val], label="Fraudeur")
    axprev1 = plt.axes([0.1, 0.02, 0.14, 0.04])
    TextBox(axprev1, '', initial="{}/{} fraudeurs ({}%)".format(len(i_val), len(X), int(100*len(i_val)/len(X))))
    ax2.legend()
    ax3 = plt.subplot(222)
    ax3.set_xlabel("Salaire")
    ax3.set_ylabel("Patrimoine")
    ax3.scatter(X,Y, label="Non fraudeur")
    ax3.title.set_text("Indicateur 3")
    ax3.scatter([X[i] for i in i_val2], [Y[i] for i in i_val2], label="Fraudeur")
    ax3.legend()
    ax4 = plt.subplot(224)
    ax4.set_xlabel("Salaire")
    ax4.set_ylabel("Dépenses")
    ax4.scatter(X,Z, label="Non fraudeur")
    ax4.scatter([X[i] for i in i_val2], [Z[i] for i in i_val2], label="Fraudeur")
    axprev = plt.axes([0.53, 0.02, 0.14, 0.04])
    TextBox(axprev, '', initial="{}/{} fraudeurs ({}%)".format(len(i_val2), len(X), int(100*len(i_val2)/len(X))))
    ax4.legend()
    fig.suptitle("Catégorie socio-professionnelle : {}".format(cat_list[cat]))
    plt.show()

#clusterise_indicateur23(1)

## Paramètres de l'ellipse : a et b

def affichage_indicateur4(cat):
    X = [data_sal[i] for i in data_catm[cat]]
    Y = [data_pat[i] for i in data_catm[cat]]
    M = [i for i in range(int(min(X)), int(max(X))+1)]
    moy_X = sum(X)/len(X)
    moy_Y = sum(Y)/len(Y)
    a = (int(max(X))+1-int(min(X)))/1.5
    b = (max(Y)-moy_Y)*0.6
    K = []
    for i in M:
        if 1-((i-(moy_X*1.2))**2)/(a**2)>=0:
            K.append(moy_Y+((1-((i-(moy_X*1.2))**2)/(a**2))*b**2)**0.5)
        else:
            K.append(moy_Y)
    fig, ax = plt.subplots()
    ax1 = plt.subplot(121)
    ax1.scatter([moy_X for _ in range(int(min(Y)), int(max(Y)+1))], [i for i in range(int(min(Y)), int(max(Y))+1)], label="Salaire moyen")
    ax1.scatter(M, [moy_Y for _ in range(int(min(X)), int(max(X))+1)], label="Patrimoine moyen")
    ax1.scatter(X, Y)
    ax1.scatter(M, K, label="Ratio limite")
    ax1.set_xlabel("Salaire")
    ax1.set_ylabel("Patrimoine")
    ax1.legend()
    af1 = AnnoteFinder(X,Y,data_catm[cat], xtol=1000, ytol=1000)
    fig.canvas.mpl_connect('button_press_event', af1)
    i_val = []
    for i in range(len(X)):
        if 1-((X[i]-(moy_X*1.2))**2)/(a**2)>=0:
            if Y[i]>moy_Y+((1-((X[i]-(moy_X*1.2))**2)/(a**2))*b**2)**0.5:
                i_val.append(i)
        else:
            if Y[i]>moy_Y:
                i_val.append(i)
    ax2 = plt.subplot(122)
    ax2.scatter(X,Y, label="Non fraudeur")
    ax2.scatter([X[i] for i in i_val], [Y[i] for i in i_val], label="Fraudeur")
    ax2.set_xlabel("Salaire")
    ax2.set_ylabel("Patrimoine")
    ax2.legend()
    af2 = AnnoteFinder(X,Y,data_catm[cat], xtol=1000, ytol=1000)
    axprev = plt.axes([0.53, 0.02, 0.14, 0.04])
    TextBox(axprev, '', initial="{}/{} fraudeurs ({}%)".format(len(i_val), len(X), int(100*len(i_val)/len(X))))
    fig.canvas.mpl_connect('button_press_event', af2)
    linkAnnotationFinders([af1, af2])
    fig.suptitle("Catégorie socio-professionnelle : {} – Indicateur 4".format(cat_list[cat]))
    plt.show()

#affichage_indicateur4(4)

def indicateur1():
    V = []
    for cat in range(len(cat_list)):
        X = [data_sal[i] for i in data_catm[cat]]
        Y = [data_pat[i] for i in data_catm[cat]]
        Z = [data_dep[i] for i in data_catm[cat]]
        moy_X = sum(X)/len(X)
        moy_Y = sum(Y)/len(Y)
        for i in range(len(X)):
            if Y[i]>=(max(Y)-((max(Y)-moy_Y)/10)-moy_Y)/(max(X)-min(X))*(X[i]-min(X))+ moy_Y:
                if Z[i]>=X[i]:
                    V.append(1)
                else:
                    V.append(0)
            else:
                V.append(0)
    print(sum(V))
    return V

def indicateur2():
    V = []
    for cat in range(len(cat_list)):
        X = [data_sal[i] for i in data_catm[cat]]
        Y = [data_pat[i] for i in data_catm[cat]]
        Z = [data_dep[i] for i in data_catm[cat]]
        N = [Z[i]-X[i] for i in range(len(X))]
        moy_X = sum(X)/len(X)
        moy_Y = sum(Y)/len(Y)
        moy_N = sum(N)/len(N)
        for i in range(len(X)):
            if N[i]>moy_N+0.35*(max(N)+moy_N) and N[i]>0:
                if Y[i]<moy_Y-0.35*(moy_Y-min(Y)):
                    V.append(1)
                else:
                    V.append(0)
            else:
                V.append(0)
    print(sum(V))
    return V

def indicateur3():
    V = []
    for cat in range(len(cat_list)):
        X = [data_sal[i] for i in data_catm[cat]]
        Y = [data_pat[i] for i in data_catm[cat]]
        Z = [data_dep[i] for i in data_catm[cat]]
        N = [Z[i]-X[i] for i in range(len(X))]
        quant = np.quantile(N,0.8)
        quant2 = np.quantile(Y, 0.2)
        for i in range(len(X)):
            if N[i]>quant and N[i]>0:
                if Y[i]<quant2:
                    V.append(1)
                else:
                    V.append(0)
            else:
                V.append(0)
    print(sum(V))
    return V

def indicateur4():
    V = []
    for cat in range(len(cat_list)):
        X = [data_sal[i] for i in data_catm[cat]]
        Y = [data_pat[i] for i in data_catm[cat]]
        M = [i for i in range(int(min(X)), int(max(X))+1)]
        moy_X = sum(X)/len(X)
        moy_Y = sum(Y)/len(Y)
        a = (int(max(X))+1-int(min(X)))/1.5
        b = (max(Y)-moy_Y)*0.6
        i_val = []
        for i in range(len(X)):
            if 1-((X[i]-(moy_X*1.2))**2)/(a**2)>=0:
                if Y[i]>moy_Y+((1-((X[i]-(moy_X*1.2))**2)/(a**2))*b**2)**0.5:
                    V.append(1)
                else:
                    V.append(0)
            else:
                if Y[i]>moy_Y:
                    V.append(1)
                else:
                    V.append(0)
    print(sum(V))
    return V

def labellisation():
    database["Indicateur 1"] = indicateur1()
    database["Indicateur 2"] = indicateur2()
    database["Indicateur 3"] = indicateur3()
    database["Indicateur 4"] = indicateur4()
    database.to_csv('new_data_big.tsv', sep = '\t')

labellisation()

def synthese_indicateur():
    fig, ax = plt.subplots()
    ax1 = plt.subplot(221)
    i1 = indicateur1()
    ax1.scatter(data_sal, data_pat, label="Non fraudeur")
    ax1.scatter([data_sal[i] for i in range(len(i1)) if i1[i]==1], [data_pat[i] for i in range(len(i1)) if i1[i]==1], label="Fraudeur")
    ax1.set_xlabel("Salaire")
    ax1.set_ylabel("Patrimoine")
    ax1.legend()
    ax1.set_title("Indicateur 1 ({}%)".format(int(100*(sum(i1)/len(i1)))), loc="right")
    ax2 = plt.subplot(222)
    i2 = indicateur2()
    ax2.scatter(data_sal, data_pat, label="Non fraudeur")
    ax2.scatter([data_sal[i] for i in range(len(i1)) if i2[i]==1], [data_pat[i] for i in range(len(i1)) if i2[i]==1], label="Fraudeur")
    ax2.set_xlabel("Salaire")
    ax2.set_ylabel("Patrimoine")
    ax2.legend()
    ax2.set_title("Indicateur 2 ({}%)".format(int(100*sum(i2)/len(i2))), loc="right")
    ax3 = plt.subplot(223)
    i3 = indicateur3()
    ax3.scatter(data_sal, data_pat, label="Non fraudeur")
    ax3.scatter([data_sal[i] for i in range(len(i1)) if i3[i]==1], [data_pat[i] for i in range(len(i1)) if i3[i]==1], label="Fraudeur")
    ax3.set_xlabel("Salaire")
    ax3.set_ylabel("Patrimoine")
    ax3.legend()
    ax3.set_title("Indicateur 3 ({}%)".format(int(100*sum(i3)/len(i3))), loc="right")
    ax4 = plt.subplot(224)
    i4 = indicateur4()
    ax4.scatter(data_sal, data_pat, label="Non fraudeur")
    ax4.scatter([data_sal[i] for i in range(len(i1)) if i4[i]==1], [data_pat[i] for i in range(len(i1)) if i4[i]==1], label="Fraudeur")
    ax4.set_xlabel("Salaire")
    ax4.set_ylabel("Patrimoine")
    ax4.legend()
    ax4.set_title("Indicateur 4 ({}%)".format(int(100*sum(i4)/len(i4))), loc="right")
    fig.suptitle("Synthèse des indicateurs")
    plt.show()

#synthese_indicateur()