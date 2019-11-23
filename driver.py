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
from gameengine import gameEngine, wallTile
from maps import Map
from agents import agent

class Driver:
    """
    Class that is used to run the program and contains all the game elements.
    """
    def __init__(self):
        self.map = None
        self.agents = {}
        self.algorithm = None
        self.driver_window()
        
    def driver_window(self):
        print("BEGIN MAIN")
        # mainWindow object contains c_map for map object , c_alg for algorithm object,
        # and a dictionary {'Hunter':[hunter obj list], 'Runner':[runner obj list].
        window = mainWindow()
        print (window.c_map)
        print (window.c_agents)
        print (window.c_alg)
        self.run_game(window.c_map, window.c_agents, window.c_alg)
        
    def formatter(self, c_map, c_agents, c_alg):
        agentList = []
        # Generate map object based on file path: c_map
        newMap = Map(c_map)
        # Generate list of wallTile objects based on coordinates from newMap
        wallList = [wallTile(i) for i in (newMap.get_walls()+newMap.get_map_bounds())]
        # Generate list of agent objects from dict c_agents
        for role, total in c_agents.items():
            for i in range(total):
                agentList.append(agent(c_map=newMap, c_alg=c_alg, _role=role))
        
        return newMap, wallList, agentList
        
    def run_game(self, c_map, c_agents, c_alg):
        newMap, wallList, agentList = self.formatter(c_map, c_agents, c_alg)
        gameEngine(agentList, wallList, newMap)

        
if __name__ == "__main__":
    run_driver = Driver()
