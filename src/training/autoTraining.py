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
    return config["auto"]

def switchStateSign(state):
    # Convert to numerical
    stateNum = ast.literal_eval(state)

    # Switch sign
    stateNum = [x * -1 for x in stateNum]

    # Convert back to a string
    return str(stateNum).replace(" ","")

def doTraining():
    # Get the training config
    config = parseConfigJson()

    # Get agent 1 vf 
    if config['agent1'] == "":
        vf.createNewValueFunction()
        vf1path = vf.getLatestValueFunction()
        vf1 = vf.loadValueFunction(vf1path)
        vf1name = os.path.splitext(os.path.basename(vf1path))[0]
        config['agent1'] = vf1name
    else:
        vf1path = os.path.join(str(vf.findProjectRoot()),'valueFunctions',config["agent1"] + ".yaml")
        vf1 = vf.loadValueFunction(vf1path)
        vf1name = config["agent1"]
    
    # Get agent 2 vf 
    if config['agent2'] == "":
        vf.createNewValueFunction()
        vf2path = vf.getLatestValueFunction()
        vf2 = vf.loadValueFunction(vf2path)
        vf2name = os.path.splitext(os.path.basename(vf2path))[0]
        config['agent2'] = vf2name
    else:
        vf2path = os.path.join(str(vf.findProjectRoot()),'valueFunctions',config["agent2"] + ".yaml")
        vf2 = vf.loadValueFunction(vf2path)
        vf2name = config["agent2"]

    # Set up tracker to track win/loss
    winTracker = []
    alpha1tracker = []

    # Loop through number of training games
    for game in range(config['numberOfGames']):

        # Set initial board state
        prevState = '[0,0,0,0,0,0,0,0,0]'

        # Set training parameters
        alpha1 = policy.setAlpha(config["alpha"],vf.getGamesPlayed(config["agent1"]))
        alpha2 = policy.setAlpha(config["alpha"],vf.getGamesPlayed(config["agent1"]))
        pctExplore = config["pctExplore"]

        alpha1tracker.append(alpha1)

        # Set who goes first (we alternate)
        if vf.getGamesPlayed(config["agent1"]) % 2 == 0:
            starter = 1
            starter1 = 1
            starter2 = -1
        else:
            starter = 2
            starter1 = -1
            starter2 = 1

        # Make first move - agent 2 is the "opponent"
        if starter == 1:
            curState = policy.agentMakeMoveTrain(prevState,starter1,vf1,policy.explore(pctExplore))
        else:
            curState = policy.agentMakeMoveTrain(prevState,starter2,vf2,policy.explore(pctExplore))
            curState = switchStateSign(curState)

        continueGame = True
        while continueGame:

            explore1 = policy.explore(pctExplore)
            explore2 = policy.explore(pctExplore)

            if starter == 1: # It's agent 2's turn
                nextState = policy.agentMakeMoveTrain(switchStateSign(curState),starter2,vf2,explore2)
                nextState = switchStateSign(nextState)
            else: # It's agent 1's turn
                nextState = policy.agentMakeMoveTrain(curState,starter1,vf1,explore1)

            winner = board.threeAcross(nextState)

            if starter == 1: # Updating agent 2
                if winner is not None:
                    vf2 = policy.updateValueFunction(vf2,prevState,nextState,alpha2)
                    continueGame = False
                    winTracker.append(2)
                    continue
                if board.isdraw(nextState):
                    vf2 = policy.updateValueFunction(vf2,prevState,nextState,alpha2)
                    continueGame = False
                    winTracker.append(0)
                    continue
                # Don't update value function if exploratory
                if not explore2:
                    vf2 = policy.updateValueFunction(vf2,prevState,nextState,alpha2)
            else: # Updating agent 1
                if winner is not None:
                    vf1 = policy.updateValueFunction(vf1,prevState,nextState,alpha1)
                    continueGame = False
                    winTracker.append(1)
                    continue
                if board.isdraw(nextState):
                    vf1 = policy.updateValueFunction(vf1,prevState,nextState,alpha2)
                    continueGame = False
                    winTracker.append(0)
                    continue
                # Don't update value function if exploratory
                if not explore1:
                    vf1 = policy.updateValueFunction(vf1,prevState,nextState,alpha1)

            # Reset states
            prevState = curState
            curState = nextState

            explore1 = policy.explore(pctExplore)
            explore2 = policy.explore(pctExplore)

            if starter == 1: # It's agent 1's turn
                nextState = policy.agentMakeMoveTrain(curState,starter1,vf1,explore1)
            else: # It's agent 2's turn
                nextState = policy.agentMakeMoveTrain(switchStateSign(curState),starter2,vf2,explore2)
                nextState = switchStateSign(nextState)

            winner = board.threeAcross(nextState)

            if starter == 1: # Updating agent 1
                if winner is not None:
                    vf1 = policy.updateValueFunction(vf1,prevState,nextState,alpha1)
                    continueGame = False
                    winTracker.append(1)
                    continue
                if board.isdraw(nextState):
                    vf1 = policy.updateValueFunction(vf1,prevState,nextState,alpha1)
                    continueGame = False
                    winTracker.append(0)
                    continue
                # Don't update value function if exploratory
                if not explore1:
                    vf1 = policy.updateValueFunction(vf1,prevState,nextState,alpha1)
            else: # Updating agent 2
                if winner is not None:
                    vf2 = policy.updateValueFunction(vf2,prevState,nextState,alpha2)
                    continueGame = False
                    winTracker.append(2)
                    continue
                if board.isdraw(nextState):
                    vf2 = policy.updateValueFunction(vf2,prevState,nextState,alpha2)
                    continueGame = False
                    winTracker.append(0)
                    continue
                # Don't update value function if exploratory
                if not explore2:
                    vf2 = policy.updateValueFunction(vf2,prevState,nextState,alpha2)

            # Reset states
            prevState = curState
            curState = nextState

        vf.incrementGamesPlayed(config["agent1"])
        vf.incrementGamesPlayed(config["agent2"])
    
    vf.writeValueFunction(vf1,vf1path)
    vf.writeValueFunction(vf2,vf2path)
    
def main():
    doTraining()

if __name__ == "__main__":
    main()
