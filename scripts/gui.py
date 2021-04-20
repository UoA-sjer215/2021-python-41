import sys

import Network

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from PIL import Image as PIL_Image     
import numpy as np                                                                    

filePlace = ''

def QPixmapToArray(pixmap):
    ## Get the size of the current pixmap
    size = pixmap.size()
    h = size.width()
    w = size.height()

    ## Get the QImage Item and convert it to a byte string
    qimg = pixmap.toImage()
    array = qimg.bits().asarray(784)

    return array

class App (QWidget):
    epoch = 0
    train_loader = None
    test_loader = None
    
    def __init__ (self,num):
        super().__init__()
        self.main(num)
 
    def main (self,num):

        if num == 1:
            self.setWindowTitle("main")
            self.move(500,200)
            self.setWindowIcon(QIcon('cat.jpg'))
            self.resize(900,600)

        
            grid = QGridLayout()
            grid.addWidget(self.preTraining(), 0, 0)
            grid.addWidget(self.training(), 0, 1)
            grid.addWidget(self.digitInsert(), 1, 1)

            self.setLayout(grid)

            self.show()

        elif num == 2 :
            self.setWindowTitle("drawing")
            self.drawing = False
            self.lastPoint = QPoint()
            self.image = QPixmap("cat.jpg")
            self.move(500,200)
            self.resize(400,400)
            self.show()

        elif num == 3 :
            self.setWindowTitle('find training data')
            self.setGeometry(500,200,900,600)

            options = QFileDialog.Options()
            options |= QFileDialog.DontUseNativeDialog
            fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*);;Python Files (*.py)", options=options)
            if fileName:
                filePlace = fileName

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
            
    def timerEvent(self,percentage):
        # if percentage >= 100:
        #     return
        self.pbar.setValue(percentage)           # update the progress bar

    def doAction(self):
        while self.step < 101:
            self.timerEvent()
    
    def test_drawing_clicked(self):
        self.image = QPixmap('new_digit')
        self.image = self.image.scaledToHeight(28)
        print(self.image.save('new_digit_scaled.png',"PNG"))
        img = QPixmapToArray(self.image)
        print("img type is:")
        print(type(img))
        prediction = Network.netEval(img)
        print(prediction)

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
        drawW.show()

    def digitInsert(self):
        groupbox = QGroupBox('Drawing')
        open_drawing = QPushButton('Draw')
        open_drawing.clicked.connect(self.open)

        test_drawing = QPushButton('Test Drawing')
        test_drawing.clicked.connect(self.test_drawing_clicked)
        
        vbox = QVBoxLayout()
        vbox.addWidget(open_drawing)
        vbox.addWidget(test_drawing)
        groupbox.setLayout(vbox)
        return groupbox

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
            painter.setPen(QPen(Qt.black, 5, Qt.SolidLine))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()
            print(self.image.save('new_digit.png', "PNG"))

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

#creates the qapplication
parent = QApplication(sys.argv)

mainW = App(1)
drawW = Drawer()


#execute the qapplication
sys.exit(parent.exec())
