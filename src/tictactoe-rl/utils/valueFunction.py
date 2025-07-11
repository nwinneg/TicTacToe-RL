import numpy as np
import yaml
import ast
import board
import tomli
import os
from pathlib import Path

# Initialize value function
def initValueFunction():
    # Note: The mapping in the following way
    #   0: Empty space
    #   +1: Agent piece
    #   -1: Opponent piece

    # Create dict for value Function
    valueFunction = {}

    stateStack = [
        '[0,0,0,0,0,0,0,0,0]',
        '[0,0,0,0,0,0,0,0,0]'
    ]
    actorStack = [1,-1]

    visitedStates = set()
    winningStates = set()
    losingStates = set()
    tieStates = set()
     
    # Iteratively build all future states
    while stateStack:
        # Get the current state and turn
        curStateStr = stateStack.pop()
        curActor = actorStack.pop()

        # Check that it's not already accounted for
        if (curStateStr,curActor) in visitedStates:
            continue

        # Turn it into a numerical array
        curStateNum = ast.literal_eval(curStateStr)

        # Get number of open spaces
        openSpaces = [ii for ii, num in enumerate(curStateNum) if num == 0]

        # Generate next states and create value function entry
        subDict = {}
        nextStates = []
        nextActors = []
        for space in openSpaces:
            nextState = curStateNum.copy()
            nextState[space] = curActor
            nextStateStr = str(nextState).replace(" ","")
            winner = board.threeAcross(nextStateStr)
            if winner == 1: # The agent won
                subDict[nextStateStr] = 1
                winningStates.add(nextStateStr)
            elif winner == -1: # The opponent won
                subDict[nextStateStr] = 0
                losingStates.add(nextStateStr)
            elif 0 not in nextState: # The game is a draw
                subDict[nextStateStr] = 0
                tieStates.add(nextStateStr)
            else: # No winner yet
                subDict[nextStateStr] = 0.5
                nextStates.append(nextStateStr)
                nextActors.append(curActor * -1)

        valueFunction[curStateStr] = {
            'actions' : subDict,
            'actor' : curActor
        }

        # Push set of next states and actors to stack
        for ii in range(len(nextStates)):
            stateStack.append(nextStates[ii])
            actorStack.append(nextActors[ii])

        visitedStates.add((curStateStr,curActor))

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
    print(valFunPath)
    return valFunPath
    
    
    

    



