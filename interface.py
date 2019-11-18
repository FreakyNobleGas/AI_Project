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
import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from agents import *
from algorithms import *
from maps import *

class mainWindow(QMainWindow):

    def __init__(self):
        # Required to start application
        app = QApplication([])

        # Creates a proxy object of the mainWindow class so that we can call
        # methods that we define below.
        super(mainWindow, self).__init__()

        # initial x, inital y, x dimension, y dimension
        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle("Multi-Agent Freeze-Tag")

        # Set program icon
        self.setWindowIcon(QIcon('images/predator-icon.png'))

        self.mainMenu = QVBoxLayout()
        self.mainMenu = self.createButtons(self.mainMenu)

        self.newGame = QVBoxLayout()

        QuitButton = QPushButton("Quit", self)
        QuitButton.clicked.connect(QCoreApplication.instance().quit)
        QuitButton.resize(600,100)
        QuitButton.move(100, 400)
        self.newGame.addWidget(QuitButton)

        self.show()
        app.exec_()

    def createButtons(self, tempLayout):

        NewGameButton = QPushButton("New Game", self)
        NewGameButton.clicked.connect(self.newGame)
        NewGameButton.resize(600, 100)
        NewGameButton.move(100, 100)

        HelpButton = QPushButton("Help", self)
        HelpButton.clicked.connect(self.help)
        HelpButton.resize(600, 100)
        HelpButton.move(100, 250)

        QuitButton = QPushButton("Quit", self)
        QuitButton.clicked.connect(QCoreApplication.instance().quit)
        QuitButton.resize(600,100)
        QuitButton.move(100, 400)

        tempLayout.addWidget(NewGameButton)
        tempLayout.addWidget(HelpButton)
        tempLayout.addWidget(QuitButton)

        return tempLayout

    def newGame(self):
        print("TODO: Add code for new game!")
        new_game = NewGameSettings(self)
        algorithms_foo()
        agents_foo()
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("TODO: Add code for new game!")
        msg.exec()


    def help(self):
        print("TODO: Add code for help functionality")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("TODO: Add code for help functionality")
        msg.exec()
    
class NewGameSettings(QMainWindow):
    def __init__(self, parent=None):
        super(NewGameSettings, self).__init__(parent)
        self.left = 100
        self.right = 100
        self.width = 800
        self.height = 600
        self.title = 'New Game'
        self.initUi()
        
    def initUi(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.right, self.width, self.height)
        self.menu = QVBoxLayout()
        self.menu = self.newGameButtons(self.menu)
        self.show()
        
    def newGameButtons(self, layout):
        SetMapButton = QPushButton("Choose Map", self)
        SetMapButton.clicked.connect(self.mapSelect)
        SetMapButton.resize(600, 100)
        SetMapButton.move(100, 100)
        
        SetAgentsButton = QPushButton("Set Agent Settings", self)
        SetAgentsButton.clicked.connect(self.agentSelect)
        SetAgentsButton.resize(600, 100)
        SetAgentsButton.move(100, 250)
        
        SetAlgorithmButton = QPushButton("Select Algorithm", self)
        SetAlgorithmButton.clicked.connect(self.algSelect)
        SetAlgorithmButton.resize(600, 100)
        SetAlgorithmButton.move(100, 400)
        
        layout.addWidget(SetMapButton)
        layout.addWidget(SetAgentsButton)
        layout.addWidget(SetAlgorithmButton)
    
    def mapSelect(self):
        print("Map select")
        gen_map = Map() 
        gen_map.map_foo()
        
    def agentSelect(self):
        print("Agent select")
        
    
    def algSelect(self):
        print("Algorithm select")

