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

import pygame

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
