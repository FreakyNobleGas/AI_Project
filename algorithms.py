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
import math

# TODO: Create manhattan distance algorithm that accounts for walls
class hunterEvalFunction:
	# agentPositions holds a list of coordinates for each agent on the map
	def __init__(self, listOfAgents, agentIndex):
		self.agentList = listOfAgents
		self.index = agentIndex
		self.agentType = listOfAgents[agentIndex].getType()
		self.agentPos = listOfAgents[agentIndex].getPos()
		self.listOfAgents = listOfAgents
		

	def evaluate(self):
		#self.agentPos = self.agentList[self.index].getPos()
		total = 0
		total = [agents.algorithm.manhattanDistance(self.agentPos, agents.getPos())
				for agents in self.listOfAgents if (agents.getType() is not self.agentType)]
		print("Total list: ", total)		
		total = min(total)
		print("hunter Total: ", total)
		return total

class runnerEvalFunction:
	# agentPositions holds a list of coordinates for each agent on the map
	def __init__(self, listOfAgents, agentIndex, total=0):
		self.agent = listOfAgents[agentIndex]
		self.agentType = self.agent.getType()
		self.agentPos = self.agent.getPos()
		self.listOfAgents = listOfAgents
		self.safeZones = self.agent.algorithm.c_map.get_safezone()
		self.total = total

	def evaluate(self):
		#print("1 = ", self.total)
		self.total = [agents.algorithm.manhattanDistance(self.agentPos, agents.getPos())
				for agents in self.listOfAgents if agents.getType() is not self.agentType]
		self.total = min(self.total) * -1.0

		totalSafeZone = [self.agent.algorithm.manhattanDistance(self.agentPos, coordinate) for coordinate in self.safeZones]
		self.total += (sum(totalSafeZone) * 0.5)

		self.total -= 15.0
		#print("2 = ", self.total)
		print("runner Toal: ", self.total)
		return self.total

class worldState:
	def __init__(self, agentPositions):
		self.agentPositions = agentPositions

	def nextState(self, action, agent):
		#print("Action: ", action)
		self.agentPositions[agent] = action
		return worldState(self.agentPositions)

	def curPos(self, agent):
		#print("Current pos for agent: ", self.agentPositions[agent])
		return self.agentPositions[agent]

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

	def linDist(self,pos1,pos2):
		return (math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2))

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
		#print("PL ", pLis7t, " BI ", pList[bestIndex])
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
				agentVal = self.linDist(pList[i][0], agent.getPos())

				''' old code, moved to agent.update() to make it universal
				if (agentVal <=1)and not(agent.getType() == self.agent_list[self.lIndex].getType()):
					agent.kill()
					# this kills off a tagged runner
					# can also add a gameType conditional, to change them to hunters
				'''
				if (agentVal < bestVal) and not(agent.getType() == "hunter"):#self.agent_list[self.lIndex].getType()):
					# NOTE: this is currently set as a dedicated hunter-only
					# algorithm.  only works for hunters chasing runners
					# (to avoid chasing itself and not moving)
					#
					# SECONDARY: self.agent_list[self.lIndex].getType() 
					# isn't working properly with two hunters.
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


class DFS(baseAlgorithm):
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

	def dfs(self, agent_pos, c_map, c_agent_list):
		"""
		Depth First Search algorithm.

		:agent_pos: Current agent position, (x, y) tuple.

		:c_map: Map object for obtaining walls, boundries, and safe zones.

		:c_agent_list: List of agent objects for iterating through and finding next moves of each agent.
		"""
		# Keep track of each coordinate the agent looks at
		visited = []

		# List of directions returned for the agent
		path = []

		# Go through the list of agents and find where this agent is located on the map
		current_pos = (agent_pos[0], agent_pos[1])
		for agent in self.agents:
			pos_form = agent.getPos()
			if (pos_form[0] == current_pos[0]) and (pos_form[1] == current_pos[1]):
				current_agent = agent

		# Add the agents current position to the list of visited and directions
		visited.append(current_pos)
		path.append((current_pos, 0))

		while path:
			# Flag for checking if a coordinate has been visited by the agent
			flag = True

			# Returns all moves that are immediately possible for the current position
			possible_moves = self.c_map.get_next(current_pos)

			# Iterate through each move possible
			for move, direction in possible_moves:
				# Check if move is a goal state and if it is, then return list of
				# instructions
				if current_agent.isGoal(move):
					path.append((move, direction))
					return path

				# If not goal state, then add to list of visited states, and continue looking
				elif move not in visited:
					flag = False
					visited.append(move)
					path.append((move, direction))
					current_pos = move
					break

			# If the state has been visited then there is no need to continue looking
			# past this specific coordinate
			if flag:
				path.pop(-1)
				# Set current position to the last coordinate in the path
				if path:
					current_pos = path[-1][0]


class BFS(baseAlgorithm):
	def __init__(self, agent_pos, c_map, c_agent_list,listIndex):
		self.current_pos = agent_pos
		self.c_map = c_map
		self.agents = c_agent_list
		self.lIndex = listIndex

	def move(self, cur_pos):
		# Caller function for bfs
		return self.bfs(cur_pos, self.c_map, self.agents)

	def bfs(self, agent_pos, c_map, c_agent_list):
		# Keep track of each coordinate the agent looks at
		visited = []

		# Keep track of the order we see coordinates so we can iterate through them
		queue = []
		path_map = {}

		# Go through the list of agents and find where this agent is located on the map
		current_pos = (agent_pos[0], agent_pos[1])
		for agent in self.agents:
			pos_form = agent.getPos()
			if (pos_form[0] == current_pos[0]) and (pos_form[1] == current_pos[1]):
				current_agent = agent

		path_map[(current_pos,0)] = 'END'

		# Add the agents current position to the list of visited and directions
		visited.append(current_pos)
		queue.append((current_pos, 0))

		while queue:
			# Grab the next coordinate in the queue
			current_pos = queue.pop(0)

			# Returns all moves that are immediately possible for the current position
			possible_moves = self.c_map.get_next(current_pos[0])

			# Iterate through each move possible
			for move, direction in possible_moves:
				# Check if move is a goal state and if it is, then return list of
				# instructions
				if current_agent.isGoal(move):
					print('GOAL')
					# Go through path map and create a list of instructions
					path_map[(move, direction)] = (current_pos)
					com = path_map[current_pos]
					return_list = [(move, direction)]
					while com is not 'END':
						return_list.append(com)
						com = path_map[com]
					return_list.reverse()
					return return_list

				# If not goal state, then add to list of visited states, and continue looking
				elif move not in visited:
					path_map[(move, direction)] = (current_pos)
					visited.append(move)
					queue.append((move, direction))

class Astar:
	def __init__(self):
		pass

class MinMax(baseAlgorithm):
	# TODO: Ensure that game engine moves agents in the same way as minmax.
	def __init__(self, agent_pos, c_map, c_agent_list, listIndex):
		self.current_pos = agent_pos
		self.c_map = c_map
		self.agents = c_agent_list
		self.lIndex = listIndex
		self.depth = 3
		#self.runner_list = [agent for agent in self.c_agentList if agent.getType() is 'runner']
		#self.hunter_list = [agent for agent in self.c_agentList if agent.getType() is 'hunter']

	def setup(self):
		self.new_list = [self.agents[self.lIndex]]
		self.indexAgentType = self.new_list[0].getType()
		self.new_list.extend([agent for agent in self.agents if agent.getType() is self.indexAgentType and agent is not self.agents[self.lIndex]])
		self.new_list.extend([agent for agent in self.agents if agent.getType() is not self.indexAgentType])

	def move(self, agent_pos):
		# Creates list of all agent positions for worldState
		self.setup()
		agent_pos_list = [agent.getPos() for agent in self.new_list]
		#print("Agent list: ", agent_pos_list)
		return self.minmax(worldState(agent_pos_list))

	def minmax(self, worldState):
		def get_min(worldState, current_depth, current_agent):
			max_successors = []

			#print("Current agent: ", current_agent)
			actions = self.c_map.get_next(worldState.curPos(current_agent))

			for action in actions:
				successor = worldState.nextState(action[0], current_agent)
				max_successors.append(helper(successor, current_depth, current_agent + 1))

			# Might need to add code for when no actions are available

			return min(max_successors)


		def get_max(worldState, current_depth, current_agent):
			min_successors = []

			#print("Current agent: ", current_agent)
			actions = self.c_map.get_next(worldState.curPos(current_agent))

			for action in actions:
				successor = worldState.nextState(action[0], current_agent)
				min_successors.append((helper(successor, current_depth, current_agent + 1), action))

			# Might need to add code for when no actions are available

			return max(min_successors)

		def helper(worldState, current_depth, current_agent):
			if current_agent is len(self.new_list):
				current_depth += 1
				current_agent = 0

			if (current_depth >= self.depth):
				# TODO: Add state scoring
				if self.new_list[current_agent].getType() is "runner":
					self.new_list[current_agent].totalEvalScore = runnerEvalFunction(self.new_list, current_agent, self.new_list[current_agent].totalEvalScore).evaluate()
					return self.new_list[current_agent].totalEvalScore
				else:
					return hunterEvalFunction(self.new_list, current_agent).evaluate()

			if self.new_list[current_agent].getType() is self.indexAgentType:
				return get_max(worldState, current_depth, current_agent)
			else:
				return get_min(worldState, current_depth, current_agent)

		best_score = helper(worldState, 0, 0)
		print(best_score)
		return best_score[1]

class ExpMax:
	def __init__(self):
		pass
