import ast
import numpy as np

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

def isdraw(boardStateString): # Returns true if draw
    boardArr = ast.literal_eval(boardStateString)
    openSpaces = [ii for ii, num in enumerate(boardArr) if num == 0]
    if len(openSpaces) == 0:
        return True
    else:
        return False

# Function to get available next movies
def getNextStates(curStateStr,starter):
    # Convert state to numerical array
    curStateNum = ast.literal_eval(curStateStr)
    
    # Get open spaces and actor (startingPlayer = 1 for agent, -1 for player)
    openSpaces = [ii for ii, num in enumerate(curStateNum) if num == 0]
    if (9-len(openSpaces)) % 2 == 0: # Odd, starters turn
        actor = starter
    else: # Even, not starters turn
        actor = starter * -1

    # for space in openSpaces:
    stateList = []
    for space in openSpaces:
        nextState = curStateNum.copy()
        nextState[space] = actor
        nextStateStr = str(nextState).replace(" ","")
        stateList.append(nextStateStr)
    
    return stateList

# Function to visualize a board state
def showBoard(boardStr):
    boardNum = ast.literal_eval(boardStr)
    print(np.array(boardNum).reshape(3,3))

def showBoardXO(boardStr,playerSymbol):
    # Convert to array of strings
    boardNum = ast.literal_eval(boardStr)
    board = [str(num) for num in boardNum]

    # Convert to X's and O's
    board = [playerSymbol if val == "-1" else val for val in board]
    if playerSymbol == 'X':
        board = ['O' if val == "1" else val for val in board]
    else:
        board = ['X' if val == "1" else val for val in board]
    board = [' ' if val == "0" else val for val in board]

    # Show the board
    print(board[0] + " | " + board[1] + " | " + board[2])
    print("--+---+--")
    print(board[3] + " | " + board[4] + " | " + board[5])
    print("--+---+--")
    print(board[6] + " | " + board[7] + " | " + board[8])