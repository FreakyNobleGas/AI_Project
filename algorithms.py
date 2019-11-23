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
		self.facing = 0 

	def move(self):
		# Old Random movement code
		#x = (random.randrange(0,3,1)-1)
		#y = (random.randrange(0,3,1)-1)
		d = (random.randrange(0,3,1)) # Increase the max to decrease odds of turning
		if d == 0: # turn Left
			print("R")
			self.facing -=0.5
			if self.facing <0:
				self.facing = 3.5
		elif d == 1:
			print("L")
			self.facing +=0.5
			if self.facing > 3.5:
				self.facing = 0
		
		# Take Step in Direction
		print("S: ",self.facing)
		if self.facing == 0:
			x = 1
			y = 0
		elif self.facing == 0.5:
			x = 1
			y = -1
		elif self.facing == 1:
			x = 0
			y = -1
		elif self.facing == 1.5:
			x = -1
			y = -1
		elif self.facing == 2:
			x = -1
			y = 0
		elif self.facing == 2.5:
			x = -1
			y = 1
		elif self.facing == 3:
			x = 0
			y = 1
		else:# facing = 3.5:
			x = 1
			y = 1
			

		# Update current agent position
		self.agent_pos= ((self.agent_pos[0] + x), (self.agent_pos[1] + y))

		# Undo move if collides with a wall
		#print("p: ", self.agent_pos, " : ",self.wallList)
		if self.agent_pos in self.wallList:
			#print("Collsiion")
			self.agent_pos= ((self.agent_pos[0] - x), (self.agent_pos[1] - y))

		return (self.agent_pos, self.facing)

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
