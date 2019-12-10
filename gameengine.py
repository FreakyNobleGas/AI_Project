###########################################################################
###########################################################################
# Authors: Adrien Forkum, Nick Quinn, Karl Horlitz
# Date: 10/26/19
#
# Description: Pygame code for drawing/iterating.  testAgent will be moved
#              into agents.py ultimately, as a base class, and this code
#				will ultimately be changed to run as an instanced trial run
#				through gameEngine()
#
#
#				TODO: implement map drawing
#
#
###########################################################################
###########################################################################

import random
import time
import os.path
import pygame
import agents
import maps


sScale =.5
spriteR = 20 * sScale
#sprite radius.  should be directly related to sprite/grid size
#currently, all sprites are 40x40, so sR=20
#this is a scaling factor only used for sprite movement and window scale


#gamewindow defines window size.  code dependent on window size
#pulls the dimensions from this variable
gameWindow = (100,100)
#NOTE! This will need to likely be dynamic based on the size of the map
#so this value should be overriden in gameEngine.__init__(), taking the
#dimensions of the given map into account

class gameEngine():

	def __init__(self, agentsList, wallList, newMap, safeList = [], c_agent=None, c_alg=None):
		self.wallList = wallList
		wallGroup = pygame.sprite.Group()
		safeGroup = pygame.sprite.Group()
		maxX = 0
		maxY = 0
		global gameWindow
		for i in wallList:
			wallGroup.add(i)
			tempPos = i.getPos()
			if tempPos[0] > maxX:
				maxX = tempPos[0]
			if tempPos[1] > maxY:
				maxY = tempPos[1]
		for i in safeList:
			safeGroup.add(i)

		#gameWindow = (int(2*spriteR*(maxX+1)),int(2*spriteR*(maxY+1)))
		gameWindow = ((maxX+1),(maxY+1))
		print(gameWindow)
		winsize= [0,0] #this is the dimensions of the onscreen window
		#gameWindow holds the dimensions of the game map itself in 1x1 squares
		winsize[0] = int(gameWindow[0]*2*spriteR)
		winsize[1] = int(gameWindow[1]*2*spriteR)
		screen = pygame.display.set_mode(winsize)
		pygame.display.flip()
		if newMap.getGameType() == 0:
			typeString = "Tag Out"
		else:
			typeString = "Zombies"
		pygame.display.set_caption(newMap.getName()+" "+typeString)

		agentGroup = pygame.sprite.Group()
		# agentsList is a list of agents, passed into agentGroup
		totalRunners = 0
		for i in agentsList:
			agentGroup.add(i)
			if i.getType() == "runner":
				totalRunners +=1

		gameOver = 0
		cycleLimit = 10000
		updateGame = 1
		runnerSafe = 0
		# Scoring inaccurate
		while cycleLimit and not gameOver:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameOver = 1
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_ESCAPE:
						gameOver = 1
					if event.key ==  pygame.K_p:
						updateGame = 0
					if event.key == pygame.K_c:
						updateGame = 1
			if updateGame:
				cycleLimit -=1 # only count while updating or pause breaks
				screen.fill((0,0,0)) #this clears the screen.
				agentGroup.update(screen) #runs agent.update() on each agent in group

				# agents themselves should check for if tagged, etc
				wallGroup.update(screen)
				safeGroup.update(screen)
				time.sleep(0.1)#to slow it down
				pygame.display.flip()
				# if all runners in safe state, or all runners dead, end game
				runnerCount = 0
				stillRunning = 0
				for a in agentGroup:
					if (a.getType() == "runner"):
						runnerCount += 1
						if not a.isGoal(a.getPos()):
							stillRunning += 1
						elif a.isGoal(a.getPos()):
							runnerSafe += 1
							a.markForDeath()
							a.kill()
				if (runnerSafe > 0) and (stillRunning == 0):
					print("Runners won!  ",runnerSafe, " runners made it to Goal ", totalRunners-runnerSafe, " were caught")
					gameOver = 1
				elif (runnerCount == 0) and (runnerSafe == 0):
					print("Hunters won!  No remaining Runners, ",totalRunners-runnerSafe, " runners were caught")
					gameOver = 1
			

	def validMove(self,agentPos):
		#this function, in this case, only checks if the proposed move is
		#inside a wall.  More advanced agents may use a more elaborate function
		p = agentPos
		for i in self.wallList:#figure out how to  handle wallList
			j = i.getPos()
			if (j[0] == p[0]) and (j[1] == p[1]):
				#print("Collision")
				return False
		return True

class wallTile(pygame.sprite.Sprite):
	def __init__(self,_current_pos):
		pygame.sprite.Sprite.__init__(self)
		self.thiscolor = (random.randrange(0,255,1),random.randrange(0,255,1),random.randrange(0,255,1))
		self.image = pygame.image.load('./images/bricks-small.png')
		self.image = pygame.transform.scale(self.image, (int(spriteR*2), int(spriteR*2)))
		self.wallPos = _current_pos
		self.rect = pygame.Rect(self.wallPos[0]*2*spriteR,self.wallPos[1]*2*spriteR, spriteR, spriteR)


	def update(self,screen):
		wallPos = self.wallPos
		self.rect = pygame.Rect(self.wallPos[0]*2*spriteR,self.wallPos[1]*2*spriteR, spriteR, spriteR)

		screen.blit(self.image,self.rect)
		#screen.blit() is what actually draws the image to the screen.
		#need to update the rect. with current coordinates before drawing

	def getPos(self):
		return self.wallPos

		
class safeTile(wallTile):
	def __init__(self,_current_pos):
		pygame.sprite.Sprite.__init__(self)
		self.thiscolor = (random.randrange(0,255,1),random.randrange(0,255,1),random.randrange(0,255,1))
		self.image = pygame.image.load('./images/blue-small.png')
		self.image = pygame.transform.scale(self.image, (int(spriteR*2), int(spriteR*2)))
		self.wallPos = _current_pos
		self.rect = pygame.Rect(self.wallPos[0]*2*spriteR,self.wallPos[1]*2*spriteR, spriteR, spriteR)
		#rest of functionality pulled from wallTile, as other than init is identical

#on run, ultimately should loop until win/loss
#loop should iterate each agent one step, then redraw screen
#code below is a basic implementation

if __name__ == "__main__":
	agentList = []
	wallList = []
	maplist = "pacman-large.txt","huge.txt","complex2.txt","complex.txt",  "default.txt",  "empty-large.txt",  "pacman.txt",  "test.txt"
	i = random.randint(0,7)
	chosenMap = "maps/"+maplist[i]
	c_map = maps.Map(chosenMap, c_gameType = random.randint(0,1))#"maps/complex2.txt")
	
	for i in range(0,10):
		r = random.randint(0,10)
		if r == 0:
			_role = "hunter"
			agentList.append(agents.agent(c_map=c_map, c_agent_list=agentList, c_alg = "Reflex", _role = _role,  _index = (len(agentList)), _rand = 2))
		elif r >=1 and r<=3:
			_role = "runner"
			agentList.append(agents.agent(c_map=c_map, c_agent_list=agentList, c_alg = "BFS", _role = _role, _index = (len(agentList))))
		elif r > 3 and r <6:
			_role = "runner"
			agentList.append(agents.agent(c_map=c_map, c_agent_list=agentList, c_alg = "DFS", _role = _role, _index = (len(agentList))))
		elif r >=6 and r <8:
			_role = "runner"
			agentList.append(agents.agent(c_map=c_map, c_agent_list=agentList, c_alg = "Reflex", _role = _role, _index = (len(agentList)), _rand=1))
		else:
			_role = "runner"
			agentList.append(agents.agent(c_map=c_map, c_agent_list=agentList, c_alg = "random", _role = _role,  _index = (len(agentList))))
	#agentList.append(agents.agent(c_map=c_map, c_agent_list=agentList, c_alg = "AStar", _role ="runner", _index = (len(agentList)), _rand=0))
	agentList.append(agents.agent(c_map=c_map, c_agent_list=agentList, c_alg = "BFS", _role ="hunter", _index = (len(agentList))))
	agentList.append(agents.agent(c_map=c_map, c_agent_list=agentList, c_alg = "Reflex", _role ="runner", _index = (len(agentList)), _rand = 1))
	
	wallList = [wallTile(i) for i in (c_map.get_walls()+c_map.get_map_bounds())] # Black Magic
	safeList = [safeTile(i) for i in (c_map.get_safezone())] 
	gameEngine(agentList,wallList, c_map, safeList)
