# hello
#hello again
#feature C created
import Network
import gui
import sys

if __name__ == '__main__':
    #creates the qapplication
    parent = gui.QApplication(sys.argv)

    mainW = gui.App(1)
    trainW = gui.App(2)
    insertW = gui.App(3)

    #execute the qapplication
    sys.exit(parent.exec())
