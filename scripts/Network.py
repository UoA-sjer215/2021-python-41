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

# Training settings
batch_size = 64

# Downloading/locating MNIST Dataset

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
    # This function (hopefully) runs the data through the currently saved nn,
    # and returns the prediction
    model = load('model.pth')
    model.eval()
    output = model(data)
    prediction = torch.argmax(output) #Unsure if this is valid in our case? Still needs testing
    return prediction

# Instantiating a Net object 
model = Net()

# Setting criterion and optimizer
criterion = nn.CrossEntropyLoss()
optimizer = optim.SGD(model.parameters(), lr=0.01, momentum=0.5)

def train(epoch):
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
        if batch_idx % 10 == 0:
            print('Train Epoch: {} | Batch Status: {}/{} ({:.0f}%) | Loss: {:.6f}'.format(
                epoch, batch_idx * len(data), len(train_loader.dataset),
                100. * batch_idx / len(train_loader), loss.item()))
    # Saving the model so it can be used again without retraining (unsure if this the right place for this)
    save(model, 'model.pth')

def test():
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


def test_and_train(US_epoch): #Acceptd a user selected value of epoch
    since = time.time()
    for epoch in range(1, US_epoch):
        epoch_start = time.time()
        train(epoch)

        m, s = divmod(time.time() - epoch_start, 60)
        print(f'Training time: {m:.0f}m {s:.0f}s')
        test()
        m, s = divmod(time.time() - epoch_start, 60)
        print(f'Testing time: {m:.0f}m {s:.0f}s')

    m, s = divmod(time.time() - since, 60)
    print(f'Total Time: {m:.0f}m {s:.0f}s')

if __name__ == '__main__':
    test_and_train(2)


