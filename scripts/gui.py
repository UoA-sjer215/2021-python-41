import sys

import Network

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PIL import Image as PIL_Image     
import numpy as np                                                                    

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

    def preTraining(self):
        groupbox = QGroupBox('Pre-Training Settings')


        importTraining = QPushButton('Import')
        importTraining.clicked.connect(self.import_clicked)

        pixmap = QPixmap('cat.jpg')
        lbl_img = QLabel()
        lbl_img.setPixmap(pixmap)

        dispTraining = QPushButton('Display random training image')
        dispTesting = QPushButton('Display random testing image')

        vbox = QVBoxLayout()
        vbox.addWidget(importTraining)
        vbox.addWidget(lbl_img)
        vbox.addWidget(dispTraining)
        vbox.addWidget(dispTesting)
        
        vbox.addStretch(1)
        groupbox.setLayout(vbox)

        return groupbox


    def value_changed(self):
        self.epoch = self.epoch_value.value()

    def train_clicked(self):
        for epoch in range(1, self.epoch+1):
            progress = Network.train(epoch, self.train_loader)
            Network.test(self.test_loader)
            self.timerEvent(100/(self.epoch) * progress)
        # Saving the model so it can be used again without retraining (unsure if this the right place for this)
        print("********************Model Saved***********************")
        Network.save(Network.model, 'model.pth')
            
    def timerEvent(self,percentage):
        # if percentage >= 100:
        #     return
        self.pbar.setValue(percentage)           # update the progress bar

    def doAction(self):
        while self.step < 101:
            self.timerEvent()
    
    def test_drawing_clicked(self):
        self.image = QPixmap('new_digit')
        img = QPixmapToArray(self.image)
        prediction = Network.netEval(img)
 
            

    def training(self):
        groupbox = QGroupBox('Training Settings')

        self.epoch_value = QSpinBox()
        self.epoch_value.setRange(0, 15)
        self.epoch_value.setSingleStep(2)        
        self.epoch_value.valueChanged.connect(self.value_changed)

        lbl1 = QLabel('Epoch Amount (the more you have, the more accurate the model is)')

        train = QPushButton('NO PAIN NO TRAIN')
        train.clicked.connect(self.train_clicked)

        self.pbar = QProgressBar(self)
        self.pbar.setGeometry(30, 40, 200, 25)

        self.timer = QBasicTimer()
        self.step = 0 

        self.start_btn = QPushButton('Start')
        self.start_btn.clicked.connect(self.doAction)

        vbox = QVBoxLayout()
        vbox.addWidget(lbl1)
        vbox.addWidget(self.epoch_value)
        vbox.addWidget(train)
        vbox.addWidget(self.pbar)
        vbox.addWidget(self.start_btn)
        groupbox.setLayout(vbox)

        return groupbox

    def open(self):
        self.drawW = Drawer()
        self.drawW.show()

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


    def guess(self):
        groupbox = QGroupBox('Number Guesses')
        N0 = QProgressBar(self)
        N0.setFormat('digit 0')
        N1 = QProgressBar(self)
        N1.setFormat('digit 1')
        N2 = QProgressBar(self)
        N2.setFormat('digit 2')
        N3 = QProgressBar(self)
        N3.setFormat('digit 3')
        N4 = QProgressBar(self)
        N4.setFormat('digit 4')
        N5 = QProgressBar(self)
        N5.setFormat('digit 5')
        N6 = QProgressBar(self)
        N6.setFormat('digit 6')
        N7 = QProgressBar(self)
        N7.setFormat('digit 7')
        N8 = QProgressBar(self)
        N8.setFormat('digit 8')
        N9 = QProgressBar(self)
        N9.setFormat('digit 9')

        vbox = QVBoxLayout()
        vbox.addWidget(N0)
        vbox.addWidget(N1)
        vbox.addWidget(N2)
        vbox.addWidget(N3)
        vbox.addWidget(N4)
        vbox.addWidget(N5)
        vbox.addWidget(N6)
        vbox.addWidget(N7)
        vbox.addWidget(N8)
        vbox.addWidget(N9)

        groupbox.setLayout(vbox)
        return groupbox

    def upgrade_guess(self):
        self.N0.setValue(num0/total_guess * 100) 
        self.N1.setValue(num0/total_guess * 100) 
        self.N2.setValue(num0/total_guess * 100) 
        self.N3.setValue(num0/total_guess * 100) 
        self.N4.setValue(num0/total_guess * 100) 
        self.N5.setValue(num0/total_guess * 100) 
        self.N6.setValue(num0/total_guess * 100) 
        self.N7.setValue(num0/total_guess * 100) 
        self.N8.setValue(num0/total_guess * 100) 
        self.N9.setValue(num0/total_guess * 100) 




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
            painter.setPen(QPen(Qt.black, 15, Qt.SolidLine))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

#creates the qapplication
parent = QApplication(sys.argv)

mainW = App(1)
# drawW = Drawer()


#execute the qapplication
sys.exit(parent.exec())
