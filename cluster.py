import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import KMeans
import pandas as pd

database = pd.read_csv("D:\MOI\CentraleSupelec\Cours CS\Projet - Modélisation mathématiques\Test\Detection-de-fraudes\labelled_database.tsv", sep="\t")

traindata = database.loc[1:900]
trainincome = list(traindata["income"])
traintaxclass = list(traindata["expenses"])

X = np.array([[trainincome[i], traintaxclass[i]] for i in range (len(trainincome))])

"""plt.scatter(X[:,0], X[:,1])
plt.show()"""

clf = KMeans(n_clusters = 3)
clf.fit(X)
centroids = clf.cluster_centers_
labels = clf.labels_

colors =10 * ["g.", "r.", "c.", "b.", "k.", "y."]  

for i in range (len(X)) : 
    plt.plot(X[i][0], X[i][1], colors[labels[i]], markersize = 10)
    
plt.scatter(centroids[:,0], centroids[:,1], marker = "x")
plt.plot(trainincome, trainincome)
plt.show()

#print(X)

