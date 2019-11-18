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
	def __init__(self, map_name=None):
		self.safe_zone = []
		self.walls = []
		self.map_bounds = []
		self.map_name = map_name
		self.get_map_assets(map_name)
		
	def map_foo(self):
		print("In Map Foo")
		
	def get_map_assets(self, map_name):
		if map_name is None:
			path = 'maps/default.txt'
		else:
			path = "maps/" + map_name
		game_map = open(path, 'r')
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
				elif m_asset is '-' or m_asset is '|':
					self.walls.append((x_coord, y_coord))
				elif m_asset is 'S':
					self.safe_zone.append((x_coord, y_coord))
				x_coord += 1
			if not h_flag:
				y_coord += 1
