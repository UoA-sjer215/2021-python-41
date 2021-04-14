from __future__ import print_function
#from torch import nn, optim, cuda
from torch.utils import data
from torchvision import datasets, transforms
#import torch.nn.functional as F
import time

import torch.autograd as autograd         # computation graph
from torch import Tensor                  # tensor node in the computation graph
import torch.nn as nn                     # neural networks
import torch.nn.functional as F           # layers, activations and more
import torch.optim as optim               # optimizers e.g. gradient descent, ADAM, etc.
from torch.jit import script, trace       # hybrid frontend decorator and tracing jit

# Training settings
batch_size = 64

# MNIST Dataset

train_dataset = datasets.MNIST(root='mnist_data_train/', train=True, transform=transforms.ToTensor(), download=False)

test_dataset = datasets.MNIST(root='mnist_data_test/', train=False, transform=transforms.ToTensor(), download=False)

print('*****datasets loaded*****') #DEBUGGING
# Data Loader (Input Pipeline)
train_loader = data.DataLoader(dataset=train_dataset,
                                           batch_size=batch_size,
                                           shuffle=True)

test_loader = data.DataLoader(dataset=test_dataset,
                                          batch_size=batch_size,
                                          shuffle=False)

class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.l1 = nn.Linear(784, 610) #Layers follow the fibonnaci sequence until reaching desired output size
        self.l2 = nn.Linear(610, 377)
        self.l3 = nn.Linear(377, 233)
        self.l4 = nn.Linear(233, 144)
        self.l5 = nn.Linear(144, 89)
        self.l6 = nn.Linear(89, 55)
        self.l7 = nn.Linear(55, 34)
        self.l8 = nn.Linear(34, 21)
        self.l9 = nn.Linear(21, 13)
        self.l10 = nn.Linear(13, 10)

    def forward(self, x):
        x = x.view(-1, 784)  # Flatten the data (n, 1, 28, 28)-> (n, 784)
        x = F.relu(self.l1(x))
        x = F.relu(self.l2(x))
        x = F.relu(self.l3(x))
        x = F.relu(self.l4(x))
        x = F.relu(self.l5(x))
        x = F.relu(self.l6(x))
        x = F.relu(self.l7(x))
        x = F.relu(self.l8(x))
        x = F.relu(self.l9(x))
        return self.l10(x)

model = Net()
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)








