import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


filePlace = ''
epoch = 0

class App (QWidget):
    
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
            self.drawing = False
            self.lastPoint = QPoint()
            self.image = QPixmap("blank.jpg")
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

        
    def import_method(self):
        impW = App(3)

    def preTraining(self):
        groupbox = QGroupBox('Pre-Training Settings')


        importTraining = QPushButton('Import')
        importTraining.clicked.connect(self.import_method)

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
        print('connect this function to the train function, and remember to take teh epoch amount')

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.start_btn.setText('Finished')
            return

        self.step = self.step + 1
        self.pbar.setValue(self.step)           # update the progress bar

    def doAction(self):
        if self.timer.isActive():
            self.timer.stop()
            self.start_btn.setText('Start')
        else:
            self.timer.start(100, self)
            self.start_btn.setText('Stop')

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
        # btn.move(40, 80)

        vbox = QVBoxLayout()
        vbox.addWidget(lbl1)
        vbox.addWidget(self.epoch_value)
        vbox.addWidget(train)
        vbox.addWidget(self.pbar)
        vbox.addWidget(self.start_btn)
        groupbox.setLayout(vbox)

        return groupbox

    def open(self):
        self.drawing_window = App(2)



    def digitInsert(self):
        groupbox = QGroupBox('Drawing')
        open_drawing = QPushButton('Draw')
        open_drawing.clicked.connect(self.open)
        
        vbox = QVBoxLayout()
        vbox.addWidget(open_drawing)
        groupbox.setLayout(vbox)
        return groupbox

    def paintEvent(self, event):
        painter = QPainter(self)
        self.blank = QPixmap("blank.jpg")


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.drawing and 1:
            painter = QPainter(self.blank)
            painter.setPen(QPen(Qt.red, 3, Qt.SolidLine))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

    




#creates the qapplication
parent = QApplication(sys.argv)

mainW = App(1)


#execute the qapplication
sys.exit(parent.exec())
