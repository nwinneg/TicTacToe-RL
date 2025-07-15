import numpy as np
import random
import valueFunction

def chooseNextMove(curState,pctExplore):
    # Decide whether this is an exploratory move 
    if pctExplore > 0:
    # choose a random number from 0-100
        pass

def explore(pctExplore):
    # Decide whether this is an exploratory move 
    explore = False
    if pctExplore > 0:
        # choose a random number from 0-100
        if random.randint(0,100) < pctExplore:
            explore = True

    return explore