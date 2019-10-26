###########################################################################
###########################################################################
# Authors: Adrien Forkum, Nick Quinn, Karl Horlitz
# Date: 10/26/19
#
# Description: This file contains the graphic implementation of the game using
#              the PYQT5 libraries.
#
###########################################################################
###########################################################################

# Library Imports
from PyQt5.QtWidgets import QMainWindow, QFrame, QDesktopWidget, QApplication, QLabel
from PyQt5.QtCore import Qt, QBasicTimer, pyqtSignal
from PyQt5.QtGui import QPainter, QColor


class mainWindow(QMainWindow):

    def __init__(self):
        app = QApplication([])
        app.setGeometry(100,100,200,50)
        label = QLabel('Multi-Agent Freeze Tag')
        label.show()
        app.exec_()

        #super().__init__()

        #self.createUI()

'''
    def createUI(self):
        self.map = genericUI(self)
        self.setCentralWidget(self.map)

        #self.statusBar = self.statusBar()

        self.resize(180, 380)
        self.center()
        self.setWindowTitle("Freeze Tag")
        self.show()

    def center(self):


        screen = QDesktopWidget().screenGeometry()
        size = self.geometry()
        self.move((screen.width()-size.width())/2,
            (screen.height()-size.height())/2)




class genericUI(QFrame):
'''
