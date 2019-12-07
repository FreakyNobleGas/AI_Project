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
from os import listdir, path
from os.path import isfile, join
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from agents import *
from algorithms import *
from maps import *

class mainWindow(QMainWindow):

    def __init__(self):
        # Required to run game
        self.c_map = None
        self.c_agents = {}
        self.c_alg = None
        self.new_game = NewGameSettings(self)
        self.opened_new_game = False

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

        # Create main menu
        self.mainMenu = QVBoxLayout()
        self.mainMenu = self.createButtons(self.mainMenu)

        self.show()
        app.exec_()

    def createButtons(self, tempLayout):

        NewGameButton = QPushButton("New Game", self)
        NewGameButton.setStyleSheet("background-color:rgb(50, 168, 82)")
        NewGameButton.clicked.connect(self.newGame)
        NewGameButton.resize(600, 100)
        NewGameButton.move(100, 100)

        RunButton = QPushButton("Run Game", self)
        RunButton.setStyleSheet("background-color:rgb(69, 120, 222)")
        RunButton.clicked.connect(self.runGame)
        RunButton.resize(600, 100)
        RunButton.move(100, 210)

        HelpButton = QPushButton("Help", self)
        HelpButton.setStyleSheet("background-color:rgb(255, 239, 0)")
        HelpButton.clicked.connect(self.help)
        HelpButton.resize(600, 100)
        HelpButton.move(100, 310)

        QuitButton = QPushButton("Quit", self)
        QuitButton.setStyleSheet("background-color:rgb(219, 15, 15)")
        QuitButton.clicked.connect(QCoreApplication.instance().quit)
        QuitButton.resize(600,100)
        QuitButton.move(100, 410)

        tempLayout.addWidget(NewGameButton)
        tempLayout.addWidget(HelpButton)
        tempLayout.addWidget(RunButton)
        tempLayout.addWidget(QuitButton)

        return tempLayout

    # Create new window with new game settings
    def newGame(self):
        super(NewGameSettings, self.new_game).__init__()
        self.new_game.initUi()

    def runGame(self):
        if not self.new_game:
            print("New game not started")
            return
        elif not self.new_game.agent_list:
            print("No agents, Check 1 ")
            return
        elif self.new_game.s_alg is None:
            print("No algorithm, Check 3")
            return
        elif self.new_game.s_map is None:
            print("No map, Check 4")
            return
        else:
            print("Game is ready!")
            self.c_map = self.new_game.s_map
            self.c_agents = self.new_game.agent_list
            self.c_alg = self.new_game.s_alg
            self.close()

    def help(self):
        print("TODO: Add code for help functionality")
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Information)
        msg.setText("TODO: Add code for help functionality")
        msg.exec_()

class NewGameSettings(QMainWindow):
    def __init__(self, parent=None):
        # Basic Window Settings
        self.left = 100
        self.right = 100
        self.width = 800
        self.height = 600
        self.title = 'New Game'

        # Holds all game information to be passed to game engine
        self.s_map = None
        self.agent_list = {'hunter':0, 'runner':0}
        self.s_alg = None

    def initUi(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.right, self.width, self.height)

        # Create layouts for each setting: Map, Agents, and Algorithm
        self.menu = self.newGameButtons(QVBoxLayout())
        self.mapMenuLayout = self.mapMenu(QVBoxLayout())
        self.agentButtons = self.AgentButtons(QVBoxLayout())
        self.algorithmMenu = self.algorithMenu(QVBoxLayout())

        self.show()

    def newGameButtons(self, layout):
        buffer_len = 100

        self.MapTitle = QLabel(self)
        self.MapTitle.setText("Select Map")
        self.MapTitle.resize((len("Select Map") * 10), 50)
        self.MapTitle.move(100, 100)

        self.AgentTitle = QLabel(self)
        self.AgentTitle.setText("Select Agents")
        self.AgentTitle.resize((len("Select Agents") * 10), 50)
        self.AgentTitle.move(100, 200)

        self.AlgorithmTitle = QLabel(self)
        self.AlgorithmTitle.setText("Select Algorithm")
        self.AlgorithmTitle.resize((len("Select Algorithm") * 10), 50)
        self.AlgorithmTitle.move(100, 300)

        self.doneButton = QPushButton("Save Game Settings", self)
        self.doneButton.clicked.connect(self.new_game_done)
        self.doneButton.resize(300, 100)
        self.doneButton.move(225, 400)

        layout.addWidget(self.doneButton)

    # Check if all fields have been specified
    def new_game_done(self):
        if self.s_map is None:
            print("No map selected!")
        if self.agent_list is {'hunter':0, 'runner':0}:
            print("Agents are not specified!")
        if self.s_alg is None:
            print("Algorithm not specified!")

        self.close()

    # Update map selction after the user selects a new map in the drop down menu
    def updateMap(self):
        self.s_map = path.dirname(path.realpath(__file__)) + "/maps/" + str(self.mapDropDownMenu.currentText())

    def mapMenu(self, layout):
        self.mapDropDownMenu = QComboBox(self)

        # Go into the maps directory and insert every map file name into a list for the user to select
        mapDir = path.dirname(path.realpath(__file__)) + "/maps/"
        mapFiles = [f for f in listdir(mapDir) if isfile(join(mapDir, f))]

        for f in mapFiles:
            self.mapDropDownMenu.addItem(f)

        # Set map to first item in list until user changes it
        self.s_map = path.dirname(path.realpath(__file__)) + "/maps/" + str(self.mapDropDownMenu.currentText())
        self.mapDropDownMenu.currentIndexChanged.connect(self.updateMap)
        self.mapDropDownMenu.resize(150, 50)
        self.mapDropDownMenu.move(250, 110)

    # Update algorithm selection after the user selects a new algorithm in the drop down menu
    def updateAlgorithm(self):
        self.s_alg = str(self.algorithmDropDownMenu.currentText())

    def algorithMenu(self, layout):
        self.algorithmDropDownMenu = QComboBox(self)
        self.algorithmDropDownMenu.addItem("DFS")
        self.algorithmDropDownMenu.addItem("BFS")
        self.algorithmDropDownMenu.addItem("A*")
        self.algorithmDropDownMenu.addItem("MinMax")
        self.algorithmDropDownMenu.addItem("ExpectiMax")

        # Set algorithm to first item in the list until user changes it
        self.s_alg = str(self.algorithmDropDownMenu.currentText())
        self.algorithmDropDownMenu.currentIndexChanged.connect(self.updateAlgorithm)
        self.algorithmDropDownMenu.move(250, 310)

    def AgentButtons(self, layout):

        self.AddHunter = QPushButton("Add Hunter", self)
        self.AddHunter.clicked.connect(lambda: self.addAgent("hunter"))
        self.AddHunter.setStyleSheet("background-color:rgb(66, 245, 69)")
        self.AddHunter.resize(len("Add Hunter") * 10, 50)
        self.AddHunter.move(250, 175)

        self.AddRunner = QPushButton("Add Runner", self)
        self.AddRunner.clicked.connect(lambda: self.addAgent("runner"))
        self.AddRunner.setStyleSheet("background-color:rgb(66, 245, 69)")
        self.AddRunner.resize(len("Add Runner") * 10, 50)
        self.AddRunner.move(250, 225)

        self.DeleteHunter = QPushButton("Delete Hunter", self)
        self.DeleteHunter.clicked.connect(lambda: self.delAgent("hunter"))
        self.DeleteHunter.setStyleSheet("background-color:rgb(245, 69, 66)")
        self.DeleteHunter.resize(len("Delete Hunter") * 10, 50)
        self.DeleteHunter.move(350, 175)

        self.DeleteRunner = QPushButton("Delete Runner", self)
        self.DeleteRunner.clicked.connect(lambda: self.delAgent("runner"))
        self.DeleteRunner.setStyleSheet("background-color:rgb(245, 69, 66)")
        self.DeleteRunner.resize(len("Delete Runner") * 10, 50)
        self.DeleteRunner.move(350, 225)

        self.HunterLabel = QLabel(self)
        self.HunterLabel.setAlignment(Qt.AlignCenter)
        self.HunterLabel.setText("Hunters: " + str(self.agent_list["hunter"]))
        self.HunterLabel.move(500, 185)

        self.RunnerLabel = QLabel(self)
        self.RunnerLabel.setAlignment(Qt.AlignCenter)
        self.RunnerLabel.setText("Runners: " + str(self.agent_list["runner"]))
        self.RunnerLabel.move(500, 230)

        layout.addWidget(self.AddHunter)
        layout.addWidget(self.AddRunner)
        layout.addWidget(self.DeleteHunter)
        layout.addWidget(self.DeleteRunner)
        layout.addWidget(self.HunterLabel)
        layout.addWidget(self.RunnerLabel)

    def addAgent(self, agent):
        self.agent_list[agent] += 1
        self.HunterLabel.setText("Hunters: " + str(self.agent_list['hunter']))
        self.RunnerLabel.setText("Runners: " + str(self.agent_list['runner']))

    def delAgent(self, agent):
        if self.agent_list[agent] is not 0:
            self.agent_list[agent] -= 1
            self.HunterLabel.setText("Hunters: " + str(self.agent_list['hunter']))
            self.RunnerLabel.setText("Runners: " + str(self.agent_list['runner']))
