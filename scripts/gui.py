import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *





class App (QWidget):
    epoch = 0
    def __init__ (self):
        super().__init__()
        self.main()

 
    def main (self):
        self.setWindowTitle("main")
        self.move(500,300)
        self.setWindowIcon(QIcon('cat.jpg'))
        self.resize(900,600)

        
        grid = QGridLayout()
        grid.addWidget(self.preTraining(), 0, 0)
        grid.addWidget(self.training(), 0, 1)
        grid.addWidget(self.digitInsert(), 1, 1)

        self.setLayout(grid)



        self.show()


    def preTraining(self):
        groupbox = QGroupBox('Pre-Training Settings')


        importTraining = QPushButton('Import')

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

        lbl1 = QLabel('Epoch Amount')
        lbl2 = QLabel('(the more you have, the more accurate the model is)')

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
        vbox.addWidget(lbl2)
        vbox.addWidget(train)
        vbox.addWidget(self.pbar)
        vbox.addWidget(self.start_btn)
        groupbox.setLayout(vbox)

        return groupbox


    def digitInsert(self):
        groupbox = QGroupBox('Insert Digits')

        self.blank = QPixmap('blank.jpg')
        lbl_img = QLabel()
        lbl_img.setPixmap(self.blank)
        self.pen = QPen(Qt.black, 3)
        
        

        vbox = QVBoxLayout()
        vbox.addWidget(lbl_img)

        vbox.addStretch(1)
        groupbox.setLayout(vbox)

        return groupbox

    def paintEvent(self, event):
        painter = QPainter(self)
        self.blank = QPixmap("blank.png")
        painter.drawPixmap(self.rect(), self.blank)
        
        painter.setPen(self.pen)


    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if event.buttons() and Qt.LeftButton and self.drawing:
            painter = QPainter(self.blank)
            painter.setPen(QPen(Qt.black, 3, Qt.SolidLine))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button == Qt.LeftButton:
            self.drawing = False

    




#creates the qapplication
parent = QApplication(sys.argv)

mainW = App()


#execute the qapplication
sys.exit(parent.exec())
