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

from torch import save as save                    # save funtion to store trained model
from torch import load as load
from torch import as_tensor as to_tensor
from torch import float as tfloat
from torch import argmax

# Training settings
batch_size = 64

# Downloading/locating MNIST Dataset 
def get_train_set():
    train_dataset = datasets.MNIST(root='mnist_data_train/', train=True, transform=transforms.ToTensor(), download=True)
    train_loader = data.DataLoader(dataset=train_dataset, batch_size=batch_size, shuffle=True)

    return train_loader

def get_test_set():
    test_dataset = datasets.MNIST(root='mnist_data_test/', train=False, transform=transforms.ToTensor(), download=True)
    test_loader = data.DataLoader(dataset=test_dataset, batch_size=batch_size, shuffle=False)

    return test_loader

#Defining the Net class
class Net(nn.Module):

    def __init__(self):
        super(Net, self).__init__()
        self.l1 = nn.Linear(784, 520)
        self.l2 = nn.Linear(520, 320)
        self.l3 = nn.Linear(320, 240)
        self.l4 = nn.Linear(240, 120)
        self.l5 = nn.Linear(120, 10)

    def forward(self, x):
        x = x.view(-1, 784)  # Flatten the data (n, 1, 28, 28)-> (n, 784)
        x = F.relu(self.l1(x))
        x = F.relu(self.l2(x))
        x = F.relu(self.l3(x))
        x = F.relu(self.l4(x))
        return self.l5(x)

def netEval(data):
    trans1 = transforms.ToTensor()
    output = model(trans1(data))
    prediction = argmax(output) 
    access = output[0]
    nums_for_sam = []
    for i in range(10):
        selection = access[i]
        nums_for_sam.append(selection.item())
    nums_for_sam.append(prediction.item())
    return nums_for_sam

# Instantiating a Net object 
model = Net()

# Setting criterion and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)

def train(epoch, train_loader):
    #Enables updating model weight
    model.train()
    # the enumerate function is supported by the DataLoader class, allowing us to traverse train_loader
    for batch_idx, (data, target) in enumerate(train_loader):
        optimizer.zero_grad()
        output = model(data)
        loss = criterion(output, target)
        # Updating model weights
        loss.backward()
        optimizer.step()
        #Printing updates as training occurs
        # if batch_idx % 25 == 0:
        #     print('Train Epoch: {} | Batch Status: {}/{} ({:.0f}%) | Loss: {:.6f}'.format(
        #         epoch, batch_idx * len(data), len(train_loader.dataset),
        #         100. * batch_idx / len(train_loader), loss.item()))
    return epoch

def test(test_loader):
     #Disables updating model weights
    model.train(False)
    test_loss = 0
    correct = 0
    for data, target in test_loader:
        output = model(data)
        # sum up batch loss
        test_loss += criterion(output, target).item()
        # get the index of the max
        pred = output.data.max(1, keepdim=True)[1]
        correct += pred.eq(target.data.view_as(pred)).cpu().sum()

    test_loss /= len(test_loader.dataset)
    print(f'===========================\nTest set: Average loss: {test_loss:.4f}, Accuracy: {correct}/{len(test_loader.dataset)} '
          f'({100. * correct / len(test_loader.dataset):.0f}%)')



