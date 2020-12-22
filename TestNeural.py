import torch
import torchvision
from torchvision import transforms, datasets
import torch.nn as nn
import torch.nn.functional as F




### DATAS ###

## Ici on traite à titre d'exemple d'images d'écriture à la main. 

#Données d'entrainement (from internet)
train = datasets.MNIST("", train=True, download=True, transform=transforms.Compose([transforms.ToTensor()]))

#Données de test (téléchargés sur le net)
test = datasets.MNIST("", train=False, download=True, transform=transforms.Compose([transforms.ToTensor()]))



trainset = torch.utils.data.DataLoader(train, batch_size=10,shuffle=True)
testset = torch.utils.data.DataLoader(train, batch_size=10,shuffle=True)




### Le tuto conseille de maîtriser la programmation orientée objet pour tout saisir ###



### NEURAL NETWORK ITSELF ###


import torch.nn as nn
import torch.nn.functional as F

class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.fc1=nn.Linear(28*28, 64) #Ici on crée la première couche en précisant l'entrée et la sortie (28*28 est l'image, et 64 la prochaine couche de 64 neuronnes)
        self.fc2=nn.Linear(64, 64) #2e couche...
        self.fc3=nn.Linear(64, 64)
        self.fc4=nn.Linear(64, 10) #Dernière couche a 10 sorties : les 10 chiffres 

    def forward(self,x): # Ici on fait passer l'info dans le réseau
        x = F.relu(self.fc1(x))
        x = F.relu(self.fc2(x)) #F.relu est la fonction d'activation. (Relu est la fonction discontinue)
        x = F.relu(self.fc3(x))
        x = self.fc4(x)

        # On peut créer un modèle plus complexe de réseau avec des if, else ...

        return F.log_softmax(x,dim=1)




net=Net()
print(net)

X = torch.rand((28,28))
X=X.view(-1,28*28) 

output=net(X)
print(output)









import torch.optim as optim

### PARAMETERS ###


optimizer = optim.Adam(net.parameters(),lr=0.001) #Lr est le learning rate, le pas de déplacement de la descente de gradient

#Attention le choix du learning rate est super important. Il est bon de commencer avec 
#Un gros lr, puis le diminuer jusquà obtenir un résultat satisfaisant. 









### TRAINING ###


EPOCHS = 3 #Number of training sessions



for epoch in range(EPOCHS):
    for data in trainset:
        #data is a batch of featuresets ans labels
        X,y = data
        net.zero_grad()
        output = net(X.view(-1,28*28)) #Rappel : view permet de reshape le torch dans une bonne taille (ici une ligne)
        loss = F.nll_loss(output,y) #Ici on calcule l'erreur de différence entre la sortie et le label
        loss.backward() #On propage le calcul d'erreur et les modifications dans le réseau (tout est déjà fait par la librairie)
        optimizer.step() #Ajuste les poids des connections dans le réseau
    print(loss) #Observons l'erreur au fur et à mesure de l'évolution du process !










### EFFICIENCY ###

# Regardons quelle est la proportion de bonnes prédictions après ces 3 entraînements !

correct = 0
total = 0

with torch.no_grad(): #inutile de calculer des gradients ici
    for data in trainset : 
        X,y = data
        output = net(X.view(-1,784))
        for idx, i in enumerate(output):
            if torch.argmax(i) == y[idx]:
                correct+=1
            total+=1
print("Accuracy : ", round(correct/total, 3))







### RESULTS ###


# Regardons quelques images et voyons si nous les avons trouvées justes. 

import matplotlib.pyplot as plt 

indice = 0 #A modifier pour observer différentes images

plt.imshow(X[indice].view(28,28)) #Numéro écrit à la main
plt.show()

print(torch.argmax(net(X[indice].view(-1,784))[0])) #Numéro vu prédit par le neuronne (penser à femer la fenêtre de l'image pourqu'il s'affiche)





### Vous pouvez Run la section entière, l'entraînement du réseau dure environ 30 secondes ###





