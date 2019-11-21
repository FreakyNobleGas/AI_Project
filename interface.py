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
        self.s_map = None
        self.s_agents = []
        self.s_alg = None
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
        self.gen_map = Map(sel_map.selected_file)
        print("Map is: ", gen_map.map_name) 
        
    def agentSelect(self):
        print("Agent select")
        sel_agents = AgentSelect(self)
        self.s_agents = sel_agents.agent_list
        
    def algSelect(self):
        print("Algorithm select")
        
class AgentSelect(QMainWindow):
    def __init__(self, parent=None):
        super(AgentSelect, self).__init__(parent)
        self.left = 100
        self.right = 100
        self.width = 800
        self.height = 600
        self.title = 'Select Agents'
        self.agent_list = []
        self.initUi()
        
    def initUi(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.right, self.width, self.height)
        self.menu = QVBoxLayout()
        self.menu = self.AgentButtons(self.menu)
        self.show()
        
    def AgentButtons(self, layout):
        HunterAgent = QPushButton("Add Hunter", self)
        HunterAgent.clicked.connect(lambda: self.addAgent("Hunter"))
        HunterAgent.resize(100, 100)
        HunterAgent.move(100, 100)
        
        RunnerAgent = QPushButton("Add Runner", self)
        RunnerAgent.clicked.connect(lambda: self.addAgent("Runner"))
        RunnerAgent.resize(100, 100)
        RunnerAgent.move(100, 250)
        
        self.HunterLabel = QLabel()
        self.HunterLabel.setAlignment(Qt.AlignCenter)
        self.HunterLabel.setText("0")
        self.HunterLabel.move(400,100)
        
        self.RunnerLabel = QLabel()
        self.RunnerLabel.setAlignment(Qt.AlignCenter)
        self.RunnerLabel.setText("0")
        self.RunnerLabel.move(400,250)
        
        layout.addWidget(self.HunterLabel, 0, 0)
        layout.addWidget(self.RunnerLabel, 0, 0)
        layout.addWidget(HunterAgent)
        layout.addWidget(RunnerAgent)
        
        #agent_params = {"Hunter":lambda: self.addAgent("Hunter"), "Runner": lambda: self.addAgent("Runner")}
        #agent_buttons = GenButtons(params=agent_params, layout=layout)
        #for agent, func in agent_buttons.button_map.items():
        #    print(agent,' ',func)
        #    layout.addWidget(func)
            
    def addAgent(self, agent):
        if agent is 'Hunter':
            self.agent_list.append(Hunter())
        elif agent is 'Runner':
            self.agent_list.append(Runner())
        
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
            
class GenButtons(QWidget):
    def __init__(self, params, parent=None, layout=None):
        """
        :input: Params is a dictionary containing key value pair of (button text : button function)
        """
        super(GenButtons, self).__init__(parent)
        self.params = params
        self.layout = layout
        self.button_map = {}
        self.createButtons()
    
    def createButtons(self):
        button_space = 0
        for name, func in self.params.items():
            button = QPushButton(name, self)
            button.clicked.connect(func)
            button.resize(600,100)
            button.move(100,100 + button_space)
            self.layout.addWidget(button)
            self.saveButton(button)
            button_space += 150
    
    def saveButton(self, obj):
        self.button_map[obj.text()] = obj
        
    def findButtonByText(self, text):
        return self.button_map[text]
