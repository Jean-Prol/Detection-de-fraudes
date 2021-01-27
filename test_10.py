import torch
import torch.nn as nn 
import torch.optim as optim 
import torch.nn.functional as F

trainset = [(torch.tensor([[30000., 1000000.]]), torch.tensor([1])), 
            (torch.tensor([[1000000., 30000.]]), torch.tensor([1])),
            (torch.tensor([[30000., 30000.]]), torch.tensor([0])),
            (torch.tensor([[30000., 40000.]]), torch.tensor([0])),
            (torch.tensor([[30000., 20000.]]), torch.tensor([0])), 
            (torch.tensor([40000., 40000.]), torch.tensor([0])),
            (torch.tensor([40000., 50000.]), torch.tensor([0])),
            (torch.tensor([40000., 30000.]), torch.tensor([0])),
            (torch.tensor([50000., 50000.]), torch.tensor([0])),
            (torch.tensor([50000., 60000.]), torch.tensor([0])),
            (torch.tensor([50000., 40000.]), torch.tensor([0]))
             ]


testset = [(torch.tensor([[35000., 1250000.]]), torch.tensor([1])), 
            (torch.tensor([[800000., 27000.]]), torch.tensor([1])),
            (torch.tensor([[33000., 22000.]]), torch.tensor([0])),
            (torch.tensor([[31000., 43000.]]), torch.tensor([0])),
            (torch.tensor([[28000., 29000.]]), torch.tensor([0])), 
            (torch.tensor([43000., 52000.]), torch.tensor([0])),
            (torch.tensor([39000., 50000.]), torch.tensor([0])),
            (torch.tensor([44000., 31000.]), torch.tensor([0])),
            (torch.tensor([52000., 50000.]), torch.tensor([0])),
            (torch.tensor([51000., 67000.]), torch.tensor([0])),
            (torch.tensor([50000., 44000.]), torch.tensor([0]))
             ]


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
#X = torch.rand((1,2))
#X = X.view(-1, 1*2)
#output = net(X) 
#print(output)

optimizer = optim.Adam(net.parameters(), lr =0.001)

#Le nombre de fois qu'on va parcourir le trainset pour entrainer notre algo 
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


X = torch.tensor([20800., 50000.])
X = X.view(-1, 1*2)
output = net(X) 
print(output)
for idx, i in enumerate(output): 
    if torch.argmax(i) == 0: 
        print("Non fraudeur")
    else : 
        print("Fraudeur")