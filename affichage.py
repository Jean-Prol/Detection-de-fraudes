import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd
import math 

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

database = pd.read_csv("/Users/jeanprolhac/Desktop/Projet/Projet 16 - IA et fraude/Detection-de-fraudes/new_data.tsv", sep="\t")

data = database.loc[1:498]
data_cat = list(data["catégorie"])
data_sal = list(data["salaire"])
data_dep = list(data["dépenses"])
data_pat = list(data["patrimoine"])

data_catm=[[],[],[],[],[],[]]

for i in range(len(data_cat)):
    elem=data_cat[i]
    if elem=="cadre":
        data_catm[0].append(i)
    elif elem=="profession intermédiaire":
        data_catm[1].append(i)
    elif elem=="employé":
        data_catm[2].append(i)
    elif elem=="ouvrier":
        data_catm[3].append(i)
    elif elem=="chef d'entreprise":
        data_catm[4].append(i)
    else:
        data_catm[5].append(i)

def tracer_donnees(cat):
    X = [data_sal[i] for i in data_catm[cat]]
    Y = [data_pat[i] for i in data_catm[cat]]
    Z = [data_dep[i] for i in data_catm[cat]]
    M=[i for i in range(int(min(X)), int(max(X)+1))]
    moy_X = sum(X)/len(X)
    moy_Y = sum(Y)/len(Y)
    fig, ax = plt.subplots()
    ax1=plt.subplot(121)
    ax1.scatter([moy_X for _ in range(int(min(Y)), int(max(Y)+1))], [i for i in range(int(min(Y)), int(max(Y))+1)])
    ax1.scatter([i for i in range(int(min(X)), int(max(X)+1))], [moy_Y for _ in range(int(min(X)), int(max(X))+1)])
    ax1.scatter(X, Y)
    af1 = AnnoteFinder(X,Y,data_catm[cat])
    fig.canvas.mpl_connect('button_press_event', af1)
    ax2=plt.subplot(122)
    ax2.scatter(M,M)
    ax2.scatter(X, Z)
    af2 = AnnoteFinder(X,Z,data_catm[cat])
    fig.canvas.mpl_connect('button_press_event', af2)
    linkAnnotationFinders([af1, af2])
    plt.show()

tracer_donnees(0)