import torch
import torch.nn as nn 
import torch.optim as optim 
import torch.nn.functional as F
import pandas as pd 
from random import shuffle
import time

def test_reseau(n_indicateur, n_epochs):
    ### Importation de la base de données

    database = pd.read_csv("/Users/jeanprolhac/Desktop/Projet/Projet 16 - IA et fraude/Detection-de-fraudes/new_data_big.tsv", sep="\t")

    ### Création du trainset et du testset

    cat_list = ["cadre", "profession intermédiaire", "employé", "ouvrier", "chef d'entreprise", "agriculteur"]

    data = database.loc[0:5972]
    data_cat = list(data["catégorie"])
    data_sal = list(data["salaire"])
    data_dep = list(data["dépenses"])
    data_pat = list(data["patrimoine"])
    data_i = list(data["Indicateur {}".format(n_indicateur)])

    trainset = []

    for i in range(len(data_cat)) : 
        trainset.append((torch.tensor([[float(data_cat[i]), float(data_sal[i]), float(data_dep[i]), float(data_pat[i])]]), torch.tensor([data_i[i]])))
    
    ### Début du réseau de neurones

    class Net(nn.Module) : 
        #define the layers
        def __init__(self) : 
            super().__init__() 
            self.fc1 = nn.Linear(4, 64)
            self.fc2 = nn.Linear(64, 64)
            self.fc3 = nn.Linear(64, 64)
            self.fc4 = nn.Linear(64, 2)
        def forward(self, x) : 
            x = F.relu(self.fc1(x))
            x = F.relu(self.fc2(x))
            x = F.relu(self.fc3(x))
            x = self.fc4(x) 
            return F.log_softmax(x, dim=1)


    start = time.time()
    net = Net() 

    ### Début de l'entraînement

    optimizer = optim.Adam(net.parameters(), lr =0.001)

    ### Le nombre de fois qu'on va parcourir le trainset pour entrainer notre algo 

    EPOCHS = n_epochs

    for epoch in range(EPOCHS) : 
        for data in trainset : 
            X, y = data  
            net.zero_grad() 
            output = net(X.view(-1, 1*4))
            loss = F.nll_loss(output, y)
            loss.backward() 
            optimizer.step() 
        #print(loss)

    end = time.time()
    #print(end-start)

    ### Mesures de performance

    testbase = pd.read_csv("/Users/jeanprolhac/Desktop/Projet/Projet 16 - IA et fraude/Detection-de-fraudes/new_data_big_test.tsv", sep="\t")

    basetest = testbase.loc[0:5972]
    test_cat = list(basetest["catégorie"])
    test_sal = list(basetest["salaire"])
    test_dep = list(basetest["dépenses"])
    test_pat = list(basetest["patrimoine"])
    test_i = list(basetest["Indicateur {}".format(n_indicateur)])
                
    test = []

    for i in range(len(test_cat)) : 
        test.append((torch.tensor([[float(test_cat[i]), float(test_sal[i]), float(test_dep[i]), float(test_pat[i])]]), torch.tensor([test_i[i]])))

    correct2 = 0 
    total2 = 0 

    with torch.no_grad() : 
        for data in test : 
            X, y = data
            output = net(X.view(-1, 4))
            for idx, i in enumerate(output): 
                if torch.argmax(i) == y[idx]: 
                    correct2 += 1 
                total2 += 1

    #print("Accuracy: ", round(correct2/total2, 10))
    return (end-start, round(correct2/total2, 10))

epoch = []
indicateur = []
temps = []
accuracy = []
for n_epoch in range(6):
    for n_indicateur in range(1,5):
        epoch.append(n_epoch)
        indicateur.append(n_indicateur)
        t, a = test_reseau(n_indicateur, n_epoch)
        temps.append(t)
        accuracy.append(a)

res = pd.DataFrame(list(zip(epoch, indicateur, temps, accuracy)), columns = ['Epoch', 'Indicateur', 'Temps', 'Accuracy'])

#res.to_csv('res.tsv', sep = '\t')