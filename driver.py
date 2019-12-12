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
import argparse
from os import path
from interface import mainWindow
from gameengine import gameEngine, wallTile, safeTile
from maps import Map
from agents import agent
from datetime import datetime, timedelta
import sys

class GameScore:
	def __init__(self, agents_list):
		self.agentScoreMap = {}
		self.gameTime = None
		self.agents_list = agents_list
		self.scoreGame()
		self.printScore()
		self.toFile()
		
	def scoreGame(self):
		r_count, h_count = 1, 1
		
		for agent in self.agents_list:
			if agent.getType() is 'runner':
				#self.agentScoreMap[agent.getType()] = (agent.c_alg, self.agentScore(agent))
				self.agentScoreMap[agent.getType() + ' ' + str(r_count)] = (agent.c_alg, self.agentScore(agent))
				r_count += 1
			else:
				#self.agentScoreMap[agent.getType()] = (agent.c_alg, self.agentScore(agent))
				self.agentScoreMap[agent.getType() + ' ' + str(h_count)] = (agent.c_alg, self.agentScore(agent))
				h_count += 1
				
	def agentScore(self, agent):
		"""
		Scoring elements in agents:
		self.agentsKilled for hunters
		self.timeAlive is datetime object for total time alive
		self.endState  End state is how agent was ended the game (0 = alive at end, 1 = killed by hunter, 2 = safe zone exit, 3 = converted)
		self.totalEvalScore = 0.0 ***Not used yet***
		"""
		total = 0
		
		if agent.getType() is 'runner':
			try:
				time = agent.timeAlive
				total += int(timedelta(hours=time.hour, minutes=time.minute, seconds=time.second).total_seconds()) * 10.0
			except:
				total += int(agent.timeAlive.total_seconds()) * 10.0
			
			if agent.endState is 2:
				total += 10000.0
		else:
			try:
				time = agent.timeAlive
				total -= int(timedelta(hours=time.hour, minutes=time.minute, seconds=time.second).total_seconds()) / 60.0
			except:
				total -= int(agent.timeAlive.total_seconds()) / 60.0
			total += agent.agentsKilled * 1000.0
		
		return total
		
	def toFile(self):
		map_name = self.agents_list[0].c_map.map_name.split('/')[-1]
		map_name = map_name.replace('.txt','')
		with open("gameData/game_output.csv", "a") as output:
			for agent, values in self.agentScoreMap.items():
				output.write(map_name + ", " + str(len(self.agents_list)) + ", " + agent.split(' ')[0] + ", " + values[0] + ", " + str(values[1]) + "\n")
			output.close()
		
	def printScore(self):
		map_name = self.agents_list[0].c_map.map_name.split('/')[-1]
		map_name = map_name.replace('.txt','')
		print("Map: " + map_name + ":")
		for agent, values in self.agentScoreMap.items():
			print(agent + " <" + values[0] + "> ---> SCORE(" + str(values[1]) + ")")

class Driver:
    """
    Class that is used to run the program and contains all the game elements.
    """
    def __init__(self, test=False, map=None, agents={}, algorithm=None):
        self.map = map
        self.agents = agents
        self.algorithm = algorithm

        if test is True:
            self.run_game(self.map, self.agents, self.algorithm)
        else:
            self.driver_window()

    def driver_window(self):
        print("BEGIN MAIN")
        # mainWindow object contains c_map for map object , c_alg for algorithm object,
        # and a dictionary {'hunter': # of hunters, 'Runner': # of runners}.
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

        # Generate a list with all safezones
        safeList = [safeTile(i) for i in (newMap.get_safezone())]

        # Generate list of agent objects from dict c_agents
        for role, total in c_agents.items():
            for i in range(total):
                agentList.append(agent(c_map=newMap, c_agent_list=agentList, c_alg=c_alg, _role=role, _index = len(agentList)))

        return newMap, wallList, agentList, safeList

    def run_game(self, c_map, c_agents, c_alg):
        newMap, wallList, agentList, safeList = self.formatter(c_map, c_agents, c_alg)
        # Game time tracker
        game_start_time = datetime.now()
        gameEngine(agentList, wallList, newMap, safeList = safeList)
        game_end_time = datetime.now() - game_start_time
        score_total = GameScore(agentList)
        print("Total run time: ", game_end_time)
        sys.exit()
		
		
if __name__ == "__main__":
    # Parse Command Line Arguments
    parser = argparse.ArgumentParser()

    # Example: python3 driver.py --test <map_name> <# of hunters> <# of runners> <algorithm>
    parser.add_argument("-t", nargs=4,
                        help="Map Name should just be the file name. Algorithm choices are DFS, BFS,"
                        + " Astar, MinMax, ExpMax, or GA (Generic Algorithm).",
                        metavar=("<map_name>", "<# of hunters>", "<# of runners>", "<algorithm>"))
    # Holds all command line arguments
    args = parser.parse_args()

    # If -t flag was passed
    if args.t:
        t = args.t
        agents_dict={"hunter": int(t[1]), "runner": int(t[2])}
        map_file = path.dirname(path.realpath(__file__)) + "/maps/" + t[0] + ".txt"
        run_driver = Driver(test=True, map=map_file, agents=agents_dict, algorithm=t[3])
    else:
        run_driver = Driver()
