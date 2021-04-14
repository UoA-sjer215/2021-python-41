import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QToolTip
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication


class App (QWidget):
    def __init__ (self,num):
        super().__init__()

        if num==1 :
            self.main()
        elif num==2:
            self.train()
        elif num==3:
            self.insert()


    def ShowMain (self):
        self.hide()
        mainW.show()

    def ShowTrain (self):
        self.hide()
        trainW.show()

    def ShowInsert (self):
        self.hide()
        insertW.show()

    
    def main (self):
        self.setWindowTitle("main")
        self.move(300,300)
        self.setWindowIcon(QIcon('cat.jpg'))
        self.resize(300,600)

        train = QPushButton('train AI', self)
        train.move(50, 50)
        train.resize(train.sizeHint())
        train.clicked.connect(self.ShowTrain)

        insert = QPushButton('Insert digit', self)
        insert.move(50, 100)
        insert.resize(insert.sizeHint())
        insert.clicked.connect(self.ShowInsert)


        self.show()


    def train (self):
        self.setWindowTitle("training")
        self.move(600,300)
        self.setWindowIcon(QIcon('cat.jpg'))
        self.resize(300,600)

        main = QPushButton('Back to intro', self)
        main.move(50, 50)
        main.resize(main.sizeHint())
        main.clicked.connect(self.ShowMain)

        insert = QPushButton('Insert digit', self)
        insert.move(50, 100)
        insert.resize(insert.sizeHint())
        insert.clicked.connect(self.ShowInsert)

    
    def insert (self):
        self.setWindowTitle("inserting digits")
        self.move(900,300)
        self.setWindowIcon(QIcon('cat.jpg'))
        self.resize(300,600)

        train = QPushButton('train AI', self)
        train.move(50, 50)
        train.resize(train.sizeHint())
        train.clicked.connect(self.ShowTrain)

        main = QPushButton('Back to intro', self)
        main.move(50, 100)
        main.resize(main.sizeHint())
        main.clicked.connect(self.ShowMain)


#creates the qapplication
parent = QApplication(sys.argv)

mainW = App(1)
trainW = App(2)
insertW = App(3)


#execute the qapplication
sys.exit(parent.exec())
