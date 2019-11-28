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

class baseAlgorithm:
	def __init__(self, agent_pos, c_map, agent_list = None, listIndex = None):
		self.agent_pos = (agent_pos[0],agent_pos[1])
		self.c_map = c_map
		self.wallList = c_map.get_map_bounds() + c_map.get_walls()
		self.facing = 0 
		self.agent_list = agent_list

	def isValidMove(self,plannedPosition):
		# takes a position, and returns if the move would collide with 
		# a world object.  Needed for the algorithms
		if plannedPosition in self.wallList:
			#print("isValidMove wall collision")
			return False
		return True
		
	def manhattanDistance(self,pos1,pos2):
		# If I understand it correctly, Manhattan Distance is the
		# x-delta + y-delta
		return (abs(pos1[0]-pos2[0])+abs(pos1[1]-pos2[1]))
	
	def cardinalDir(self):
		# will ultimately return the rough (N-S-E-W) direction to 
		# the nearest runner in agent_list
		# to simulate basic "hearing"
		# this could be expanded to use diagonals, but may overly
		#expand the scope of the project
		None


class genericAlgorithms(baseAlgorithm):
	# This generic algorithm is a basic structure to show how to 
	# interface between the agent and algorithm in a way that the game
	# engine can use the data
	def __init__(self, agent_pos, c_map):
		# Create Algorithm
		self.agent_pos = (agent_pos[0],agent_pos[1])
		self.c_map = c_map
		self.wallList = c_map.get_map_bounds() + c_map.get_walls()
		#self.wallList.expand(c_map.get_walls())
		self.facing = 0 

	def move(self,unusedPos = None):
		d = (random.randrange(0,3,1)) 
		# Increase the max to decrease odds of turning
		if d == 0: # turn Left
			#print("R")
			self.facing -=0.5
			if self.facing <0:
				self.facing = 3.5
		elif d == 1:
			#print("L")
			self.facing +=0.5
			if self.facing > 3.5:
				self.facing = 0
		
		# Take Step in Direction
		#print("S: ",self.facing)
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
			
		# Old movement check code - moved into baseAlgorithm.isValidMove()
		# Update current agent position OLD. 
		#self.agent_pos= ((self.agent_pos[0] + x), (self.agent_pos[1] + y))
		# Undo move if collides with a wall
		#print("p: ", self.agent_pos, " : ",self.wallList)
		#if self.agent_pos in self.wallList:
			#print("Collsiion")
			#self.agent_pos= ((self.agent_pos[0] - x), (self.agent_pos[1] - y))
		if self.isValidMove(((self.agent_pos[0] + x), (self.agent_pos[1] + y))):
			self.agent_pos= ((self.agent_pos[0] + x), (self.agent_pos[1] + y))

		return (self.agent_pos, self.facing)



class testAlgorithm(baseAlgorithm):
	def __init__(self, agent_pos, c_map, c_agent_list,listIndex):
		self.agent_pos = (agent_pos[0],agent_pos[1])
		self.c_map = c_map
		self.wallList = c_map.get_map_bounds() + c_map.get_walls()
		self.facing = 0 
		self.agent_list = c_agent_list
		#print("Ag: ",self.agent_list)
		
	def move(self,unusedPos=None):
		# get best direction from current position
		# then step in that direction
		newPos = self.bestDir(self.agent_pos, 5) # 
		#print("NP:",newPos)
		self.agent_pos = (newPos[0],newPos[1])
		return self.agent_pos,0
	
	def bestDir(self,pPos,remainingDepth):
		pList = []
		bestPos = 0
		bestVal = 999999999
		# up: 0 -1
		# dn: 0 +1
		# lf: -1 0
		# rt: +1 0
		# this set initializes the NSEW squares in a list, if valid
		# There is probably a better way to do this
		if self.isValidMove(((pPos[0]),(pPos[1]-1))):
			pList.append((((pPos[0]),(pPos[1]-1)),999999999))
		if self.isValidMove(((pPos[0]),(pPos[1]+1))):
			pList.append((((pPos[0]),(pPos[1]+1)),999999999))
		if self.isValidMove(((pPos[0]-1),(pPos[1]))):
			pList.append((((pPos[0]-1),(pPos[1])),999999999))
		if self.isValidMove(((pPos[0]+1),(pPos[1]))):
			pList.append((((pPos[0]+1),(pPos[1])),999999999))
		# all valid positions now in a list
		#print( "PL ", pList)
		# pList is [((x,y),manhattanDist),...]
		for i in range(0,len(pList)):
			# for each square, go through list of agents, finding the closest
			bestVal = 99999999
			for agent in self.agent_list:
				# find closest agent's distance
				agentVal = self.manhattanDistance(pList[i][0], agent.getPos())
				#print("pp ",pList[i][0]," ap ", agent.getPos()," ",agentVal)
				if (agentVal < bestVal) and not(agent.getType() == "hunter"):
					# NOTE: this is currently set as a dedicated hunter-only
					# algorithm.  only works for hunters chasing runners
					# (to avoid chasing itself and not moving)
					bestVal = agentVal
			pList[i] = ((pList[i][0]),bestVal)
			# the above loop should find the closest agent to that position,
			# and sets the value for the position being checked to that
			# value
		bestIndex = None
		bestVal = 999999999
		for i in range(0,len(pList)):
			if ((pList[i][1]) < bestVal):
				bestVal = pList[i][1]
				bestIndex = i
		#print("PL ", pList, " BI ", pList[bestIndex])
		return pList[bestIndex][0]


class Reflex(baseAlgorithm):
	def __init__(self, agent_pos, c_map, c_agent_list, randomness, listIndex):
		self.agent_pos = (agent_pos[0],agent_pos[1])
		self.c_map = c_map
		self.wallList = c_map.get_map_bounds() + c_map.get_walls()
		self.facing = 0 
		self.agent_list = c_agent_list
		self.rand = randomness
		self.lIndex = listIndex
		#randomness is the chance to go in a random direction
		
		
	def move(self,unusedPos=None):
		# get best direction from current position
		# then step in that direction
		newPos = self.bestDir(self.agent_pos)
		self.agent_pos = (newPos[0],newPos[1])
		return self.agent_pos,0
	
	def bestDir(self,pPos):
		pList = []
		bestPos = 0
		bestVal = 999999999
		# up: 0 -1
		# dn: 0 +1
		# lf: -1 0
		# rt: +1 0
		# this set initializes the NSEW squares in a list, if valid
		# There is probably a better way to do this
		if self.isValidMove(((pPos[0]),(pPos[1]-1))):
			pList.append((((pPos[0]),(pPos[1]-1)),999999999))
		if self.isValidMove(((pPos[0]),(pPos[1]+1))):
			pList.append((((pPos[0]),(pPos[1]+1)),999999999))
		if self.isValidMove(((pPos[0]-1),(pPos[1]))):
			pList.append((((pPos[0]-1),(pPos[1])),999999999))
		if self.isValidMove(((pPos[0]+1),(pPos[1]))):
			pList.append((((pPos[0]+1),(pPos[1])),999999999))
		# all valid positions now in a list
		# pList is [((x,y),manhattanDist),...]
		# manhattanDist val is init as a very large value, vastly larger
		# than expected max paths
		if (self.rand >= (random.randrange(0,100,1))):
			# random move with self.rand as the threshold
			return pList[random.randrange(0,len(pList),1)][0]
		
		# else keep going
		for i in range(0,len(pList)):
			# for each square, go through list of agents, finding the closest
			bestVal = 99999999
			for agent in self.agent_list:
				# find closest agent's distance
				agentVal = self.manhattanDistance(pList[i][0], agent.getPos())
				#if (agentVal < bestVal) and not(agent.getType() == "hunter"): # old hardcoded check
				if (agentVal < bestVal) and not(agent.getType() == self.agent_list[self.lIndex].getType()):
					# NOTE: this is currently set as a dedicated hunter-only
					# algorithm.  only works for hunters chasing runners
					# (to avoid chasing itself and not moving)
					bestVal = agentVal
			pList[i] = ((pList[i][0]),bestVal)
			# the above loop should find the closest agent to that position,
			# and sets the value for the position being checked to that
			# value
		bestIndex = None
		bestVal = 999999999
		for i in range(0,len(pList)):
			if ((pList[i][1]) < bestVal):
				bestVal = pList[i][1]
				bestIndex = i
		#print("PL ", pList, " BI ", pList[bestIndex])
		return pList[bestIndex][0]



				
class DFS:
	# NOTE: DFS may not work well in this setup- need a map with paths
	# to be able to limit depth paths (and avoid looping)
	def __init__(self, agent_pos, c_map, c_agent_list, listIndex):
		self.current_pos = agent_pos
		self.c_map = c_map
		self.agents = c_agent_list
		self.lIndex = listIndex
		
	def move(self, cur_pos):
		# Caller function for dfs
		return self.dfs(cur_pos, self.c_map, self.agents)
		
	def dfs(self):
		"""
		Depth First Search algorithm.
		
		:agent_pos: Current agent position, (x, y) tuple.
		
		:c_map: Map object for obtaining walls, boundries, and safe zones.
		
		:c_agent_list: List of agent objects for iterating through and finding next moves of each agent.
		"""
		visited = []
		path = []
		current_pos = (agent_pos[0], agent_pos[1])
		for agent in self.agents: 
			pos_form = agent.getPos()
			if (pos_form[0] == current_pos[0]) and (pos_form[1] == current_pos[1]):
				current_agent = agent
		visited.append(current_pos)
		path.append((current_pos, 0))
		while path:
			flag = True
			possible_moves = self.c_map.get_next(current_pos)
			for move, direction in possible_moves:
				if current_agent.isGoal(move):
					path.append((move, direction))
					return path
				elif move not in visited:
					flag = False
					visited.append(move)
					path.append((move, direction))
					current_pos = move
					break
			if flag:
				path.pop(-1)
				if path:
					current_pos = path[-1][0]
				

class BFS:
	def __init__(self, agent_pos, c_map, c_agent_list,listIndex):
		self.current_pos = agent_pos
		self.c_map = c_map
		self.agents = c_agent_list
		self.lIndex = listIndex
		
	def move(self, cur_pos):
		# Caller function for bfs
		return self.bfs(cur_pos, self.c_map, self.agents)
		
	def bfs(self, agent_pos, c_map, c_agent_list):
		visited = []
		queue = []
		path_map = {}
		current_pos = (agent_pos[0], agent_pos[1])
		path_map[(current_pos,0)] = 'END'
		for agent in self.agents: 
			pos_form = agent.getPos()
			if (pos_form[0] == current_pos[0]) and (pos_form[1] == current_pos[1]):
				current_agent = agent
		visited.append(current_pos)
		queue.append((current_pos, 0))
		while queue:
			current_pos = queue.pop(0)
			possible_moves = self.c_map.get_next(current_pos[0])
			for move, direction in possible_moves:
				if current_agent.isGoal(move):
					print('GOAL')
					path_map[(move, direction)] = (current_pos)
					com = path_map[current_pos]
					return_list = [(move, direction)]
					while com is not 'END':
						return_list.append(com)
						com = path_map[com]
					return_list.reverse()
					return return_list
				elif move not in visited:
					path_map[(move, direction)] = (current_pos)
					visited.append(move)
					queue.append((move, direction))

class Astar:
	def __init__(self):
		pass

class MinMax:
	def __init__(self, agent_pos, c_map, c_agent_list,listIndex):
		self.current_pos = agent_pos
		self.c_map = c_map
		self.agents = c_agent_list
		self.lIndex = listIndex
		self.depth = 2
		
	def move(self):
		self.minmax()
		
	def minmax(self):
		def get_min(agent_pos_list, cur_depth, cur_agent):
			max_successors = []
			
			actions = self.c_map.get_next(agent_pos_list[cur_agent])
			
			for action in actions:
				agent_pos_list[cur_agent] = action
				max_successors.append(mm_driver(agent_pos_list, current_depth, current_agent + 1))
			
		
		def get_max(agent_pos_list, cur_depth, cur_agent):
			min_successors = []
			
			actions = self.c_map.get_next(agent_pos_list[cur_agent])
			
			for action in actions:
				agent_pos_list[cur_agent] = action
				min_successors.append(mm_driver(agent_pos_list, current_depth, current_agent + 1))
				
			return max(min_successors)
			
		def mm_driver(agent_pos_list, cur_depth, cur_agent):
			
			if current_agent is len(c_agent_list):
				current_depth += 1
			
			if (current_depth >= self.depth):
				return "SCORE STATES" # Add state scoring
			
			if current_agent is calling agent:
				return get_max(agent_pos_list, current_depth, current_agent)
class ExpMax:
	def __init__(self):
		pass
