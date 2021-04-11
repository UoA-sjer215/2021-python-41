import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtGui import QIcon

class App (QWidget):
    def __init__ (self,num):
        super().__init__()

        if num==1 :
            self.main(name)
        elif num==2:
            self.main(name)
        elif num==3:
            self.main(name)


    
    def main (self):
        self.setWindowTitle("main")
        self.move(300,300)
        self.setWindowIcon(QIcon('cat.jpg'))
        self.resize(300,600)
        self.show()

    def train (self):
        self.setWindowTitle("training")
        self.move(300,300)
        self.setWindowIcon(QIcon('cat.jpg'))
        self.resize(300,600)
        self.show()
    
    def insert (self):
        self.setWindowTitle("inserting digits")
        self.move(300,300)
        self.setWindowIcon(QIcon('cat.jpg'))
        self.resize(300,600)
        self.show()


#creates the qapplication
parent = QApplication(sys.argv)

firstwindow = App(1)


#execute the qapplication
sys.exit(parent.exec())
