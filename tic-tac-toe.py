"""
Play TTT on terminal

Control Flow:
    Define Board
    Print Board
    Ask User Input => Position
    Check if a winning condition is satisfied
    
    player-1 is X and player-2 is O always
"""

position_map = {1 : (0, 0), 2 : (0, 1), 3 : (0, 2),
                4 : (1, 0), 5 : (1, 1), 6 : (1, 2), 
                7 : (2, 0), 8 : (2, 1), 9 : (2, 2)}


def gameReset():
    return [["_"]*3 for _ in range(3)], True, 0

def print_board(board):
    for row in board:
        for slot in row:
            print(f"{slot} ", end=" ")
        print(" ")
    
def checkValidPos(board, x, y):
    if(board[x][y] != '_'):
        print("Position already played")
        return False

    return True

def isValid(board, user_input):
    #Check if its a valid position
    if user_input.lower() == 'q':
        return True
    elif(int(user_input) >= 1 and int(user_input) <= 9):
        (i, j) = position_map[int(user_input)]
        return checkValidPos(board, i, j)
    
    return False

def isQuit(user_input):
    return user_input.lower() == 'q'

def moveCoin(playerOne):
    if(playerOne):
        return 'X'
    return 'O'

def playMove(board, position_map, moveCount, position, token):

    (i, j) = position_map[int(position)]
    board[i][j] = token
    ##print_board(board)
    moveCount += 1
    return

def checkPlayerWon(board, token):
    result = [token] * 3

    #Check Rows
    for row in board:
        if(row == result):
            return True
    
    #Check Columns
    for col in range(3):
        colTokens = []
        for row in range(3):
            if(board[row][col] == token):
                colTokens.append(board[row][col])
            else: break
        if(colTokens == result):
            return True 

    #Check Diagonal-1
    diag = []
    for i in range(3):
        if(board[i][i] == token):
            diag.append(board[i][i])
        else: break
    if(diag == result):
        return True
    
    #Check Diagonal-2
    diag = []
    for i in range(3):
        if(board[i][2-i] == token):
            diag.append(board[i][2-i])
        else: break
    
    if(diag == result):
        return True

    return False

def checkDraw(moveCount):
    return moveCount == 9

def playAgain():
    playAgain = input("Play Again ? y for yes, no otherwise: ")
    if(playAgain.lower() == 'y'):
        return True
    print("Thank you for playing!")
    return False


def playGame():
    
    board = [["_" for _ in range(3)] for _ in range(3)]
    moveCount = 0
    playerOne = True
    #Main Game Loop
    while True:
        
        print_board(board)
        if(playerOne):
            print("Player 1's Turn:")
        else:
            print("Player 2's Turn:")

        user_input = input("Enter position (1-9) you want play or q/Q to quit: ")
        #Validate User Input    
        if not isValid(board, user_input):
            print("Kindly Enter a Valid Input, for the game to proceed")
            continue

        #Check if quitting the game
        if(isQuit(user_input)):
            print("Thank you for playing!")
            break
        
        #Play the move
        token = moveCoin(playerOne)
        playMove(board, position_map, moveCount, user_input, token)
        
        #Check if game is finished
        if checkPlayerWon(board, token):
            print_board(board)
            print(f"{token} has Won the game")
            if(playAgain()):
                board, playerOne, moveCount = gameReset()
                continue
            else:
                break
        elif checkDraw(moveCount):
            print_board(board)
            print("The Game is a Draw")
            if(playAgain()):
                board, playerOne, moveCount = gameReset()
                continue
            else:
                break
        
        #Switch to opponent
        playerOne = not playerOne
    
    return

if __name__ == "__main__":
    playGame()


    
