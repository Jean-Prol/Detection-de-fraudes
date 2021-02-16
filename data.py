import numpy as np
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from sklearn.naive_bayes import GaussianNB

prop=0.577
loca=1-prop

patri={"cadre":392100,"profession intermédiaire":221400, "employé":123300,
             'ouvrier':112200,"chef d'entreprise":547400,'agriculteur':1040000}

pourcentage={"cadre":0.193,"profession intermédiaire":0.256, "employé":0.268,
             'ouvrier':0.196,"chef d'entreprise":0.067,'agriculteur':0.015}

moyenne={"cadre":41650,"profession intermédiaire":23030, "employé":13780,
             'ouvrier':15180,"chef d'entreprise":114000,'agriculteur':30360}
ecart_type={"cadre":5000,"profession intermédiaire":3000, "employé":1000,
             'ouvrier':2000,"chef d'entreprise":10000,'agriculteur':7000}
expense={"cadre":0.95,"profession intermédiaire":0.98, "employé":1,
             'ouvrier':1,"chef d'entreprise":0.85,'agriculteur':0.99}

categories=list(moyenne.keys())
def generate_salaire(n) :
    categorie=[]
    l=[]
    m=[]
    p=[]
    for x in categories :
        a=round(pourcentage[x]*n)
        categorie+=a*[categories.index(x)]
        b=np.random.normal(moyenne[x],ecart_type[x],a)
        l+=list(b)
        m+=[expense[x]*w for w in b]
        p+=list(np.random.normal(patri[x],10000,a))
    a=len(l)
    noise=np.random.normal(0,3000,a)
    salaire=[noise[i]+l[i] for i in range(a)]
    noise=np.random.normal(0,1000,a)
    expenses=[m[i]+noise[i] for i in range(a)]
    noise=np.random.normal(0,10000,a)
    patrimoine=[p[i] + noise[i] for i in range(a)]
    
    return categorie, salaire,expenses,patrimoine

cat,sal,ex,pat=generate_salaire(500)

"""
X = np.array([[sal[i],ex[i],cat[i],pat[i]] for i in range (len(pat))])
clf = GaussianNB()
a=[[20000,50000,1,200000],[30000,28000,4,1000000],[41650,40650,0,392100],
   [23030,23030,1,221400],[13780,14780,2,123300],[15180,15180,3,112200],
   [114000,100000,4,540000],[30360,31000,5,1040000],[40000,10000,0,400000]]
b=[1,1,0,0,0,0,0,0,1]
clf.fit(a,b)
label=clf.predict(X)

"""

    
    
    