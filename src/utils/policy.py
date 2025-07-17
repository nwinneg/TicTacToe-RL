import numpy as np # type: ignore
import random
from utils import valueFunction as vf
from utils import board

# Function to facilitate the agent making a move during training
def agentMakeMoveTrain(curState,starter,valueFunction,explore):
    # Get list of next states and associated values
    moveOptions = board.getNextStates(curState,starter)
    moveValues = [valueFunction[move] for move in moveOptions]

    # If we are exploring, choose a move at random
    if explore:
        moveIndex = random.randint(0,len(moveValues)-1)
    else:
        moveIndex = np.argmax(np.array(moveValues))

    if explore:
        return moveOptions[moveIndex]
    else:
        return moveOptions[moveIndex]

# Function to facilitate the agent making a move during testing
def agentMakeMoveTest(curState,starter,valueFunction):
    # Get list of next states and associated values
    moveOptions = board.getNextStates(curState,starter)
    moveValues = [valueFunction[move] for move in moveOptions]

    # We don't explore in testing
    moveIndex = np.argmax(np.array(moveValues))

    if explore:
        return moveOptions[moveIndex]
    else:
        return moveOptions[moveIndex]

# Function to decide whether a move is exploratory (or exploitative)
def explore(pctExplore):
    # Decide whether this is an exploratory move 
    explore = False
    if pctExplore > 0:
        # choose a random number from 0-100
        if random.randint(0,100) < pctExplore:
            explore = True

    return explore

# Function to update the value function
def updateValueFunction(valueFunction,prevState,curState,alpha):
    # Get the value before the greedy move
    v = valueFunction[prevState]
    vprime = valueFunction[curState]

    # Get the new value before the greedy move
    vnew = v + (vprime - v)*alpha

    # Update the value function
    valueFunction[prevState] = vnew

    return valueFunction

# TODO: Function to set alpha based on number of games
def setAlpha(alpha,ratio):
    return alpha * ratio
    