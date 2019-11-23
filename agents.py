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

class agent(pygame.sprite.Sprite):
	def __init__(self, gameWindow,_current_pos=None, _image=None, _image2=None, _algorithm=None,
				c_map, c_agent, c_alg, _role, _screen):

		# Create Sprite Object for Agent
		pygame.sprite.Sprite.__init__(self)

		# Create Object Variables
		self.agent_pos = _current_pos
		self.c_map = c_map
		self.c_agent = c_agent
		self.c_alg = c_alg
		self.role = _role
		self.image = _image
		self.image2 = _image2
		self.sScale = .5
		self.spriteR = 20 * self.sScale


		# TODO: Add vield of vision / direction facing variables

		# TODO: Add functionality for map to decide where agents start
		if self.agent_pos == None:
			self.agent_pos = [random.randrange(3,gameWindow[0]-3,1),random.randrange(3,gameWindow[1]-3,1)]

		# Create sprite image based on location and dimensions
		self.rect = pygame.Rect(self.agent_pos[0],self.agent_pos[1], spriteR, spriteR)

		# Assign Agent Algorithm
		if _algorithm == "DFS":
			self.algorithm = DFS(self.agent_pos, self.c_map)
		elif _algorithm == "BFS":
			self.algorithm = BFS(self.agent_pos, self.c_map)
		elif _algorithm == "Astar":
			self.algorithm = Astar(self.agent_pos, self.c_map)
		elif _algorithm == "MinMax":
			self.algorithm = MinMax(self.agent_pos, self.c_map)
		elif _algorithm == "ExpMax":
			self.algorithm = ExpMax(self.agent_pos, self.c_map)
		else:
			print("Using generic algorithms.")
			self.algorithm = genericAlgorithms()

		# Assign Image
		if self.roles == "hunter":
			self.image = pygame.image.load('./images/predator-small.png')
		if self.roles == "runner":
			self.image = pygame.image.load('./images/waldo-small.png')
		else:
			print "ERROR: AGENTS.PY - COULD NOT FIND IMAGE."
			exit()

		# Resize image for gameWindow
		self.image = pygame.transform.scale(self.image, (int(self.spriteR * 2), int(self.spriteR * 2)))


	def update(self, screen):
		'''
		This ultimately calls the search algorithm, chooses the next step, and takes it
		will also need to check for, f.ex tag or escape states, either here or when update
		is called: could create list of Hunter positions, Runner positions, and check overlaps
		'''
		self.agent_pos = self.algorithm.move()

		self.rect = pygame.Rect(self.agent_pos[0] * 2 * spriteR,
								self.agent_pos[1] * 2 * spriteR,
								spriteR,
								spriteR)

		# Draw screen to image
		screen.blit(self.image, self.rect)
