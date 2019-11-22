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
        # Required to run game
        self.c_map = None
        self.c_agent = {}
        self.c_alg = None
        self.new_game = None
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

        self.show()
        app.exec_()

    def createButtons(self, tempLayout):

        NewGameButton = QPushButton("New Game", self)
        NewGameButton.clicked.connect(self.newGame)
        NewGameButton.resize(600, 100)
        NewGameButton.move(100, 100)
        
        RunButton = QPushButton("Run Game", self)
        RunButton.clicked.connect(self.runGame)
        RunButton.resize(600, 100)
        RunButton.move(100, 210)

        HelpButton = QPushButton("Help", self)
        HelpButton.clicked.connect(self.help)
        HelpButton.resize(600, 100)
        HelpButton.move(100, 310)

        QuitButton = QPushButton("Quit", self)
        QuitButton.clicked.connect(QCoreApplication.instance().quit)
        QuitButton.resize(600,100)
        QuitButton.move(100, 410)

        tempLayout.addWidget(NewGameButton)
        tempLayout.addWidget(HelpButton)
        tempLayout.addWidget(RunButton)
        tempLayout.addWidget(QuitButton)

        return tempLayout

    def newGame(self):
        self.new_game = NewGameSettings(self)
        
    def runGame(self):
        if not self.new_game:
            print("New game not started")
            return
        elif not self.new_game.hunter_list:
            print("No hunters, Check 1 ", self.new_game.hunter_list)
            return
        elif not self.new_game.runner_list:
            print("No runners, Check 2")
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
            self.c_agent['Hunter'] = self.new_game.hunter_list
            self.c_agent['Runner'] = self.new_game.runner_list
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
        super(NewGameSettings, self).__init__(parent)
        self.left = 100
        self.right = 100
        self.width = 800
        self.height = 600
        self.title = 'New Game'
        self.s_map = None
        self.hunter_list = []
        self.runner_list = []
        self.s_alg = None
        self.alg_text = ''
        self.initUi()
        
    def initUi(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.right, self.width, self.height)
        self.menu = QVBoxLayout()
        self.menu = self.newGameButtons(self.menu)
        self.show()
        
    def newGameButtons(self, layout):
        buffer_len = 100
        
        self.SetMapButton = QPushButton("Choose Map", self)
        self.SetMapButton.clicked.connect(self.mapSelect)
        self.SetMapButton.resize((len("Choose Map") * 10), 100)
        self.SetMapButton.move(buffer_len, 100)
        buffer_len += 10 + (len("Choose Map") * 10)
        
        self.SetAgentsButton = QPushButton("Set Agent Settings", self)
        self.SetAgentsButton.clicked.connect(self.agentSelect)
        self.SetAgentsButton.resize(len("Set Agent Settings") * 10, 100)
        self.SetAgentsButton.move(buffer_len, 100)
        buffer_len += 10 + (len("Set Agent Settings") * 10)
        
        self.SetAlgorithmButton = QPushButton("Select Algorithm", self)
        self.SetAlgorithmButton.clicked.connect(self.algSelect)
        self.SetAlgorithmButton.resize((len("Set Agent Settings") * 10), 100)
        self.SetAlgorithmButton.move(buffer_len, 100)
        
        self.N_G_Done = QPushButton("Done", self)
        self.N_G_Done.clicked.connect(self.n_g_done)
        self.N_G_Done.resize(400, 100)
        self.N_G_Done.move(100, 400)
        
        layout.addWidget(self.SetMapButton)
        layout.addWidget(self.SetAgentsButton)
        layout.addWidget(self.SetAlgorithmButton)
        layout.addWidget(self.N_G_Done)
    
    def mapSelect(self):
        print("Map select")
        sel_map = FileMenu()
        if sel_map.selected_file is not None:
            map_title = sel_map.selected_file.split("/")
            self.SetMapButton.setText(map_title[-1].replace('.txt',''))
            self.s_map = Map(sel_map.selected_file)
        else:
            print("Map not selected: Add dailogbox to inform user", sel_map.selected_file)
        
    def agentSelect(self):
        print("Agent select")
        self.sel_agents = AgentSelect()
        
    def algSelect(self):
        print("Algorithm select")
        self.sel_alg = AlgSelect(self.SetAlgorithmButton)
        
    def n_g_done(self):
        if not self.sel_alg.getAlg() or not self.sel_agents.hunter_list or not self.sel_agents.runner_list or not self.s_map:
            print("Returned with no Values")
            self.close()
        else:
            self.s_alg = self.sel_alg.getAlg()
            self.hunter_list = self.sel_agents.hunter_list
            self.runner_list = self.sel_agents.runner_list
            self.close()
        
class AgentSelect(QMainWindow):
    def __init__(self, parent=None):
        super(AgentSelect, self).__init__(parent)
        self.left = 100
        self.right = 100
        self.width = 800
        self.height = 600
        self.title = 'Select Agents'
        self.hunter_list = []
        self.runner_list = []
        self.initUi()
        
    def initUi(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.right, self.width, self.height)
        self.menu = QVBoxLayout()
        self.menu = self.AgentButtons(self.menu)
        self.show()
        
    def AgentButtons(self, layout):
        self.AddHunter = QPushButton("Add Hunter", self)
        self.AddHunter.clicked.connect(lambda: self.addAgent("Hunter"))
        self.AddHunter.resize(len("Add Hunter") * 10, 100)
        self.AddHunter.move(100, 100)
        
        self.AddRunner = QPushButton("Add Runner", self)
        self.AddRunner.clicked.connect(lambda: self.addAgent("Runner"))
        self.AddRunner.resize(len("Add Runner") * 10, 100)
        self.AddRunner.move(100, 250)
        
        self.DeleteHunter = QPushButton("Delete Hunter", self)
        self.DeleteHunter.clicked.connect(lambda: self.delAgent("Hunter"))
        self.DeleteHunter.resize(len("Delete Hunter") * 10, 100)
        self.DeleteHunter.move(200, 100)
        
        self.DeleteRunner = QPushButton("Delete Runner", self)
        self.DeleteRunner.clicked.connect(lambda: self.delAgent("Runner"))
        self.DeleteRunner.resize(len("Delete Runner") * 10, 100)
        self.DeleteRunner.move(200, 250)
        
        self.A_B_Done = QPushButton("Done", self)
        self.A_B_Done.clicked.connect(self.close)
        self.A_B_Done.resize(600, 100)
        self.A_B_Done.move(100, 400)
        
        self.HunterLabel = QLabel(self)
        self.HunterLabel.setAlignment(Qt.AlignCenter)
        self.HunterLabel.setText("Hunters: 0")
        self.HunterLabel.move(400,100)
        
        self.RunnerLabel = QLabel(self)
        self.RunnerLabel.setAlignment(Qt.AlignCenter)
        self.RunnerLabel.setText("Runners: 0")
        self.RunnerLabel.move(400,250)
        
        layout.addWidget(self.AddHunter)
        layout.addWidget(self.AddRunner)
        layout.addWidget(self.DeleteHunter)
        layout.addWidget(self.DeleteRunner)
        layout.addWidget(self.A_B_Done)
        layout.addWidget(self.HunterLabel)
        layout.addWidget(self.RunnerLabel)
            
    def addAgent(self, agent):
        if agent is 'Hunter':
            self.hunter_list.append(Hunter())
            self.HunterLabel.setText("Hunters: " + str(len(self.hunter_list)))
        elif agent is 'Runner':
            self.runner_list.append(Runner())
            self.RunnerLabel.setText("Runners: " + str(len(self.runner_list)))
            
    def delAgent(self, agent):
        if agent is 'Hunter' and len(self.hunter_list) != 0:
            self.hunter_list.pop(-1)
            self.HunterLabel.setText("Hunters: " + str(len(self.hunter_list)))
        elif agent is 'Runner' and len(self.runner_list) != 0:
            self.runner_list.pop(-1)
            self.RunnerLabel.setText("Runners: " + str(len(self.runner_list)))
            
    def getAgents(self):
        return self.hunter_list, self.runner_list
        
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
            
class AlgSelect(QMainWindow):
    def __init__(self, obj):
        super(AlgSelect, self).__init__()
        self.left = 100
        self.right = 100
        self.width = 800
        self.height = 600
        self.title = 'Select Algorithm'
        self.alg = None
        self.obj = obj
        self.initUi()
        
    def initUi(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.right, self.width, self.height)
        self.menu = QVBoxLayout()
        self.menu = self.AlgButtons(self.menu)
        self.show()
    
    def AlgButtons(self, layout):
        def name_len(name):
            return (len(name) * 10) + (100 - (len(name) * 10))
        
        buffer_len = 100
        dist_len = 0
        self.DFSButton = QPushButton("DFS", self)
        self.DFSButton.clicked.connect(lambda: self.selectAlg("DFS"))
        self.DFSButton.resize(name_len("DFS"), 100)
        self.DFSButton.move(buffer_len, 100 + dist_len)
        buffer_len += 10 + name_len("DFS")
        
        self.BFSButton = QPushButton("BFS", self)
        self.BFSButton.clicked.connect(lambda: self.selectAlg("BFS"))
        self.BFSButton.resize(name_len("BFS"), 100)
        self.BFSButton.move(buffer_len, 100 + dist_len)
        buffer_len += 10 + name_len("BFS")
        
        self.AStarButton = QPushButton("A*", self)
        self.AStarButton.clicked.connect(lambda: self.selectAlg("A*"))
        self.AStarButton.resize(name_len("A*"), 100)
        self.AStarButton.move(buffer_len, 100 + dist_len)
        buffer_len += 10 + name_len("A*")
        
        buffer_len = 100
        dist_len = 100
        self.MinMaxButton = QPushButton("Min Max", self)
        self.MinMaxButton.clicked.connect(lambda: self.selectAlg("Min Max"))
        self.MinMaxButton.resize(name_len("Min Max"), 100)
        self.MinMaxButton.move(buffer_len, 100 + dist_len)
        buffer_len += 10 + name_len("Min Max")
        
        self.ExpMaxButton = QPushButton("Expected Max", self)
        self.ExpMaxButton.clicked.connect(lambda: self.selectAlg("Expected Max"))
        self.ExpMaxButton.resize(name_len("Expected Max"), 100)
        self.ExpMaxButton.move(buffer_len, 100 + dist_len)
        
        self.Al_Done = QPushButton("Done", self)
        self.Al_Done.clicked.connect(self.close)
        self.Al_Done.resize(400, 100)
        self.Al_Done.move(100, 400)
        
        layout.addWidget(self.DFSButton)
        layout.addWidget(self.BFSButton)
        layout.addWidget(self.AStarButton)
        layout.addWidget(self.MinMaxButton)
        layout.addWidget(self.ExpMaxButton)
        layout.addWidget(self.Al_Done)
    
    def selectAlg(self, selected_alg):
        self.obj.setText(selected_alg)
        if selected_alg == 'DFS':
            self.alg = DFS()
        elif selected_alg == 'BFS':
            self.alg = BFS()
        elif selected_alg == 'A*':
            self.alg = Astar()
        elif selected_alg == 'Min Max':
            self.alg = MinMax()
        elif selected_alg == 'Expected Max':
            self.alg = ExpMax()
        else:
            print("NO ALGORITHM")
            
    def getAlg(self):
        return self.alg
            
