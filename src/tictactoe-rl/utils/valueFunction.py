import numpy as np
import yaml
import ast
import board
import tomli
import os
from pathlib import Path
import board

# Initialize value function
def initValueFunction():
    # Note: The mapping in the following way
    #   0: Empty space
    #   +1: Agent piece
    #   -1: Opponent piece

    # Create dict for value Function
    valueFunction = {}

    actorCases = [1,-1]

    # Do both starting cases
    for starter in actorCases:
        # Track visited states
        visitedStates = set()
        # Initialize state stack
        stateStack = ['[0,0,0,0,0,0,0,0,0]']
        # Iteratively build cases
        while stateStack: 
            # Get the current state and turn
            curStateStr = stateStack.pop()

            # Check that it's not already accounted for
            # if (curStateStr != '[0,0,0,0,0,0,0,0,0]') & ((curStateStr) in visitedStates):
            if ((curStateStr) in visitedStates):
                continue

            # Add current state to visited states
            visitedStates.add(curStateStr)

            # Turn it into a numerical array
            curStateNum = ast.literal_eval(curStateStr)

            # Get number of open spaces
            openSpaces = [ii for ii, num in enumerate(curStateNum) if num == 0]

            # Check who's move it is
            if (9-len(openSpaces)) % 2 == 0: # Odd, starters turn
                actor = starter
            else: # Even, not starters turn
                actor = starter * -1

            # Set flag to continue game
            continueGame = False

            # Check if this state ends the game
            winner = board.threeAcross(curStateStr)
            if winner == 1: # Agent wins
                curValue = 1
            elif winner == -1: # Opponent wins
                curValue = 0
            elif len(openSpaces) == 0: # Game is a draw
                curValue = 0
            else: #  No winner yet
                curValue = 0.5
                continueGame = True

            # Add state to value function
            valueFunction[curStateStr] = curValue

            # Add next set of states to the stack
            if continueGame:
                for space in openSpaces:
                    nextState = curStateNum.copy()
                    nextState[space] = actor
                    nextStateStr = str(nextState).replace(" ","")
                    stateStack.append(nextStateStr)

    return valueFunction

# Load value function dictionary from file
def loadValueFunction(valFunPath):
    valFunPath = valFunPath.replace("\\", "/")
    with open(valFunPath,'r') as file:
        valueFunction = yaml.safe_load(file)
    return valueFunction

# Write value function dictionary to yaml file
def writeValueFunction(valueFunction,fileName):
    with open(fileName,'w') as file:
        yaml.dump(valueFunction,file,default_flow_style=False)

def findProjectRoot(filename="pyproject.toml"):
    path = Path(__file__).resolve()
    for parent in path.parents:
        if (parent / filename).exists():
            return parent
        
def getLatestValueFunction():
    # Read toml file
    with open('pyproject.toml','rb') as f:
        config = tomli.load(f)
    
    # Extract the version
    ver = config['project']['version']

    # Check if folder exists and create a new name
    rootDir = findProjectRoot()
    valueFunDir = os.path.join(rootDir,"valueFunctions")

    # Check for empty directory
    if os.path.isdir(valueFunDir) and not os.listdir(valueFunDir):
        return None
    
    # Get latest version
    filenames = os.listdir(valueFunDir)
    matches = [f for f in filenames if ver in f]
    suffix = []
    for match in matches:
        suffix.append(match.split('.yaml')[0].split('_')[-1])
    curSuf = chr(ord(max(suffix)))
    fname = ver + '_' + curSuf + ".yaml"
    return os.path.join(valueFunDir,fname)

def generateValueFunctionName():
    # Read toml file
    with open('pyproject.toml','rb') as f:
        config = tomli.load(f)
    
    # Extract the version
    ver = config['project']['version']

    # Check if folder exists and create a new name
    rootDir = findProjectRoot()
    valueFunDir = os.path.join(rootDir,"valueFunctions")
    if not os.path.isdir(valueFunDir):
        os.makedirs(valueFunDir, exist_ok=True)
        valFunPath = os.path.join(valueFunDir,ver+"_A.yaml")
        print(valFunPath)
        return valFunPath

    filenames = os.listdir(valueFunDir)
    matches = [f for f in filenames if ver in f]
    suffix = []
    for match in matches:
        suffix.append(match.split('.yaml')[0].split('_')[-1])
    
    fname = ver + '_' + chr(ord(max(suffix)) + 1)
    valFunPath = os.path.join(valueFunDir,fname)
    # print(valFunPath)
    return valFunPath
    
    
    

    



