import numpy as np
import sys
import os
import random
import yaml
import ast

sys.path.append(os.path.abspath("src/tictactoe-rl/utils"))
# import board, policy, valueFunction
from utils import board, policy, valueFunction as vf

def agentMakeMove(curState,starter,valueFunction,explore):
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

def playerMakeMove(curState,playerSymbol):
    # Show the player the board
    boardNum = ast.literal_eval(curState)

    # Get input from the player
    valueInput = False
    while not valueInput:
        playerInput = input("Enter move: ")
        try:
            playerInput = int(playerInput)
        except:
            print('Input must be a single digit integer from 1-9')
        if boardNum[playerInput-1] == 0: # Valid move
            valueInput = True
        else: # Not valud move
            print('Please choose an empty square')
    
    # Input player move and return next state as string
    boardNum[playerInput - 1] = -1
    nextState = str(boardNum).replace(" ","")
    return nextState

def updateValueFunction(valueFunction,prevState,curState,alpha):
    # Get the value before the greedy move
    v = valueFunction[prevState]
    vprime = valueFunction[curState]

    # Get the new value before the greedy move
    vnew = v + (vprime - v)*alpha

    # Update the value function
    valueFunction[prevState] = vnew

    return valueFunction

def gameplay(valueFunction, alpha, pctExplore, starter):
    # Initialize board
    prevState = '[0,0,0,0,0,0,0,0,0]'
    playerSymbol = 'X'

    # Initialize the game
    if starter == -1:
        board.showBoardXO(prevState,playerSymbol)
        curState = playerMakeMove(prevState,playerSymbol)
    else:
        prevState = agentMakeMove(prevState,starter,valueFunction,policy.explore(pctExplore))
        board.showBoardXO(prevState,playerSymbol)
        curState = playerMakeMove(prevState,playerSymbol)
        board.showBoardXO(curState,playerSymbol)
    
    continueGame = True
    while continueGame:
        # Decide if this move is exploratory
        exploratory = policy.explore(pctExplore)

        # Make agent move
        nextState = agentMakeMove(curState,starter,valueFunction,exploratory)

        # Check for winner
        winner = board.threeAcross(nextState)
        if winner is not None:
            valueFunction = updateValueFunction(valueFunction,prevState,nextState,alpha)
            if winner == -1:
                print("Player Wins!")
            else:
                print("Agent Wins!")
            continueGame = False
            board.showBoardXO(nextState,playerSymbol)
            continue
        if board.isdraw(nextState):
            print("Draw!")
            valueFunction = updateValueFunction(valueFunction,prevState,nextState,alpha)
            continueGame = False
            board.showBoardXO(nextState,playerSymbol)
            continue
            
        # Update value function if exploratory
        if not exploratory:
            valueFunction = updateValueFunction(valueFunction,prevState,nextState,alpha)

        # Reset states
        prevState = nextState
        board.showBoardXO(prevState,playerSymbol)
        curState = playerMakeMove(nextState,playerSymbol)

        # Check for winner
        winner = board.threeAcross(curState)
        if winner is not None:
            if winner == -1:
                print("Player Wins!")
            else:
                print("Agent Wins!")
            continueGame = False
            valueFunction = updateValueFunction(valueFunction,nextState,curState,alpha)
            board.showBoardXO(curState,playerSymbol)
            continue

        if board.isdraw(curState):
            print("Draw!")
            continueGame = False
            valueFunction = updateValueFunction(valueFunction,nextState,curState,alpha)
            board.showBoardXO(curState,playerSymbol)

    
    return valueFunction
    
    
def main():
    fileName = vf.getLatestValueFunction()
    valueFunction = vf.loadValueFunction(fileName)
    
    alpha = 0.1
    pctExplore = 10
    starter = 1
    valueFunction = gameplay(valueFunction,alpha,pctExplore,starter)

    lst = valueFunction.values()
    filtered = [x for x in lst if x not in {0, 0.5, 1}]
    print(filtered)  # Output: [2, 3.5, 0.1, 1.1]
    vf.writeValueFunction(valueFunction,fileName)


if __name__ == "__main__":
    main()