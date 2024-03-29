###########################################################################
###########################################################################
# Authors: Adrien Forkum, Nick Quinn, Karl Horlitz
# Date: 10/26/19
#
# Description: This file contains the structure and implementation of each
#              agent, such as each runner or hunter.
#
###########################################################################
###########################################################################
import random
import pygame
from datetime import datetime, timedelta
from algorithms import *

class agent(pygame.sprite.Sprite):
	def __init__(self, c_map, c_agent_list=None, c_alg=None, _role=None,
				_current_pos=None, _image=None, _image2=None, _algorithm=None, _rand = 0, _index = None):

		# Create Sprite Object for Agent
		pygame.sprite.Sprite.__init__(self)

		# Create Object Variables
		self.agent_pos = _current_pos
		self.role = _role
		self.lIndex = _index
		#print("lInd- ",_index)

		# Game environement variables
		self.c_map = c_map
		self.c_agent_list = c_agent_list
		self.c_alg = c_alg
		_algorithm = c_alg
		self.algorithmName = "Not Initialized"

		# Game engine variables
		self.image = _image
		self.image2 = _image2
		self.sScale = .5
		self.spriteR = 20 * self.sScale
		self.facing = 0
		self.rand = _rand
		self.die = 0
		self.teamChanged = 0

		# Algorithm variables
		self.com_mag = None
		self.visited = {}

		# Scoring variables
		self.agentsKilled = 0
		self.timeAlive = None
		self.endState = 0	# End state is how agent was ended the game (0 = alive at end, 1 = killed by hunter, 2 = safe zone exit, 3 = converted)
		self.totalEvalScore = 0.0


		if self.agent_pos == None:
			if self.role == "runner":
				#self.agent_pos = [1,1]#[random.randrange(5,gameWindow[0]-5,1),random.randrange(5,gameWindow[1]-5,1)]
				posSpawn = c_map.get_rspawn()
			else:
				#self.agent_pos = [10,10]
				posSpawn = c_map.get_hspawn()
			self.agent_pos = posSpawn[random.randrange(0,len(posSpawn),1)]

		# Create sprite image based on location and dimensions
		self.rect = pygame.Rect(self.agent_pos[0],self.agent_pos[1], self.spriteR, self.spriteR)

		# Assign Agent Algorithm
		self.setAlg(_algorithm)

		# Assign Image
		#print("Role: ", self.role)
		'''if self.role == "hunter":
			self.image = pygame.image.load('./images/r-arrow-small.png')
		elif self.role == "runner":
			self.image = pygame.image.load('./images/b-arrow-small.png')
		else:
			print("ERROR: AGENTS.PY - COULD NOT FIND IMAGE.")
			self.image = pygame.image.load('./images/waldo-small.png')'''

		# Resize image for gameWindow
		self.image = pygame.transform.scale(self.image, (int(self.spriteR * 2), int(self.spriteR * 2)))


	def setAlg(self,alg):
		if alg.lower() == "dfs":
			self.algorithm = DFS(self.agent_pos, self.c_map, self.c_agent_list, self.lIndex)
			self.algorithm.setImage('./images/b4-arrow-small.png')
			self.algorithmName = "DFS"
		elif alg.lower() == "bfs":
			self.algorithm = BFS(self.agent_pos, self.c_map, self.c_agent_list, self.lIndex)
			self.algorithmName = "BFS"
			if self.role == "hunter":
				self.algorithm.setImage('./images/r1-arrow-small.png')
			else:
				self.algorithm.setImage('./images/b1-arrow-small.png')
		elif alg.lower() == "astar" or alg.lower() == "A*":
			self.algorithm = Astar(self.agent_pos, self.c_map, self.c_agent_list, self.lIndex)
			self.algorithmName = "A*"
		elif alg.lower() == "minmax":
			self.algorithm = MinMax(self.agent_pos, self.c_map, self.c_agent_list, self.lIndex)
			self.algorithmName = "MinMax"
			if self.role == "hunter":
				self.algorithm.setImage('./images/r2-arrow-small.png')
			else:
				self.algorithm.setImage('./images/b2-arrow-small.png')
		elif alg.lower() == "expmax" or alg.lower() == "expectimax":
			self.algorithm = ExpMax(self.agent_pos, self.c_map, self.c_agent_list, self.lIndex)
			self.algorithmName = "ExpectiMax"
		elif alg.lower() == "reflex":
			self.algorithm = Reflex(self.agent_pos, self.c_map,self.c_agent_list, self.lIndex, self.rand)
			self.algorithmName = "Reflex"
			if self.role == "hunter":
				self.algorithm.setImage('./images/r3-arrow-small.png')
			else:
				self.algorithm.setImage('./images/b3-arrow-small.png')
		elif alg.lower() == "test":
			self.algorithm = testAlgorithm(self.agent_pos, self.c_map,self.c_agent_list, self.lIndex)
			self.algorithmName = "Test"
		elif alg.lower() == "testmm":
			self.algorithm = testMM(self.agent_pos, self.c_map,self.c_agent_list, self.lIndex)
			self.algorithmName = "TestMM"
		else:
			print("Using generic algorithms.")
			self.algorithm = genericAlgorithms(self.agent_pos, self.c_map, self.c_agent_list, self.lIndex)
			self.algorithmName = "GA"

		# Assign Image
		print("Role: ", self.role)
		#print(self.algorithm.getImage())

		self.image = pygame.image.load(self.algorithm.getImage())
		self.sScale = .5
		self.spriteR = 20 * self.sScale
		self.image = pygame.transform.scale(self.image, (int(self.spriteR * 2), int(self.spriteR * 2)))



	def update(self, screen):
		'''
		This ultimately calls the search algorithm, chooses the next step, and takes it
		will also need to check for, f.ex tag or escape states, either here or when update
		is called: could create list of Hunter positions, Runner positions, and check overlaps
		'''
		#self.agent_pos = self.algorithm.move()
		# Possible way of doing persistant commands by checking for existing commands in the object.
		if self.teamChanged:
			# if team has changed (runner converted to hunter) clear
			# the move list and reset teamChanged in case it changes back
			self.com_mag = None
			self.teamChanged = 0

		if not self.com_mag:
			#print("self.agentpos",self.agent_pos)
			# Algorithm time tracker
			alg_start_time = datetime.now()

			move_result = self.algorithm.move(self.agent_pos)

			alg_end_time = datetime.now() - alg_start_time

			#print("Move result: ", move_result)

			# kill or convert.  for now, kills on hunter tagging a runner
			if self.getType() == "hunter":
				for a in self.c_agent_list:
					if (a.getType() is not "hunter") and (1.5 >= self.algorithm.linDist(self.getPos(),a.getPos())):
						# a.markForDeath, a.kill() used to kill runners
						if self.c_map.getGameType() == 0: # kill runners, default
							self.agentsKilled += 1
							a.markForDeath()
							a.kill()
							a.endState = 1
							a.timeAlive = datetime.now() - a.timeAlive
						# a.changeTeam() converts them into Reflex hunters
						elif self.c_map.getGameType() == 1: # convert runners
							a.changeTeam(self.c_alg)
							self.agentsKilled += 1
							a.endState = 3
							a.timeAlive = datetime.now() - a.timeAlive
						else:
							print("no gameType ",self.c_map.getGameType(),"! ")

			# MinMax currently does not have a facing parameter
			if type(self.algorithm) is not MinMax:
				#print("Foo")
				self.facing = self.algorithm.facing

			# If move_result is a list of tupples set self.com_mag
			if isinstance(move_result, list):
				first_result = move_result[0]
				self.agent_pos = first_result[0]
				self.facing = first_result[1]
				move_result.pop(0)
				self.com_mag = move_result
			elif move_result == None:
				#no moves, do nothing
				None

			elif not isinstance(move_result[0],int):
				#None
				#print("MR: ",move_result)
				self.agent_pos = move_result[0]
				self.facing = move_result[1]
			else:# MR is a tuple
				self.agent_pos = move_result

		else:
			first_result = self.com_mag[0]
			self.agent_pos = first_result[0]
			self.facing = first_result[1]
			self.com_mag.pop(0)
		#self.facing = self.algorithm.facing
		rotated_image = pygame.transform.rotate(self.image, 90*(self.facing))
		#self.image = rotated_image
		#print(self.algorithm.getImage())
		self.rect = pygame.Rect(self.agent_pos[0] * 2 * self.spriteR,
								self.agent_pos[1] * 2 * self.spriteR,
								self.spriteR,
								self.spriteR)

		# Draw screen to image
		screen.blit(rotated_image, self.rect)

	def getPos(self):
		return (self.agent_pos[0],self.agent_pos[1])

	def getType(self):
		return self.role

	def isGoal(self, position, hunter_flag=False):
		# Added this code just to satisfy minmax dependency since DFS and BFS do not work with
		# hunters enabled at this time
		if hunter_flag:
			hunters = [agent for agent in self.agents if agent.role is 'hunter']

		runners = [agent for agent in self.c_agent_list if agent.role is 'runner']

		# Check for role of agent then return true based on criteria
		if self.role is 'hunter':
			# Hunter criteria
			for runner in runners:
				#print("p: ",position," GP: ", runner.getPos())
				#print("p type = ", type(position[1]), "gp type = ", type(runner.getPos()))

				if position is runner.getPos():
					return True

				# Not sure why, but AStar Algorithm doesn't work without this conditional
				temp = runner.getPos()
				if position[0] == temp[0] and position[1] == temp[1]:
					return True

		elif self.role is 'runner':
			# Runner criteria
			if position in self.c_map.get_safezone():
				return True

		# Return False fallthrough
		return False

	def getGoalCoord(self):

		if self.role is "runner":
			return self.c_map.get_safezone()
		else:
			runnerCoord = []

			for agents in range(len(self.c_agent_list)):
				if self.c_agent_list[agents].getType() is not 'hunter':
					runnerCoord.append(self.c_agent_list[agents].getPos())

			return runnerCoord

	def markForDeath(self):
		self.die = 1
		self.agent_pos = (-999999999,-999999999)

	def shouldDie(self):
		return self.die

	def changeTeam(self,alg):
		self.teamChanged = 1
		print("Alg: ",alg)
		if self.role == "runner":
			self.role = "hunter"
			self.image = pygame.image.load('./images/r-arrow-small.png')
			self.sScale = .5
			self.spriteR = 20 * self.sScale
			self.image = pygame.transform.scale(self.image, (int(self.spriteR * 2), int(self.spriteR * 2)))
			#self.algorithm = Reflex(self.agent_pos, self.c_map,self.c_agent_list, self.rand, self.lIndex)
			self.c_alg = alg
			self.setAlg(alg)

		else:
			self.role = "runner"
			self.image = pygame.image.load('./images/b-arrow-small.png')

	def getAlg(self):
		return self.algorithm

	def getAlgName(self):
		return self.algorithmName
