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
from agents import *
from algorithms import *
from interface import *
from maps import *



def main():
    print("BEGIN MAIN")
    #interface_foo()
    window = mainWindow()
    map_foo()
    algorithms_foo()
    agents_foo()


main()
