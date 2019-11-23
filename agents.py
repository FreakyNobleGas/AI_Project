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



sScale =.5
spriteR = 20*sScale

class Hunter:
	def __init__(self, _current_pos=None, _image=None, _image2=None, _algorithm=None):
		self.current_pos = _current_pos
		self.image = _image
		self.image2 = _image2
		self.algorithm = _algorithm
		self.agentPos = _current_pos

class Runner:
	def __init__(self, _current_pos=None, _image=None, _image2=None, _algorithm=None):
		self.current_pos = _current_pos
		self.image = _image
		self.image2 = _image2
		self.algorithm = _algorithm
		self.agentPos = _current_pos



class testAgent(pygame.sprite.Sprite):
	def __init__(self,gameWindow,_current_pos=None, _image=None, _image2=None, _algorithm=None):
		pygame.sprite.Sprite.__init__(self)
		self.thiscolor = (random.randrange(0,255,1),random.randrange(0,255,1),random.randrange(0,255,1))
		self.agentAlgorithm = _algorithm
		self.image = _image
		self.image2 = _image2
		self.agentPos = _current_pos
		self.hunter = 1
		#self.wallList = wallList
		#we won't use this- ultimately will be pulling from agents.py
		if self.agentPos == None:
			self.agentPos = [random.randrange(3,gameWindow[0]-3,1),random.randrange(3,gameWindow[1]-3,1)]
		self.rect = pygame.Rect(self.agentPos[0],self.agentPos[1], spriteR, spriteR)
		if self.image == None:
			if not random.randrange(0,5,1):
				self.image = pygame.image.load('./images/waldo-small.png')
				self.hunter = 0
			else:
				self.image = pygame.image.load('./images/predator-small.png')
			self.image = pygame.transform.scale(self.image, (int(spriteR*2), int(spriteR*2)))

		
	def update(self,screen,gameWindow, wallList):
		#this ultimately calls the search algorithm, chooses the next step, and takes it
		#will also need to check for, f.ex tag or escape states, either here or when update
		#is called- could create list of Hunter positions, Runner positions, and check overlaps
		agentPos = self.agentPos
		self.algorithm(wallList,gameWindow)	

		self.rect = pygame.Rect(self.agentPos[0]*2*spriteR,self.agentPos[1]*2*spriteR, spriteR, spriteR)
		screen.blit(self.image,self.rect)
		#screen.blit() is what actually draws the image to the screen.
		#need to update the rect. with current coordinates before drawing
		#print("X: ",agentPos[0]," Y: ", agentPos[1])
		
		
	def algorithm(self,wallList , gameWindow):
		if self.agentAlgorithm == None:
			agentPos = self.agentPos
			#random movement code
			x = (random.randrange(0,3,1)-1)
			y = (random.randrange(0,3,1)-1)
			agentPos[0] += x
			agentPos[1] += y
			if not self.validMove(wallList):#undo move if collides with a wall
				agentPos[0] -= x
				agentPos[1] -= y
				None
			#print("Pos: ",agentPos)
			self.agentPos = agentPos
			#out of bounds collision.  real Agents should keep this from happening
			#by not taking invalid moves offscreen
			if agentPos[0] < 1:
				agentPos[0] = 1
			if agentPos[1] < 1:
				agentPos[1] = 1
			if agentPos[0] > (gameWindow[0]-2):
				agentPos[0] = (gameWindow[0]-2)
			if agentPos[1] > (gameWindow[1]-2):
				agentPos[1] = (gameWindow[1]-2)
		else:
			#use algorithm
			None


	def validMove(self,wallList):
		#this function, in this case, only checks if the proposed move is
		#inside a wall.  More advanced agents may use a more elaborate function
		p = self.agentPos
		for i in wallList:
			j = i.getPos()
			if (j[0] == p[0]) and (j[1] == p[1]):
				#print("Collision")
				return False
		return True
	
	def getposition(self):
		return agentPos
