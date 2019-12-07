# AI_Project

** NEED TO UPDATE AS PROJECT DEVELOPS **

Authors: Adrien, Karl, and Nick


Project Overview
----------------

In this project, we create a program that simulates multiple AI agents using searching algorithms, heuristics, and local search. 


Game Rules
----------

- There are two seperate AI groups: Hunters and Runners.
- The hunters chase the runners, both behave based on various algorithms
- The Runners have a goal state of escaping to a blue "Safe" zone
- Some algorithms for Runners (DFS, BFS) are simple find path -> follow path
- Other algorithms consider if a hunter is nearby, and prioritize short term survival



Usage
-----
To run the game, run:
python3 driver.py

This will open the UI that allows you to select the map, agent and other rules.

Running gameengine.py standalone (python3 gameengine.py)  will start a demo run, using a randomly chosen map, a random assortment of 20 runners using various algorithms, and a single Reflex hunter.



The goal of this project is to create multiple A.I. agents, and teach them to play Freeze Tag using genetic algorithms. This project is written in Python and utilizes the SFML graphics libraries.
