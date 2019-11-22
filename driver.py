###########################################################################
###########################################################################
# Authors: Adrien Forkum, Nick Quinn, Karl Horlitz
# Date: 10/26/19
#
# Description: This file is the start point for the entire program and contains
#              all neccessary library imports and driver code to execute the program.
#
# Requirements: Python3.5 or higher. PYQT5 graphics library installed.
#
# Usage: Python3 driver.py
###########################################################################
###########################################################################

# Library Imports
from interface import *

class Driver:
    """
    Class that is used to run the program and contains all the game elements.
    """
    def __init__(self):
        self.map = None
        self.agents = []
        self.algorithm = None
        self.driver_window()
        
    def driver_window(self):
        print("BEGIN MAIN")
        window = mainWindow()
        print (window.c_map)
        print (window.c_agent)
        print (window.c_alg)

if __name__ == "__main__":
    run_driver = Driver()
