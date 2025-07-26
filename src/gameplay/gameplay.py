# from utils import board, valueFunction, policy
from utils import valueFunction as vf
from utils import policy, board
import numpy as np # type: ignore
import sys, os
import yaml # type: ignore
import json
import random
import ast
from training.manualTraining import parseConfigJson

def parseConfigJson():
    # Get the project root
    baseDir = vf.findProjectRoot()

    # Parse training config
    with open(os.path.join(baseDir,"trainingConfig.json")) as f:
        config = json.load(f)
    
    # Print the config
    return config["test"]

def playGame():
    # Load the config
    config = parseConfigJson()

    # Initialize new agent if left empty
    if config["agent"] == "":
        vfPath = vf.getLatestValueFunction()
    else:
        vfPath = os.path.join(str(vf.findProjectRoot()),'valueFunctions',config["agent"] + ".yaml")
    
    # Load the value function
    valFun = vf.loadValueFunction(vfPath)
    config["agent"] = os.path.splitext(os.path.basename(vfPath))[0]

    # Get games played, alpha, and pctExplore
    gamesPlayed = vf.getGamesPlayed(config["agent"])
    starter = config["starter"]

    # Initialize board
    prevState = '[0,0,0,0,0,0,0,0,0]'
    playerSymbol = config["playerSymbol"]

    # Initialize the game
    if starter == -1:
        board.showBoardXO(prevState,playerSymbol)
        curState = board.playerMakeMove(prevState)
    else:
        prevState = policy.agentMakeMoveTest(prevState,starter,valFun)
        board.showBoardXO(prevState,playerSymbol)
        curState = board.playerMakeMove(prevState)
        board.showBoardXO(curState,playerSymbol)
    
    continueGame = True
    while continueGame:
        # Decide if this move is exploratory
        exploratory = False

        # Make agent move
        nextState = policy.agentMakeMoveTest(curState,starter,valFun)

        # Check for winner
        winner = board.threeAcross(nextState)
        if winner is not None:
            if winner == -1:
                print("Player Wins!")
            else:
                print("Agent Wins!")
            continueGame = False
            board.showBoardXO(nextState,playerSymbol)
            continue
        if board.isdraw(nextState):
            print("Draw!")
            continueGame = False
            board.showBoardXO(nextState,playerSymbol)
            continue

        # Reset states
        prevState = nextState
        board.showBoardXO(prevState,playerSymbol)
        curState = board.playerMakeMove(nextState)

        # Check for winner
        winner = board.threeAcross(curState)
        if winner is not None:
            if winner == -1:
                print("Player Wins!")
            else:
                print("Agent Wins!")
            continueGame = False
            board.showBoardXO(curState,playerSymbol)
            continue

        if board.isdraw(curState):
            print("Draw!")
            continueGame = False
            board.showBoardXO(curState,playerSymbol)

    playerInput = input("\nPlay again> (y/n): ")
    if playerInput.lower() == "y":
        playGame()
    else:
        pass

def main():
    playGame()

if __name__ == "__main__":
    main()