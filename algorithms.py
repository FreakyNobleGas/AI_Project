###########################################################################
###########################################################################
# Authors: Adrien Forkum, Nick Quinn, Karl Horlitz
# Date: 10/26/19
#
# Description: This file contains all of the algorithms needed for implementing
#              the AI agents.
#
###########################################################################
###########################################################################
import random

class genericAlgorithms:
	def __init__(self, agent_pos, c_map):
		# Create Algorithm
		self.agent_pos = (agent_pos[0],agent_pos[1])
		self.c_map = c_map
		self.wallList = c_map.get_map_bounds() + c_map.get_walls()
		#self.wallList.expand(c_map.get_walls())

	def move(self):
		# Random movement code
		x = (random.randrange(0,3,1)-1)
		y = (random.randrange(0,3,1)-1)

		# Update current agent position
		self.agent_pos= ((self.agent_pos[0] + x), (self.agent_pos[1] + y))

		# Undo move if collides with a wall
		print("p: ", self.agent_pos, " : ",self.wallList)
		if self.agent_pos in self.wallList:
			print("Collsiion")
			self.agent_pos= ((self.agent_pos[0] - x), (self.agent_pos[1] - y))

		return self.agent_pos

class DFS:
	def __init__(self):
		pass

class BFS:
	def __init__(self):
		pass

class Astar:
	def __init__(self):
		pass

class MinMax:
	def __init__(self):
		pass

class ExpMax:
	def __init__(self):
		pass
