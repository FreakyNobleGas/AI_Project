###########################################################################
###########################################################################
# Authors: Adrien Forkum, Nick Quinn, Karl Horlitz
# Date: 10/26/19
#
# Description: This file contains all the game map data and map generation
#              functions.
#
###########################################################################
###########################################################################

class Map():
	"""
	"Description: Object that cointains the file name of the map and the
	"             x,y coordinates of map assets i.e. walls, map boundry.
	"
	"Input: String that is the name of map file.
	"""
	def __init__(self, map_name=None, c_gameType = 0):
		self.safe_zone = []
		self.walls = []
		self.map_bounds = []
		self.hunter_spawn = []
		self.runner_spawn = []
		self.x_bound = None
		self.y_bound = None
		self.map_name = map_name
		self.get_map_assets(map_name)
		self.gameType = c_gameType

	def map_foo(self):
		print("In Map Foo")

	def get_map_assets(self, map_name):
		"""
		"Description: Takes a map name to retrieve the map assets from
		"             a file and attain x,y coordinates for those assets.
		"
		"Input: String that is the map file name.
		"
		"Output: None
		"""

		# Take the given file name and return the file
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
					self.map_bounds.append((x_coord, y_coord))
					#self.walls.append((x_coord, y_coord))
				elif m_asset is '-' or m_asset is '|':
					self.walls.append((x_coord, y_coord))
				elif m_asset is 'S':
					self.safe_zone.append((x_coord, y_coord))
				elif m_asset is 'R':
					self.runner_spawn.append((x_coord, y_coord))
				elif m_asset is 'H':
					self.hunter_spawn.append((x_coord, y_coord))
				x_coord += 1
			if not h_flag:
				y_coord += 1

		game_map.close()

		self.x_bound = x_coord
		self.y_bound = y_coord

	def get_walls(self):
		return self.walls
	
	def get_hspawn(self):
		return self.hunter_spawn
	
	def get_rspawn(self):
		return self.runner_spawn

	def out_of_bounds(self, move):
		"""
		Checks to see if (x, y) is inside of map and not in a wall.

		:move: A tuple that contains the x and y coordinates of a move.
		"""
		if move[0] < 0 or move[0] > self.x_bound or move[1] < 0 or move[1] > self.y_bound:
			return False
		elif move in self.walls or move in self.map_bounds:
			return False
		else:
			return True

	def get_map_bounds(self):
		return self.map_bounds

	def get_safezone(self):
		return self.safe_zone

	def get_next(self, agent_position):
		"""
		Takes a current position and returns possible moves based on that position.

		:agent_position: A tupple of the agent's current position.
		"""
		valid_moves = []
		north = (agent_position[0], agent_position[1] + 1)
		south = (agent_position[0], agent_position[1] - 1)
		east = (agent_position[0] + 1, agent_position[1])
		west = (agent_position[0] - 1, agent_position[1])
		next_moves = [(north, 3), (south, 1), (east, 0), (west, 2)]

		for move, direction in next_moves:
			 if self.out_of_bounds(move):
				 valid_moves.append((move, direction))
		#print("Valid Moves: ", valid_moves)

		return valid_moves
		
	def getGameType(self):
		return self.gameType
	
	def getName(self):
		return self.map_name
		
