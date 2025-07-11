import ast
import numpy as np

# Function to check if there are 3 across - We can win on a row, a column, or one of the diagonals
def threeAcross(boardStateString): # Returns winner (-1 or 1) if there is a winner, otherwise returns None
    # Reformat as a matrix
    boardArr = ast.literal_eval(boardStateString)
    boardMat = np.array(boardArr).reshape(3,3)

# Function to visualize a board state
def showBoard(boardStr):
    # TODO
    boardNum = ast.literal_eval(boardStr)
    print(np.array(boardNum).reshape(3,3))