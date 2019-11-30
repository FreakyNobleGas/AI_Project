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


sScale =1
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

	def __init__(self, agentsList, wallList, newMap, c_agent=None, c_alg=None):
		self.wallList = wallList
		wallGroup = pygame.sprite.Group()
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

		#gameWindow = (int(2*spriteR*(maxX+1)),int(2*spriteR*(maxY+1)))
		gameWindow = ((maxX+1),(maxY+1))
		print(gameWindow)
		winsize= [0,0] #this is the dimensions of the onscreen window
		#gameWindow holds the dimensions of the game map itself in 1x1 squares
		winsize[0] = int(gameWindow[0]*2*spriteR)
		winsize[1] = int(gameWindow[1]*2*spriteR)
		screen = pygame.display.set_mode(winsize)
		pygame.display.flip()
		pygame.display.set_caption('Freeze Tag')

		agentGroup = pygame.sprite.Group()
		# agentsList is a list of agents, passed into agentGroup
		for i in agentsList:
			agentGroup.add(i)

		gameOver = 0
		updateGame = 1
		while not gameOver:
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
				screen.fill((0,0,0)) #this clears the screen.
				agentGroup.update(screen) #runs agent.update() on each agent in group

				# agents themselves should check for if tagged, etc
				wallGroup.update(screen)
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
				if (runnerCount > 0) and (stillRunning == 0):
					print("Runners won!  All remaining runners at Goal")
					gameOver = 1
				elif runnerCount == 0:
					print("Hunters won!  No remaining Runners")
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

	def manhattanDistance():
		None#Foo.



class tempGetMap():
	#this is a temporary getmap function to figure out how to handle map passing
	def __init__(self,map_name=None):
		self.safe_zone = []
		self.walls = []
		self.map_bounds = []
		self.map_name = map_name
		#self.get_map_assets(map_name)
		if map_name is None:
			path = 'maps/default.txt'
		else:
			path = map_name
		game_map = open(path, 'r')

		# Loop through opened map file to parse the x,y coordinates
		y_coord = 0
		for line in game_map.readlines():
			x_coord = 0
			h_flag = False
			for m_asset in line:
				if m_asset is '#' or not line.strip():
					h_flag = True
					break
				if m_asset is '=':
					self.walls.append((x_coord, y_coord))
				elif m_asset is '-' or m_asset is '|':
					self.walls.append((x_coord, y_coord))
				elif m_asset is 'S':
					self.safe_zone.append((x_coord, y_coord))
				x_coord += 1
			if not h_flag:
				y_coord += 1

		game_map.close()

	def getWalls(self):
		return self.walls



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
		#print("Xw: ",wallPos[0]," Yw: ", wallPos[1])

	def getPos(self):
		return self.wallPos


#on run, ultimately should loop until win/loss
#loop should iterate each agent one step, then redraw screen
#code below is a basic implementation

if __name__ == "__main__":
	agentList = []
	wallList = []
	#tempWalls = tempGetMap("maps/pacman.txt")
	c_map = maps.Map("maps/test.txt")
	#c_map.get_map_assets()
	c_agent_list = []
	'''
	for i in range(0,5):
		r = random.randrange(0,5,1)
		if r == 0:
			_role = "runner"
			agentList.append(agents.agent(c_map=c_map, c_agent_list=c_agent_list, c_alg = "BFS", _role = _role))
		else:
			_role = "runner"
			agentList.append(agents.agent(c_map=c_map, c_agent_list=c_agent_list, c_alg = "DFS", _role = _role))
	agentList.append(agents.agent(c_map=c_map, c_agent_list=agentList, c_alg = "test", _role ="hunter"))'''
	agentList.append(agents.agent(c_map=c_map, c_agent_list=agentList, c_alg = "DFS", _role ="runner", _index = (len(agentList))))
	agentList.append(agents.agent(c_map=c_map, c_agent_list=agentList, c_alg = "BFS", _role ="runner", _index = (len(agentList))))
	agentList.append(agents.agent(c_map=c_map, c_agent_list=agentList, c_alg = "MinMax", _role ="hunter",_rand=20, _index = (len(agentList))))
	
	#agentList.append(agents.agent(c_map=c_map, c_agent_list=agentList, c_alg = "DFS", _role ="runner", _index = (len(agentList))))
	#agentList.append(agents.agent(c_map=c_map, c_agent_list=agentList, c_alg = "MinMax", _role ="hunter", _index = (len(agentList))))
	
	
	#c_agent_list.append(agents.agent(c_map=c_map, c_agent_list=agentList, c_alg = "test", _role ="hunter"))
	
	
	wallList = [wallTile(i) for i in (c_map.get_walls()+c_map.get_map_bounds())] # Black Magic
	gameEngine(agentList,wallList, c_map)
