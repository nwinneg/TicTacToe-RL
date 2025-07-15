import numpy as np
import os
import yaml
import ast
import tomli
from pathlib import Path

# Initialize value function
def initValueFunction():
    # Note: The mapping in the following way
    #   0: Empty space
    #   +1: Agent piece
    #   -1: Opponent piece

    # Create dict for value Function
    valueFunction = {}

    actorCases = [1,-1]
    visitedStates = set()

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
            winner = threeAcross(curStateStr)
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
        print(len(visitedStates))
    return valueFunction

def countWinningStates(valueFunction):
    keyList = list(valueFunction.keys())
    totalWins = 0
    for key in keyList:
        values = list(valueFunction[key]['actions'].values())
        totalWins += values.count(0)
    print("Total wins: {}".format(totalWins))

def showBoard(boardStr):
    boardNum = ast.literal_eval(boardStr)
    print(np.array(boardNum).reshape(3,3))

# Write value function dictionary to yaml file
def writeValueFunction(valueFunction,fileName):
    with open(fileName,'w') as file:
        yaml.dump(valueFunction,file,default_flow_style=False)

# Load value function dictionary from file
def loadValueFunction(valFunPath):
    valFunPath = valFunPath.replace("\\", "/")
    with open(valFunPath,'r') as file:
        valueFunction = yaml.safe_load(file)
    return valueFunction

# Function to check if there are 3 across - We can win on a row, a column, or one of the diagonals
def threeAcross(boardStateString): # Returns winner (-1 or 1) if there is a winner, otherwise returns None
    # Reformat as a matrix
    boardArr = ast.literal_eval(boardStateString)
    boardMat = np.array(boardArr).reshape(3,3)

    # Check the case we've won on a row
    for row in range(3):
        if np.abs(boardMat[row,:].sum()) == 3: # Someone won on a row
            return boardMat[row,0]
        
    for col in range(3):
        if np.abs(boardMat[:,col].sum()) == 3: # Someone won on a column
            return boardMat[0,col]
    
    if np.abs(np.diag(boardMat).sum()) == 3: # Someone won on a diag
        return boardMat[0,0]
    
    if np.abs(np.diag(np.fliplr(boardMat)).sum()) == 3: # Someone won on the other diag
        return boardMat[0,2]
    
    # Return none if no winner
    return None

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
        return valFunPath

    filenames = os.listdir(valueFunDir)
    if len(filenames) == 0:
        os.makedirs(valueFunDir, exist_ok=True)
        valFunPath = os.path.join(valueFunDir,ver+"_A.yaml")
        return valFunPath
    
    matches = [f for f in filenames if ver in f]
    suffix = []
    for match in matches:
        suffix.append(match.split('.yaml')[0].split('_')[-1])
    
    fname = ver + '_' + chr(ord(max(suffix)) + 1) + '.yaml'
    valFunPath = os.path.join(valueFunDir,fname)
    return valFunPath
    
def main():
    valueFunction = initValueFunction()
    fname = generateValueFunctionName()
    print(fname)
    print(len(valueFunction))
    # print(valueFunction['[1,-1,1,-1,0,0,0,0,0]'])
    # print(valueFunction['[-1,1,-1,1,0,0,0,0,0]'])
    writeValueFunction(valueFunction,fname)
    # valueFunction = loadValueFunction('valueFunction.yaml')
    # countWinningStates(valueFunction)

    ## Change to only save agent actions ... we have duplicates
    

if __name__ == "__main__":
    main()