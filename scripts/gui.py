import sys

import Network

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PIL import Image     
import numpy as np
import time
from torchvision.utils import save_image


Maxvalue = 60000

filePlace = ''

def QPixmapToArray(pixmap):
    pixmap = pixmap.scaledToHeight(28)
    ## Get the size of the current pixmap
    size = pixmap.size()
    h = size.width()
    w = size.height()

    ## Get the QImage Item and convert it to a byte string
    qimg = pixmap.toImage()
    array = qimg.bits().asarray(784)

    return array

#Main function that creates the window
class App (QWidget):
    #important data needed
    epoch = 0
    train_loader = None
    test_loader = None
    picplace = 0
    
    #initiate function
    def __init__ (self,num):
        super().__init__()
        self.main(num)
 
    #start function that creates the windows
    def main (self,num):
        #the numbers are for different windows that can be opened
        #not all of them are currently in use

        if num == 1:
            #main start window
            self.setWindowTitle("main")
            self.move(500,200)
            self.setWindowIcon(QIcon('cat.jpg'))
            self.resize(900,600)

            #sets the quadrants for the amin window ( and location)
            grid = QGridLayout()
            grid.addWidget(self.preTraining(), 0, 0)
            grid.addWidget(self.training(), 0, 1)
            grid.addWidget(self.digitInsert(), 1, 1)
            grid.addWidget(self.guess(), 1, 0)

            self.setLayout(grid)

            self.show()

        elif num == 2 :
            #The old drawing window, (no longer used)
            self.setWindowTitle("drawing")
            self.drawing = False
            self.lastPoint = QPoint()
            self.image = QPixmap("cat.jpg")
            self.move(500,200)
            self.resize(400,400)
            self.show()

        elif num == 3 :
            #File dialog window, (can get a file path)
            self.setWindowTitle('find training data')
            self.setGeometry(500,200,900,600)

            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
            if fileName:
                filePlace = fileName

    #imports the data
    def import_clicked(self):
        self.test_loader = Network.get_test_set()
        self.train_loader = Network.get_train_set()
        print(self.train_loader)
        print(self.test_loader)

        self.AllDataImages =  iter(self.test_loader)


    def go_next(self):
        print('next')
        for batch_idx, (data, target) in enumerate(self.train_loader):
            print('batch index = ')
            print(batch_idx)
            print('contents of data at index = ') 
            print(data[batch_idx])
            save_image(data[self.dataset_index], 'dataset_img.png')
            self.datasetImage.setPixmap(QPixmap('dataset_img.png'))
            self.dataset_index += 1
            break
        
    def go_previous(self):
        print('back')


    #Pre-training, will load and make the dataset usable
    #ahould aslo be able to loop through the images in the dataset 
    def preTraining(self):
        groupbox = QGroupBox('Pre-Training Settings')


        importTraining = QPushButton('Import')
        importTraining.clicked.connect(self.import_clicked)

        self.dataImage = QPixmap('cat.jpg')
        self.datasetImage = QLabel()
        self.datasetImage.setPixmap(self.dataImage)
        self.dataset_index = 0

        #Next and Previous buttons
        Next = QPushButton('Next')
        Next.clicked.connect(self.go_next)

        Previous = QPushButton('Previous')
        Previous.clicked.connect(self.go_previous)

        vbox = QVBoxLayout()
        vbox.addWidget(importTraining)
        vbox.addWidget(self.datasetImage)
        vbox.addWidget(Next)
        vbox.addWidget(Previous)
        
        vbox.addStretch(1)
        groupbox.setLayout(vbox)

        return groupbox



    #changes teh current epoch
    def value_changed(self):
        self.epoch = self.epoch_value.value()

    #trains the dataset based on the epoch amount selected
    def train_clicked(self):
        for epoch in range(1, self.epoch+1):
            progress = Network.train(epoch, self.train_loader)
            Network.test(self.test_loader)
            self.timerEvent(100/(self.epoch) * progress)
        # Saving the model so it can be used again without retraining (unsure if this the right place for this)
        print("********************Model Saved***********************")
        Network.save(Network.model, 'model.pth')
            


    #updates the trainging progress bar
    def timerEvent(self,percentage):
        # if percentage >= 100:
        #     return
        self.pbar.setValue(percentage)           # update the progress bar


    #will submit the drawing created to the NN
    def test_drawing_clicked(self):
        # self.image = QPixmap('new_digit')
        # img = QPixmapToArray(self.image)

        img = Image.open('new_digit.png')
        img = img.resize((28, 28))

        prediction = Network.netEval(img)
        self.upgrade_guess(prediction)
        print(prediction)



    #the training quadrant, containt all the stuff inside
    def training(self):
        groupbox = QGroupBox('Training Settings')


        self.epoch_value = QSpinBox()
        self.epoch_value.setRange(0, 15)
        self.epoch_value.setSingleStep(2)        
        self.epoch_value.valueChanged.connect(self.value_changed)

        lbl1 = QLabel('Epoch Amount (the more you have, the more accurate the model is)')

        train = QPushButton('Train Model')
        train.clicked.connect(self.train_clicked)

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        self.timer = QBasicTimer()
        self.step = 0 

        vbox = QVBoxLayout()
        vbox.addWidget(lbl1)
        vbox.addWidget(self.epoch_value)
        vbox.addWidget(train)
        vbox.addWidget(self.pbar)
        groupbox.setLayout(vbox)

        return groupbox
        
    #creates the drawing window
    def open(self):
        self.drawW = Drawer()
        self.drawW.show()

    #Creates teh drawing quadrant
    def digitInsert(self):
        groupbox = QGroupBox('Drawing')
        open_drawing = QPushButton('new draw')
        open_drawing.clicked.connect(self.open)

        test_drawing = QPushButton('Test Drawing')
        test_drawing.clicked.connect(self.test_drawing_clicked)
        
        vbox = QVBoxLayout()
        vbox.addWidget(open_drawing)
        vbox.addWidget(test_drawing)
        groupbox.setLayout(vbox)
        return groupbox

    #creates the guess quadrant, (only has progress bars)
    def guess(self):
        groupbox = QGroupBox('Number Guesses')

        self.numGuess =QLabel("No guess made")
        # self.N0 = QProgressBar(self)
        # self.N1 = QProgressBar(self)
        # self.N2 = QProgressBar(self)
        # self.N3 = QProgressBar(self)
        # self.N4 = QProgressBar(self)
        # self.N5 = QProgressBar(self)
        # self.N6 = QProgressBar(self)
        # self.N7 = QProgressBar(self)
        # self.N8 = QProgressBar(self)
        # self.N9 = QProgressBar(self)

        vbox = QVBoxLayout()
        vbox.addWidget(self.numGuess)
        # vbox.addWidget(self.N0)
        # vbox.addWidget(self.N1)
        # vbox.addWidget(self.N2)
        # vbox.addWidget(self.N3)
        # vbox.addWidget(self.N4)
        # vbox.addWidget(self.N5)
        # vbox.addWidget(self.N6)
        # vbox.addWidget(self.N7)
        # vbox.addWidget(self.N8)
        # vbox.addWidget(self.N9)

        groupbox.setLayout(vbox)
        return groupbox

    #the function to call to update the quess values 
    def upgrade_guess(self,prediction):
        self.numGuess.setText("Prediction is that it's number" + str(prediction))

        # self.N0.setValue(num0/total_guess * 100) 
        # self.N1.setValue(num0/total_guess * 100) 
        # self.N2.setValue(num0/total_guess * 100) 
        # self.N3.setValue(num0/total_guess * 100) 
        # self.N4.setValue(num0/total_guess * 100) 
        # self.N5.setValue(num0/total_guess * 100) 
        # self.N6.setValue(num0/total_guess * 100) 
        # self.N7.setValue(num0/total_guess * 100) 
        # self.N8.setValue(num0/total_guess * 100) 
        # self.N9.setValue(num0/total_guess * 100) 




class Drawer(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("drawing")
        self.drawing = False
        self.lastPoint = QPoint()
        self.image = QPixmap("blank.png")
        self.image = self.image.scaled(280, 280)
        self.image.save('blank.png', 'PNG')
        self.resize(self.image.width(), self.image.height())
        self.move(500,200)
        self.show()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.drawPixmap(self.rect(), self.image)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.drawing :
            painter = QPainter(self.image)
            painter.setPen(QPen(Qt.white, 15, Qt.SolidLine))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()
            self.image.save("new_digit.png", "PNG")

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

#creates the qapplication
parent = QApplication(sys.argv)

mainW = App(1)
# drawW = Drawer()


#execute the qapplication
sys.exit(parent.exec())
