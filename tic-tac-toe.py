"""
Play TTT on terminal

Control Flow:
    Define Board
    Print Board
    Ask User Input => Position
    Check if a winning condition is satisfied
    
    player-1 is X and player-2 is O always
"""

board = [["_" for _ in range(3)] for _ in range(3)]
position_map = {1 : (0, 0), 2 : (0, 1), 3 : (0, 2),
                4 : (1, 0), 5 : (1, 1), 6 : (1, 2), 
                7 : (2, 0), 8 : (2, 1), 9 : (2, 2)}
playerOne = True
moveCount = 0

def gameReset():
    global board
    global playerOne
    global moveCount 
    board = [["_" for _ in range(3)] for _ in range(3)]
    playerOne = True
    moveCount = 0
    return

def print_board(board):
    for row in board:
        for slot in row:
            print(f"{slot} ", end=" ")
        print(" ")
    


def isValid(user_input):
    #Check if its a valid position
    if user_input.lower() == 'q':
        return True
    elif(int(user_input) >= 1 and int(user_input) <= 9):
        (i, j) = position_map[int(user_input)]
        if board[i][j] != "_":
            print("Position already Played")
            return False
        return True
    return False

def isQuit(user_input):
    return user_input.lower() == 'q'

def moveCoin(playerOne):
    if(playerOne):
        return 'X'
    return 'O'

def playMove(position, token):
    
    global board
    global position_map
    global moveCount
    (i, j) = position_map[int(position)]
    board[i][j] = token
    ##print_board(board)
    moveCount += 1
    return

def checkPlayerWon(token):
    global board
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

def checkDraw():
    global moveCount
    return moveCount == 9

def playAgain():
    playAgain = input("Play Again ? y for yes, no otherwise: ")
    if(playAgain.lower() == 'y'):
        gameReset()
        return True
    print("Thank you for playing!")
    return False


def playGame():
    
    global board
    global playerOne
    #Main Game Loop
    while True:
        
        print_board(board)
        if(playerOne):
            print("Player 1's Turn:")
        else:
            print("Player 2's Turn:")

        user_input = input("Enter position (1-9) you want play or q/Q to quit: ")
        #Validate User Input    
        if not isValid(user_input):
            print("Kindly Enter a Valid Input, for the game to proceed")
            continue

        #Check if quitting the game
        if(isQuit(user_input)):
            print("Thank you for playing!")
            break
        
        #Play the move
        token = moveCoin(playerOne)
        playMove(user_input, token)
        
        #Check if game is finished
        if checkPlayerWon(token):
            print_board(board)
            print(f"{token} has Won the game")
            if(playAgain()):
                continue
            else:
                break
        elif checkDraw():
            print_board(board)
            print("The Game is a Draw")
            if(playAgain()):
                continue
            else:
                break
        
        #Switch to opponent
        playerOne = not playerOne
    
    return

if __name__ == "__main__":
    playGame()


    
