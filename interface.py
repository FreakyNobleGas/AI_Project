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
        new_game = NewGameSettings(self)
        


    def help(self):
        print("TODO: Add code for help functionality")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("TODO: Add code for help functionality")
        msg.exec_()
    
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
        self.SetMapButton = QPushButton("Choose Map", self)
        self.SetMapButton.clicked.connect(self.mapSelect)
        self.SetMapButton.resize(600, 100)
        self.SetMapButton.move(100, 100)
        
        self.SetAgentsButton = QPushButton("Set Agent Settings", self)
        self.SetAgentsButton.clicked.connect(self.agentSelect)
        self.SetAgentsButton.resize(600, 100)
        self.SetAgentsButton.move(100, 250)
        
        self.SetAlgorithmButton = QPushButton("Select Algorithm", self)
        self.SetAlgorithmButton.clicked.connect(self.algSelect)
        self.SetAlgorithmButton.resize(600, 100)
        self.SetAlgorithmButton.move(100, 400)
        
        layout.addWidget(self.SetMapButton)
        layout.addWidget(self.SetAgentsButton)
        layout.addWidget(self.SetAlgorithmButton)
    
    def mapSelect(self):
        print("Map select")
        sel_map = FileMenu()
        map_title = sel_map.selected_file.split("/")
        self.SetMapButton.setText(map_title[-1].replace('.txt',''))
        gen_map = Map(sel_map.selected_file)
        print("Map is: ", gen_map.map_name) 
        
    def agentSelect(self):
        print("Agent select")
        
    
    def algSelect(self):
        print("Algorithm select")
        
class FileMenu(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Select Map'
        self.left = 10
        self.top = 10
        self.width = 640
        self.height = 480
        self.selected_file = ''
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        self.openFileNameDialog()
        
        self.show()
    
    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, 
            "Map Select",
            "",
            "All Files (*);;Python Files (*.py)",
            options=options)
        if fileName:
            self.selected_file = fileName
    
    def openFileNamesDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        files, _ = QFileDialog.getOpenFileName(self, 
            "QFileDialog.getOpenFileNames()",
            "",
            "All Files (*);;Python Files (*.py)",
            options=options)
        if files:
            print(files)
            
    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, 
            "QFileDialog.getSaveFileName()",
            "",
            "All Files (*);;Text Files (*.txt)",
            options=options)
        if fileName:
            print(fileName)
