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
from algorithms import *

class agent(pygame.sprite.Sprite):
	def __init__(self, c_map, c_agent_list=None, c_alg=None, _role=None,
				_current_pos=None, _image=None, _image2=None, _algorithm=None, _rand = 0, _index = None):

		# Create Sprite Object for Agent
		pygame.sprite.Sprite.__init__(self)

		# Create Object Variables
		self.agent_pos = _current_pos
		self.c_map = c_map
		# TODO: Need to discuss agent list.
		self.c_agent_list = c_agent_list
		self.c_alg = c_alg
		self.role = _role
		self.image = _image
		self.image2 = _image2
		self.sScale = 1
		self.spriteR = 20 * self.sScale
		self.com_mag = None
		_algorithm = c_alg
		self.facing = 0
		self.rand = _rand
		self.lIndex = _index
		self.totalEvalScore = 0.0
		print("lInd- ",_index)
		self.die = 0

		# TODO: Add vield of vision / direction facing variables

		# TODO: Add functionality for map to decide where agents start
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
		if _algorithm.lower() == "dfs":
			self.algorithm = DFS(self.agent_pos, self.c_map, c_agent_list, self.lIndex)
		elif _algorithm.lower() == "bfs":
			self.algorithm = BFS(self.agent_pos, self.c_map, c_agent_list, self.lIndex)
		elif _algorithm.lower() == "astar" or _algorithm.lower() == "A*":
			self.algorithm = Astar(self.agent_pos, self.c_map, self.lIndex)
		elif _algorithm.lower() == "minmax":
			self.algorithm = MinMax(self.agent_pos, self.c_map, self.c_agent_list, self.lIndex)
		elif _algorithm.lower() == "expmax" or _algorithm.lower() == "expectimax":
			self.algorithm = ExpMax(self.agent_pos, self.c_map, self.lIndex)
		elif _algorithm.lower() == "reflex":
			self.algorithm = Reflex(self.agent_pos, self.c_map,self.c_agent_list, self.rand, self.lIndex)
		elif _algorithm.lower() == "test":
			self.algorithm = testAlgorithm(self.agent_pos, self.c_map,self.c_agent_list, self.lIndex)

		else:
			print("Using generic algorithms.")
			self.algorithm = genericAlgorithms(self.agent_pos, self.c_map)

		# Assign Image
		print("Role: ", self.role)
		if self.role == "hunter":
			self.image = pygame.image.load('./images/r-arrow-small.png')
		elif self.role == "runner":
			self.image = pygame.image.load('./images/b-arrow-small.png')
		else:
			print("ERROR: AGENTS.PY - COULD NOT FIND IMAGE.")
			self.image = pygame.image.load('./images/waldo-small.png')

		# Resize image for gameWindow
		self.image = pygame.transform.scale(self.image, (int(self.spriteR * 2), int(self.spriteR * 2)))


	def update(self, screen):
		'''
		This ultimately calls the search algorithm, chooses the next step, and takes it
		will also need to check for, f.ex tag or escape states, either here or when update
		is called: could create list of Hunter positions, Runner positions, and check overlaps
		'''
		#self.agent_pos = self.algorithm.move()
		# Possible way of doing persistant commands by checking for existing commands in the object.
		if not self.com_mag:
			#print("self.agentpos",self.agent_pos)
			move_result = self.algorithm.move(self.agent_pos)
			print("Move result: ", move_result)

			# kill or convert.  for now, kills on hunter tagging a runner
			if self.getType() == "hunter":
				for a in self.c_agent_list:
					if (a.getType() is not "hunter") and (1>= self.algorithm.manhattanDistance(self.getPos(),a.getPos())):
						#self.c_agent_list.remove(a)
						a.markForDeath()
						a.kill()

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
			else:
				#print("MR: ",move_result)
				self.agent_pos = move_result[0]
				self.facing = move_result[1]
		else:
			first_result = self.com_mag[0]
			self.agent_pos = first_result[0]
			self.facing = first_result[1]
			self.com_mag.pop(0)
		rotated_image = pygame.transform.rotate(self.image, 90*(self.facing))
		#self.image = rotated_image
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
				if position is runner.getPos():
					return True

		elif self.role is 'runner':
			# Runner criteria
			if position in self.c_map.get_safezone():
				return True

		# Return False fallthrough
		return False

	def markForDeath(self):
		self.die = 1
		self.agent_pos = (-999999999,-999999999)

	def shouldDie(self):
		return self.die
