import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip, QLabel, QVBoxLayout, QGroupBox, QRadioButton, QCheckBox, QPushButton, QMenu, QGridLayout, QVBoxLayout, QProgressBar, QSpinBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QBasicTimer


epoch = 0


class App (QWidget):
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

    def training(self):
        groupbox = QGroupBox('Training Settings')

        spinbox = QSpinBox()
        spinbox.setRange(0, 15)
        spinbox.setSingleStep(2)        
        spinbox.valueChanged.connect(self.value_changed)

        lbl1 = QLabel('Epoch Amount')
        lbl2 = QLabel('(the more you have, the more accurate the model is)')

        train = QPushButton('NO PAIN NO TRAIN')

        pbar = QProgressBar(self)
        pbar.setGeometry(30, 40, 200, 25)

        btn = QPushButton('Start')
        btn.move(40, 80)

        
        

        vbox = QVBoxLayout()
        vbox.addWidget(lbl1)
        vbox.addWidget(spinbox)
        vbox.addWidget(lbl2)
        vbox.addWidget(train)
        vbox.addWidget(pbar)
        vbox.addWidget(btn)
        groupbox.setLayout(vbox)

        return groupbox


    def digitInsert(self):
        groupbox = QGroupBox('Insert Digits')

        # different push buttons
        pushbutton = QPushButton('Normal Button')
        togglebutton = QPushButton('Toggle Button')
        togglebutton.setCheckable(True)
        togglebutton.setChecked(True)
        flatbutton = QPushButton('Flat Button')
        flatbutton.setFlat(True)
        popupbutton = QPushButton('Popup Button')
        menu = QMenu(self)
        menu.addAction('First Item')
        menu.addAction('Second Item')
        menu.addAction('Third Item')
        menu.addAction('Fourth Item')
        popupbutton.setMenu(menu)

        vbox = QVBoxLayout()
        vbox.addWidget(pushbutton)
        vbox.addWidget(togglebutton)
        vbox.addWidget(flatbutton)
        vbox.addWidget(popupbutton)
        vbox.addStretch(1)
        groupbox.setLayout(vbox)

        return groupbox

    def value_changed(self):
        epoch = self.spinbox.value()




#creates the qapplication
parent = QApplication(sys.argv)

mainW = App()


#execute the qapplication
sys.exit(parent.exec())
