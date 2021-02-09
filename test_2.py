import torch
import torch.nn as nn 
import torch.optim as optim 
import torch.nn.functional as F
import pandas as pd 


### Importation de la base de données

database = pd.read_csv("D:\MOI\CentraleSupelec\Cours CS\Projet - Modélisation mathématiques\Test\Detection-de-fraudes\labelled_database.tsv", sep="\t")

### Création du trainset et du testset

trainset = []             
testset = []


traindata = database.loc[1:50]
testdata = database.loc[50:100]
trainincome = list(traindata["income"])
traintaxclass = list(traindata["taxclass"])
trainfraud = list(traindata["fraud"])
testincome = list(testdata["income"])
testtaxclass = list(testdata["taxclass"])
testfraud = list(testdata["fraud"])

for i in range(50) : 
    trainset.append((torch.tensor([[float(trainincome[i]), float(traintaxclass[i])]]), torch.tensor([trainfraud[i]])))
    testset.append((torch.tensor([[float(testincome[i]), float(testtaxclass[i])]]), torch.tensor([testfraud[i]])))



### Début duu réseau de neurones



class Net(nn.Module) : 

    #define the layers
    def __init__(self) : 
        super().__init__() 
        self.fc1 = nn.Linear(2, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, 64)
        self.fc4 = nn.Linear(64, 2)


    def forward(self, x) : 
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x))
        x = F.relu(self.fc3(x))
        x = self.fc4(x) 
        return F.log_softmax(x, dim=1)



net = Net() 

### Début de l'entraînement

optimizer = optim.Adam(net.parameters(), lr =0.001)

# Le nombre de fois qu'on va parcourir le trainset pour entrainer notre algo 

EPOCHS = 5

for epoch in range(EPOCHS) : 
    for data in trainset : 
        X, y = data  
        net.zero_grad() 
        output = net(X.view(-1, 1*2))
        loss = F.nll_loss(output, y)
        loss.backward() 
        optimizer.step() 
    print(loss)

### Début des mesures de performance

correct = 0 
total = 0 

with torch.no_grad() : 
    for data in testset : 
        X, y = data
        output = net(X.view(-1, 2))
        for idx, i in enumerate(output): 
            if torch.argmax(i) == y[idx]: 
                correct += 1 
            total += 1

print("Accuracy: ", round(correct/total, 3))


### Test sur un cas 

X = torch.tensor([50000., 50000.])
X = X.view(-1, 1*2)
output = net(X) 
print(output)
for idx, i in enumerate(output): 
    if torch.argmax(i) == 0: 
        print("Non fraudeur")
    else : 
        print("Fraudeur")