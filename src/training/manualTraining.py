# from utils import board, valueFunction, policy
from utils import valueFunction as vf
from utils import policy, board
import numpy as np # type: ignore
import sys, os
import yaml # type: ignore
import json
import random
import ast

def parseConfigJson():
    # Get the project root
    baseDir = vf.findProjectRoot()

    # Parse training config
    with open(os.path.join(baseDir,"trainingConfig.json")) as f:
        config = json.load(f)
    
    # Print the config
    return config["manual"]

def writeConfigJson(manualConfig):
    # Get the project root
    baseDir = vf.findProjectRoot()

    # Parse training config
    with open(os.path.join(baseDir,"trainingConfig.json"),'r') as f:
        config = json.load(f)
    
    config["manual"] = manualConfig

    with open(os.path.join(baseDir,"trainingConfig.json"),'w') as f:
        json.dump(config,f,indent=4)

def playGame():
    # Load the confi
    config = parseConfigJson()

    # Initialize new agent if left empty
    if config["agent"] == "":
        vf.createNewValueFunction()
        newName = vf.getLatestValueFunction()
        config["agent"] = os.path.splitext(os.path.basename(newName))[0]
        writeConfigJson(config)

    # Load the value function
    vfPath = os.path.join(str(vf.findProjectRoot()),'valueFunctions',config["agent"] + ".yaml")
    valFun = vf.loadValueFunction(vfPath)

    # Get games played, alpha, and pctExplore
    gamesPlayed = vf.getGamesPlayed(config["agent"])
    alpha = policy.setAlpha(config["alpha"],gamesPlayed/config["numberOfGames"])
    pctExplore = config["pctExplore"]

    # Set who goes first (we alternate)
    if gamesPlayed % 2 == 0:
        starter = -1
    else:
        starter = 1

    # Initialize board
    prevState = '[0,0,0,0,0,0,0,0,0]'
    playerSymbol = config["playerSymbol"]

    # Initialize the game
    if starter == -1:
        board.showBoardXO(prevState,playerSymbol)
        curState = board.playerMakeMove(prevState)
    else:
        prevState = policy.agentMakeMoveTrain(prevState,starter,valFun,policy.explore(pctExplore))
        board.showBoardXO(prevState,playerSymbol)
        curState = board.playerMakeMove(prevState)
        board.showBoardXO(curState,playerSymbol)
    
    continueGame = True
    while continueGame:
        # Decide if this move is exploratory
        exploratory = policy.explore(pctExplore)

        # Make agent move
        nextState = policy.agentMakeMoveTrain(curState,starter,valFun,exploratory)

        # Check for winner
        winner = board.threeAcross(nextState)
        if winner is not None:
            valFun = policy.updateValueFunction(valFun,prevState,nextState,alpha)
            if winner == -1:
                print("Player Wins!")
            else:
                print("Agent Wins!")
            continueGame = False
            board.showBoardXO(nextState,playerSymbol)
            continue
        if board.isdraw(nextState):
            print("Draw!")
            valFun = policy.updateValueFunction(valFun,prevState,nextState,alpha)
            continueGame = False
            board.showBoardXO(nextState,playerSymbol)
            continue
            
        # Don't update value function if exploratory
        if not exploratory:
            valFun = policy.updateValueFunction(valFun,prevState,nextState,alpha)

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
            valFun = policy.updateValueFunction(valFun,nextState,curState,alpha)
            board.showBoardXO(curState,playerSymbol)
            continue

        if board.isdraw(curState):
            print("Draw!")
            continueGame = False
            valFun = policy.updateValueFunction(valFun,nextState,curState,alpha)
            board.showBoardXO(curState,playerSymbol)

    vf.writeValueFunction(valFun,vfPath)
    vf.incrementGamesPlayed(config["agent"])

    playerInput = input("\nPlay again> (y/n): ")
    if playerInput.lower() == "y":
        playGame()
    else:
        pass

def main():
    playGame()

if __name__ == "__main__":
    main()