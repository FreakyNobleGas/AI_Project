###########################################################################
###########################################################################
# Authors: Adrien Forkum, Nick Quinn, Karl Horlitz
# Date: 10/26/19
#
# Description: This file is the start point for the entire program and contains
#              all neccessary library imports and driver code to execute the program.
#
# Requirements: Python3.5 or higher. PYQT5 graphics library installed.
#
# Usage: Python3 driver.py
###########################################################################
###########################################################################

# Library Imports
from interface import mainWindow
from gameengine import gameEngine

class Driver:
    """
    Class that is used to run the program and contains all the game elements.
    """
    def __init__(self):
        self.map = None
        self.agents = []
        self.algorithm = None
        self.driver_window()
        
    def driver_window(self):
        print("BEGIN MAIN")
        # mainWindow object contains c_map for map object , c_alg for algorithm object,
        # and a dictionary {'Hunter':[hunter obj list], 'Runner':[runner obj list].
        window = mainWindow()
        print (window.c_map)
        print (window.c_agent)
        print (window.c_alg)
        self.run_game(window.c_map, window.c_agent, window.c_alg)
        
    def run_game(self, c_map, c_agent, c_alg):
        agentList = []
        wallList = []
        for agent, agent_list in c_agent.items():
            agentList.extend(agent_list)
        for i in c_map.get_walls():
            wallList.append(wallTile(i))
        gameEngine(agentList,wallList)

        
if __name__ == "__main__":
    run_driver = Driver()
