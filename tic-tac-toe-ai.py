# Board defined as a 1-D array for simplified understanding and conditional functions
# 0,0 => 0 ; 0,1 => 1; 0,2 => 2
# 1,0 => 3 ; 1,1 => 4; 1,2 => 5 and so on..

AIPlayer = 'O'
HumanPlayer = 'X'

class minMaxMove:

    def __init__(self, idx = None, score = None) -> None:
         self.index = idx
         self.score = score

    def setIdx(self, idx):
        self.index = idx
        return
    
    def setScore(self, minMaxMoveObj):
        self.score = minMaxMoveObj.score
        return

class Player:
    def __init__(self, token = 'X', human = None):
        self.human = human
        self.token = token

    def playerCopy(self, player):
        self.human = player.human
        self.token = player.token

def generateBoard(dims = 3):
    return ["_"] * (dims**2)


def printBoard(board, dims = 3):
    for i in range(dims):
        row = []
        for j in range(dims):
            row.append(board[dims*i + j])
        print(row)

def checkWin(board, token):

    if ((board[0] == token and board[1] == token and board[2] == token) or  
    (board[3] == token and board[4] == token and board[5] == token) or  
    (board[6] == token and board[7] == token and board[8] == token) or  
    (board[0] == token and board[3] == token and board[6] == token) or  
    (board[1] == token and board[4] == token and board[7] == token) or  
    (board[2] == token and board[5] == token and board[8] == token) or  
    (board[0] == token and board[4] == token and board[8] == token) or  
    (board[2] == token and board[4] == token and board[6] == token)):
        return True

    return False

def availableSpots(board):
    available = []
    for (idx, value) in enumerate(board):
        if(value == '_'):
            available.append(idx)
    return available

def playMove(board, player, position):
    if(position == None):
        return
    board[position]  = player.token
    return
    
def oppTn(token):
    if token == 'X':
        return 'O'
    return 'X'

def opp(player):
    Opp = Player()
    Opp.human = not player.human
    Opp.token = oppTn(player.token)
    return Opp


def minMax(currState, player):

    if(checkWin(currState, AIPlayer)):
        return minMaxMove(None, +10)
    elif(checkWin(currState, HumanPlayer)):
        return minMaxMove(None, -10)

    availSpots = availableSpots(currState)
    if(len(availSpots) == 0):
        return minMaxMove(None, 0)

    allMoves = []
    for i in range(len(availSpots)):
        
        move = minMaxMove()
        
        move.setIdx(availSpots[i])
        currState[availSpots[i]] = player

        result = None
        if player == HumanPlayer:
            result = minMax(currState, AIPlayer)
            move.setScore(result)
        else:
            result = minMax(currState, HumanPlayer)
            move.setScore(result)
        
        currState[availSpots[i]] = "_"
        allMoves.append(move)

    bestMove = minMaxMove()

    #print(allMoves)
    
    if(player == AIPlayer):
        bestScore = -1e4
        for move in allMoves:
            if move.score > bestScore:
                bestScore = move.score
                bestMove = move
    else:
        bestScore = 1e4
        for move in allMoves:
            if move.score <= bestScore:
                bestScore = move.score
                bestMove = move

    #print(bestMove)
    return bestMove


def playGame():
    
    print("Player - 1 is X, Player - 2 is O.")
    
    playerOne = Player('X', True)
    playerTwo = Player('O', True)

    isPlayer1AI = input('Is Player - 1 AI ? Y/y if yes, else otherwise: ')
    if(isPlayer1AI.lower() == 'y'):
        playerOne.human = False

    isPlayer2AI = input('Is Player - 2 AI ? Y/y if yes, else otherwise: ')
    if(isPlayer2AI.lower() == 'y'):
        playerTwo.human = False
    
    turnOne = True
    board = generateBoard()
    
    while True:

        currPlayer = Player()
        oppPlayer = Player()
        printBoard(board)
        availSpots = availableSpots(board)

        if(len(availSpots) == 0):
            print("Game is a Draw")
            break

        if(turnOne):
            print("Player 1's Turn:")
            currPlayer.playerCopy(playerOne)
            oppPlayer.playerCopy(playerTwo)
        else:
            print("Player 2's Turn:")
            currPlayer.playerCopy(playerTwo)
            oppPlayer.playerCopy(playerOne)

        posToPlay = None
        if currPlayer.human == True:
            while True:
                userAvailSpots = [1 + spots for spots in availSpots]
                print(f'List of Available Spots to Play: {userAvailSpots}')
                try:
                    userInput = int(input("Enter Spot: ")) - 1
                    if(userInput in availSpots):
                        posToPlay = userInput
                        break
                    print("Invalid Position Argument, only input available integers. Try Again")
                    continue
                except:
                    print("Invalid Position Argument, only input available integers. Try Again")
                    continue

            playMove(board, currPlayer, posToPlay)
            if(checkWin(board, currPlayer.token)):
                printBoard(board)
                print(f'{currPlayer.token} has won')
                break
        else:
            
            global AIPlayer
            global HumanPlayer 
            AIPlayer = currPlayer.token
            HumanPlayer = oppPlayer.token

            minMaxres = minMax(board, AIPlayer)
            #print(f'idx: {minMaxres.index}')
            posToPlay = minMaxres.index
            playMove(board, currPlayer, posToPlay)
            if(checkWin(board, currPlayer.token)):
                printBoard(board)
                print(f'{currPlayer.token} has won')
                break
        
        print('-------------------------------------------------------------')
        turnOne = not turnOne

    return

if __name__ == "__main__":
    playGame()






            

        

    


    





    



    



