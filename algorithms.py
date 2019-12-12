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
import queue
from heapq import *

# TODO: Create manhattan distance algorithm that accounts for walls
class hunterEvalFunction:
	# agentPositions holds a list of coordinates for each agent on the map
	def __init__(self, listOfAgents, agentIndex):
		self.agentList = listOfAgents
		self.index = agentIndex
		self.agentType = listOfAgents[agentIndex].getType()
		self.agentPos = listOfAgents[agentIndex].getPos()
		self.listOfAgents = listOfAgents


	def evaluate(self, worldState):
		#self.agentPos = self.agentList[self.index].getPos()
		total = 0
		total = [agents.algorithm.BFSDist(self.agentPos, agents.getPos())
				for agents in self.listOfAgents if (agents.getType() is not self.agentType)]
		#print("Total list: ", total)
		total = min(total)
		#print("Hunter Total: ", total)
		return total
		#return random.randrange(0,255,1)

class runnerEvalFunction:
	# agentPositions holds a list of coordinates for each agent on the map
	def __init__(self, listOfAgents, agentIndex, total=0):
		self.agent = listOfAgents[agentIndex]
		self.agentType = self.agent.getType()
		self.agentPos = self.agent.getPos()
		self.listOfAgents = listOfAgents
		self.safeZones = self.agent.algorithm.c_map.get_safezone()
		self.total = total

	def evaluate(self, worldState):
		#print("1 = ", self.total)
		self.total = [agents.algorithm.BFSDist(self.agentPos, agents.getPos())
				for agents in self.listOfAgents if agents.getType() is not self.agentType]
		self.total = min(self.total) * -1.0

		totalSafeZone = [self.agent.algorithm.BFSDist(self.agentPos, coordinate) for coordinate in self.safeZones]
		self.total += (sum(totalSafeZone) * 0.5) - min(totalSafeZone)

		#self.total -= 15.0
		#print("2 = ", self.total)
		#print("Runner Total: ", self.total)
		return min(totalSafeZone)

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

	def hunterEval(self, cur_agent, listOfAgents):
		total = []
		agent = listOfAgents[cur_agent]
		for agents in range(len(listOfAgents)):
			if listOfAgents[agents].getType() is not 'hunter':
				total.append(agent.algorithm.manhattanDistance(self.curPos(cur_agent), self.curPos(agents)))
		print ("Total: ", min(total))
		return min(total) * -1

	def runnerEval(self, cur_agent, listOfAgents):
		agent = listOfAgents[cur_agent]
		safeZones = agent.algorithm.c_map.get_safezone()
		totalSafeZone = [agent.algorithm.manhattanDistance(self.curPos(cur_agent), coordinate) for coordinate in safeZones]
		hunter_pos_list = []
		#print("safzone: ", min(totalSafeZone))
		total = min(totalSafeZone) * -1
		if self.curPos(cur_agent) in list(agent.visited.keys()):
			print("Agent visit: ", agent.visited[self.curPos(cur_agent)])
			#total -= agent.visited[self.curPos(cur_agent)]

		for agents in range(len(listOfAgents)):
			if listOfAgents[agents].getType() is not 'runner':
				hunter_pos_list.append(agent.algorithm.manhattanDistance(self.curPos(cur_agent), self.curPos(agents)))

		print(min(hunter_pos_list))
		if min(hunter_pos_list) <= 1:
			total += -2
		print ("Total: ", total)
		#return total
		return 0


class baseAlgorithm:
	def __init__(self, agent_pos, c_map, c_agent_list = None, index = None,rand = 0):
		self.agent_pos = (agent_pos[0],agent_pos[1])
		self.c_map = c_map
		self.wallList = c_map.get_map_bounds() + c_map.get_walls()
		self.facing = 0
		self.agent_list = c_agent_list
		#self.agents = c_agent_list#
		self.index = index
		#self.lIndex = index#
		self.moveList = []
		self.rand = rand
		self.last = [None, None, self.agent_pos]
		self.imagePath = './images/b-arrow-small.png'
		self.agent = None

	def getImage(self):
		return self.imagePath

	def setImage(self,imagePath):
		self.imagePath = imagePath

	def isValidMove(self,plannedPosition):
		# takes a position, and returns if the move would collide with
		# a world object.  Needed for the algorithms
		self.agent = self.agent_list[self.index]
		if plannedPosition in self.wallList:
			#print("isValidMove wall collision")
			return False
		for a in self.agent_list:
			if (plannedPosition == a.getPos()) and (a.getType() == self.getType()):#"hunter"):
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

	def getType(self):
		return self.agent.getType()

	def genericMove(self,tempPos):
		savedPos = (self.agent_pos[0],self.agent_pos[1])
		self.agent_pos = (tempPos[0],tempPos[1])
		if (self.getType() == "DFS") or (self.getType() == "BFS"):
			#copy list and take position after target
			if tempPos not in self.moveList: # if not in list, just started
				temp = (self.moveList[0],0)
			else:
				tempI = self.moveList.index(tempPos)
				temp = (self.moveList[tempI+1],0)
		else:
			temp = self.move()
		self.agent_pos = (savedPos[0],savedPos[1])
		print("Self: ",self.agent_pos," Temp: ",temp[0])
		return temp[0]


	def BFSDist(self, pPos, pos2, last = None):
		# need to start a queue, and a Visited list
		if self.linDist(pPos,pos2)<15:
			#print("Foo")
			return 5*self.linDist(pPos,pos2)
		#print("No Foo")
		visited = []
		# find & return distance to target (depth
		distance = 0
		tempList = self.generateMoves(pPos) #generate first set of positions
		#print("TL: ",tempList)
		random.shuffle(tempList)
		#print("TL: ",tempList)
		#print(tempList)
		while not (pos2 in tempList) and (distance < 30) :#and not (len(tempList)==0):#not len([item for item in tempList if item==pos2])==0:
			#print("P2: ",pos2," TL: ",tempList)
			distance +=1
			#use current list to generate a new one
			#print("TL: ", tempList)
			oldList = tempList
			tempList = []
			for aPos in oldList:
				if aPos not in visited:
					#iterList = []
					tempList+=self.generateMoves(aPos)
					visited.append(aPos)
			if len(tempList)==0:
				#print("Empty List!")
				return distance#1000#if list is empty, exhausted possible moves without finding target

			#print("TL: ", tempList, " Dist ", distance)
		if distance >= 29:
			#print("Max Distance")
			return self.linDist(pPos,pos2)
		return distance

	def generateMovelist(self, pPos, defaultValue = 999999999, randomize = 0):
		#same method as Reflex
		pList = []
		#if self.isValidMove(((pPos[0]),(pPos[1]))): # don't move if current position is ideal
		if (self.agent is not None) and (self.agent.getType() == "runner"):
			pList.append((((pPos[0]),(pPos[1])),defaultValue-1,-1))
		if self.isValidMove(((pPos[0]),(pPos[1]-1))):
			pList.append((((pPos[0]),(pPos[1]-1)),defaultValue,1))
		if self.isValidMove(((pPos[0]),(pPos[1]+1))):
			pList.append((((pPos[0]),(pPos[1]+1)),defaultValue,3))
		if self.isValidMove(((pPos[0]-1),(pPos[1]))):
			pList.append((((pPos[0]-1),(pPos[1])),defaultValue,2))
		if self.isValidMove(((pPos[0]+1),(pPos[1]))):
			pList.append((((pPos[0]+1),(pPos[1])),defaultValue,0))
		if randomize:
			random.shuffle(pList)
		return pList

	def generateMoves(self, pPos): #mostly for BSFDepth
		pList = []
		if self.isValidMove(((pPos[0]),(pPos[1]))):
			pList.append(((pPos[0]),(pPos[1])))
		if self.isValidMove(((pPos[0]),(pPos[1]-1))):
			pList.append(((pPos[0]),(pPos[1]-1)))
		if self.isValidMove(((pPos[0]),(pPos[1]+1))):
			pList.append(((pPos[0]),(pPos[1]+1)))
		if self.isValidMove(((pPos[0]-1),(pPos[1]))):
			pList.append(((pPos[0]-1),(pPos[1])))
		if self.isValidMove(((pPos[0]+1),(pPos[1]))):
			pList.append(((pPos[0]+1),(pPos[1])))
		return pList

###############################


class genericAlgorithms(baseAlgorithm):
	# This generic algorithm is a basic structure to show how to
	# interface between the agent and algorithm in a way that the game
	# engine can use the data
	'''def __init__(self, agent_pos, c_map): # use base init
		# Create Algorithm
		self.agent_pos = (agent_pos[0],agent_pos[1])
		self.c_map = c_map
		self.wallList = c_map.get_map_bounds() + c_map.get_walls()
		#self.wallList.expand(c_map.get_walls())
		self.facing = 0'''

	def getType(self):
		return "generic"

	def move(self,unusedPos = None):
		d = (random.randrange(0,3,1))
		# Increase the max to decrease odds of turning(baseAlgorithm)
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

class testAlgorithm(baseAlgorithm): # should remain unused.  For basic interface demonstration
	def __init__(self, agent_pos, c_map, c_agent_list,listIndex):
		self.agent_pos = (agent_pos[0],agent_pos[1])
		self.c_map = c_map
		self.wallList = c_map.get_map_bounds() + c_map.get_walls()
		self.facing = 0
		self.agent_list = c_agent_list
		#print("Ag: ",self.agent_list)

	def getAlgType(self):
		return "test"

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
		#if self.isValidMove(((pPos[0]),(pPos[1]))): # don't move if current position is ideal
		#	pList.append((((pPos[0]),(pPos[1])),999999999))
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
		#using default init

	def getAlgType(self):
		return "Reflex"

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
		pList = self.generateMovelist(pPos, 999999999,1)

		if len(pList) == 0: # if no valid moves currently, don't bother checking
			return (pPos[0]),(pPos[1])
		# all valid positions now in a list
		# pList is [((x,y),manhattanDist),...]
		# manhattanDist val is init as a very large value, vastly larger
		# than expected max paths
		if (self.rand >= (random.randrange(0,100,1))):
			# random move with self.rand as the threshold
			ranDir = random.randrange(0,len(pList),1)
			self.facing = pList[ranDir][2]
			return pList[ranDir][0]

		# get nearest opposing agent:
		nearest = 9999999
		for agent in self.agent_list:
			# find closest agent's distance
			agentVal = self.linDist(self.agent_pos, agent.getPos())
			if (agentVal < nearest) and not(agent.getType() == self.agent.getType()):
				nearest = agentVal
				nearestAgent = agent

		# if hunter: move toward nearest runner, found above
		# if runner, move toward exit unless hunter is too close
		if self.getType() == "runner":
			agentDist = 0
			moveIndex = 0
			#if (nearest < 5): # if enemy too close plan to run
			for i in range(0,len(pList)):
				tempDist = self.linDist(pList[i][0], nearestAgent.getPos())
				pList[i] = ((pList[i][0]), tempDist,pList[i][2])
				if tempDist > agentDist:
					agentDist = tempDist
					moveIndex = i
			#print("Running", pList)
			self.facing = pList[moveIndex][2]
			#return pList[moveIndex][0] # return the move most opposite of the hunter

			#else: # head toward exit
			currentBest = 999999999
			currentIndex =  None
			#print(pList)
			for i in range(0,len(pList)):
				# for each square, go through list of agents, finding
				# the closest step to the closest exit
				bestVal = 99999999
				for safe in self.c_map.get_safezone():
					tempVal = self.linDist(pList[i][0],safe) #change for BFSDist here
					#print("safe: ",safe," temp ",tempVal)
					if  tempVal < bestVal:
						bestVal = tempVal
				if bestVal < currentBest:
					currentBest = bestVal
					currentIndex = i
				pList[i] = ((pList[i][0]),bestVal,pList[i][2])
			self.facing = pList[currentIndex][2]
			#return pList[currentIndex][0]
			if (nearest < 7) and (currentBest > 5):# if nearest is too close and not close enough to exit
				self.facing = pList[moveIndex][2]
				return pList[moveIndex][0] # return the move most opposite of the hunter
			else:
				return pList[currentIndex][0]


		# else keep going
		for i in range(0,len(pList)):
			# for each square, go through list of agents, finding the closest
			bestVal = 99999999
			for agent in self.agent_list:
				# find closest agent's distance
				if not (agent.getType() == self.agent.getType()):
					agentVal = self.linDist(pList[i][0], agent.getPos()) #and BFSDist here as well

				if (agentVal < bestVal):
					bestVal = agentVal
			pList[i] = ((pList[i][0]),bestVal,pList[i][2])
			# the above loop should find the closest opposing agent to that
			# position, and sets the value for the position being checked
			# to that value
		bestIndex = None
		bestVal = 999999999
		for i in range(0,len(pList)):
			if ((pList[i][1]) < bestVal):
				bestVal = pList[i][1]
				bestIndex = i
		self.facing = pList[bestIndex][2]
		return pList[bestIndex][0]


class DFS(baseAlgorithm):
	# NOTE: DFS may not work well in this setup- need a map with paths
	# to be able to limit depth paths (and avoid looping)
	# UPDATE:  Works on all maps, visually clear it is a nonideal choice

	def getAlgType(self):
		return "DFS"

	def move(self, cur_pos):
		# Caller function for dfs
		return self.dfs(cur_pos, self.c_map, self.agent_list)

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
		for agent in self.agent_list:
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
					self.moveList = path
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
	# using default init from baseAlgorithm

	def getAlgType(self):
		return "BFS"

	def move(self, cur_pos):
		#self.last.append(cur_pos)
		# Caller function for bfs
		if self.agent_list[self.index].getType() == "hunter":
			result = self.hunterbfs(cur_pos)

			# This finds value based on a BFS search between two squares
			# doing this iteratively is SLOW
		else:
			result = self.runnerbfs(cur_pos, self.c_map, self.agent_list)
		self.last[0] = self.last[1]
		self.last[1] = self.last[2]
		self.last[2] = cur_pos

		return result

	def hunterbfs(self, pPos):
		override = 0
		pList = []
		bestPos = 0
		bestVal = 999999999
		# up: 0 -1
		# dn: 0 +1
		# lf: -1 0
		# rt: +1 0
		pList = self.generateMovelist(pPos, 999999999,1)

		if len(pList) == 0: # if no valid moves currently, don't bother checking
			return (pPos[0]),(pPos[1])
		# all valid positions now in a list
		# pList is [((x,y),manhattanDist),...]
		# manhattanDist val is init as a very large value, vastly larger
		# than expected max paths
		if (self.rand >= (random.randrange(0,100,1))):
			# random move with self.rand as the threshold
			#print("Random Move")
			ranDir = random.randrange(0,len(pList),1)
			self.facing = pList[ranDir][2]
			return pList[ranDir][0]

		# get nearest opposing agent:
		nearest = 9999999
		for agent in self.agent_list:
			# find closest agent's distance

			agentVal = self.linDist(self.agent_pos, agent.getPos())
			if (agentVal < nearest) and not(agent.getType() == self.agent.getType()):
				nearest = agentVal

		# else keep going
		# remove last square from possible valid moves
		if (self.last[0] is not "foo"):
			#print(pList[1][0]," ",self.last[0])
			for x in pList:
				if (x[0] == self.last[0]) and (len(pList)>1):# and (pList[x][0][1] == self.last[0][1]) :
					#print("Remove Last")
					pList.remove(x)
					override = 1

		for i in range(0,len(pList)):
			# for each square, go through list of agents, finding the closest
			bestVal = 99999999
			for agent in self.agent_list:
				# find closest agent's distance
				if not (agent.getType() == self.agent.getType()):
					if override:
						agentVal = self.linDist(pList[i][0], agent.getPos())
					else:
						agentVal = self.BFSDist(pList[i][0], agent.getPos())

				if (agentVal < bestVal):
					bestVal = agentVal
			pList[i] = ((pList[i][0]),bestVal,pList[i][2]) # update the value for agent list
			# the above loop should find the closest opposing agent to that
			# position, and sets the value for the position being checked
			# to that value

		bestIndex = None
		bestVal = 999999999
		for i in range(0,len(pList)):
			if ((pList[i][1]) < bestVal):
				bestVal = pList[i][1]
				bestIndex = i
		#if (pList is not None) and (pList[bestIndex] is not None) and (pList[bestIndex][2] is not None):
		self.facing = pList[bestIndex][2]
		return pList[bestIndex][0]


########################################
	def runnerbfs(self, agent_pos, c_map, c_agent_list):
		# Keep track of each coordinate the agent looks at
		visited = []

		# Keep track of the order we see coordinates so we can iterate through them
		queue = []
		path_map = {}

		# Go through the list of agents and find where this agent is located on the map
		current_pos = (agent_pos[0], agent_pos[1])

		for agent in self.agent_list:
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
					#print('GOAL')
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

class Astar(baseAlgorithm):

	# Use baseAlgorithm init function
	def move(self, cur_pos):
		self.agent = self.agent_list[self.index]
		return self.Astar(cur_pos, self.c_map, self.agent_list)

	def heuristic(self, pos1, pos2):
		# Change later to create a more sophisticated heuristic
		return self.manhattanDistance(pos1, pos2)

	def Astar(self, agent_pos, c_map, c_agent_list):

		h = []

		# Priority Queue that pops the smallest priority first
		#a = queue.PriorityQueue()

		# Keep track of the cost for each state
		cost_history = {}
		explored = []

		# Set starting state to zero
		cost_history[str(agent_pos)] = 0

		# ((Agent Position, Actions to State, Cost of State), Total Cost up to State)
		empty_list = []
		#a.put((agent_pos, empty_list, 0, 0))

		heappush(h, (0, (agent_pos, 0)))
		i = 0
		while True:
			print("Explored = ", explored)
			print("i = ", i)
			i += 1

			if i == 100:
				exit()

			#if a.empty():
			#	print("Error: Priority Queue is Empty!")
			#	exit()

			# Get state information from lowest priority state
			# NEED TO CHECK
			#position, action_list, cost, total_cost = a.get()
			currentState = heappop(h)
			print("Current State = ", currentState)
			total_cost = currentState[0]
			position = currentState[1][0]
			cost = currentState[1][1]

			print("Total Cost = ", total_cost)
			print("Position = ", position)
			print("Cost = ", cost)


			#if action_list is None:
			#	action_list = []
			#	print("creating empty list")

			#print("action_list = ", action_list)
			#print("cost = ", cost)
			#print("position = ", position)

			if self.agent.isGoal((position[0], position[1])):
				print("Found goal!")
				return position

			# Add coordinate to set of explored states
			if position not in explored:
				explored.append(position)

				# Returns a ((x,y), direction) tuple
				actions = self.c_map.get_next(position)

				for action in actions:
					cost_history[str(action[0])] = total_cost + self.heuristic(position, action[0])

					#a.put((action[0], action_list.append(action[0]), self.heuristic(position, action[0]), cost_history[str(action[0])]))
					heappush(h, (cost_history[str(action[0])], (position, self.heuristic(position, action[0]))))

	def getAlgType(self):
		return "Astar"

class MinMax(baseAlgorithm):
	# TODO: Ensure that game engine moves agents in the same way as minmax.
	def __init__(self, agent_pos, c_map, c_agent_list, listIndex):
		self.current_pos = agent_pos
		self.c_map = c_map
		self.agents = c_agent_list
		# For BFSDist algorithm
		self.agent_list = c_agent_list
		self.index = listIndex
		self.wallList = c_map.get_map_bounds() + c_map.get_walls()

		self.lIndex = listIndex
		self.depth = 2
		#self.runner_list = [agent for agent in self.c_agentList if agent.getType() is 'runner']
		#self.hunter_list = [agent for agent in self.c_agentList if agent.getType() is 'hunter']

	def getAlgType(self):
		return "MinMax"

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
			#print("Action List: ",actions)

			for action in actions:
				#print("action[0] = ", action[0])
				successor = worldState.nextState(action[0], current_agent)
				#print("successor =", successor)
				max_successors.append((helper(successor, current_depth, current_agent + 1), action))
				#max_successors.append(helper(successor, current_depth, current_agent + 1))


			# Might need to add code for when no actions are available
			#print("Max Successors: ", max_successors)
			#exit()
			if max_successors:
				return min(max_successors)
			else:
				return (0,((-1,-1),0))

		def get_max(worldState, current_depth, current_agent):
			min_successors = []

			#print("Current agent: ", current_agent)
			actions = self.c_map.get_next(worldState.curPos(current_agent))

			for action in actions:
				#print("action[0] = ", action[0])
				successor = worldState.nextState(action[0], current_agent)
				min_successors.append((helper(successor, current_depth, current_agent + 1), action))

			# Might need to add code for when no actions are available
			#print("Min Successors ", min_successors)
			if min_successors:
				return max(min_successors)
			else:
				return (0,((-1,-1),0))

		def helper(worldState, current_depth, current_agent):
			if current_agent is len(self.new_list):
				current_depth += 1
				current_agent = 0

			if (current_depth is self.depth):
				# TODO: Add state scoring
				if self.new_list[0].getType() is "runner":
					#self.new_list[current_agent].totalEvalScore = runnerEvalFunction(self.new_list, current_agent, self.new_list[current_agent].totalEvalScore).evaluate()
					#return self.new_list[current_agent].totalEvalScore
					#print("runner eval = ", runnerEvalFunction(self.new_list, current_agent).evaluate())
					#return runnerEvalFunction(self.new_list, current_agent).evaluate(worldState)
					return worldState.runnerEval(current_agent, self.new_list)
				else:
					#print("hunter eval = ", hunterEvalFunction(self.new_list, current_agent).evaluate())
					#return hunterEvalFunction(self.new_list, current_agent).evaluate(worldState)
					return worldState.hunterEval(current_agent, self.new_list)

			if self.new_list[current_agent].getType() is self.indexAgentType:
				return get_max(worldState, current_depth, current_agent)
			else:
				return get_min(worldState, current_depth, current_agent)

		# Beginning of MinMax
		best_score = helper(worldState, 0, 0)

		#print("---------------------")
		#print(self.agents[self.lIndex].role ," best score = ", best_score)
		#print("best score = ", best_score[1])
		print ("Visited: ", self.agent_list[0].visited)
		if best_score[1][0] not in list(self.agent_list[0].visited.keys()):
			self.new_list[0].visited[best_score[1][0]] = 1
		else:
			self.new_list[0].visited[best_score[1][0]] += 1

		return best_score[1]

class ExpMax(baseAlgorithm):
	# TODO: Ensure that game engine moves agents in the same way as minmax.
	def __init__(self, agent_pos, c_map, c_agent_list, listIndex):
		baseAlgorithm.__init__(self, agent_pos, c_map)
		self.current_pos = agent_pos
		self.c_map = c_map
		self.agents = c_agent_list
		# For BFSDist algorithm
		self.agent_list = c_agent_list
		self.index = listIndex
		self.wallList = c_map.get_map_bounds() + c_map.get_walls()

		self.lIndex = listIndex
		self.depth = 2
		#self.runner_list = [agent for agent in self.c_agentList if agent.getType() is 'runner']
		#self.hunter_list = [agent for agent in self.c_agentList if agent.getType() is 'hunter']

	def getAlgType(self):
		return "MinMax"

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
			#print("Action List: ",actions)

			for action in actions:
				#print("action[0] = ", action[0])
				successor = worldState.nextState(action[0], current_agent)
				#print("successor =", successor)
				max_successors.append((helper(successor, current_depth, current_agent + 1), action))

			total = 0.0
			for value, state in max_successors:
				if type(value) is tuple:
					#print("value = ", value)
					#exit()
					total += value[0]
				else:
					total += value

			return total * (1.0/float(len(max_successors)))

			# Might need to add code for when no actions are available
			#print("Max Successors: ", max_successors)
			#print("Length of Max Successors: ", len(max_successors))
			#exit()
			#return min(max_successors)


		def get_max(worldState, current_depth, current_agent):
			min_successors = []

			#print("Current agent: ", current_agent)
			actions = self.c_map.get_next(worldState.curPos(current_agent))

			for action in actions:
				successor = worldState.nextState(action[0], current_agent)
				min_successors.append((helper(successor, current_depth, current_agent + 1), action))

			# Might need to add code for when no actions are available
			#print("Min Successors ", min_successors)
			return max(min_successors)

		def helper(worldState, current_depth, current_agent):
			if current_agent is len(self.new_list):
				current_depth += 1
				current_agent = 0

			if (current_depth >= self.depth):

				# TODO: Add state scoring
				if self.new_list[current_agent].getType() is "runner":
					#self.new_list[current_agent].totalEvalScore = runnerEvalFunction(self.new_list, current_agent, self.new_list[current_agent].totalEvalScore).evaluate()
					#return self.new_list[current_agent].totalEvalScore
					#print("runner eval = ", runnerEvalFunction(self.new_list, current_agent).evaluate())
					return runnerEvalFunction(self.new_list, current_agent).evaluate()
				else:
					#print("hunter eval = ", hunterEvalFunction(self.new_list, current_agent).evaluate())
					return hunterEvalFunction(self.new_list, current_agent).evaluate()

			if self.new_list[current_agent].getType() is self.indexAgentType:
				return get_max(worldState, current_depth, current_agent)
			else:
				return get_min(worldState, current_depth, current_agent)

		best_move = helper(worldState, 0, 0)

		#print("---------------------")
		#print(self.agents[self.lIndex].role ," best move = ", best_move)
		#print("best move = ", best_move[1][0])
		return best_move[1][0]
