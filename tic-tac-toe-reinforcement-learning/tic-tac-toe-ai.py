import numpy as np
import pickle

#setting rows and cols to 3
ROWS = 3
COLS = 3

#X - O Map, 1 for X, -1 for O
XO_map = {1:'X', -1: 'O', 0: '__'}

class gameState:

    def __init__(self, player1, player2) -> None:
        self.board = np.zeros((ROWS, COLS))
        self.p1 = player1
        self.p2 = player2
        self.gameOver = False
        self.boardHash = None
        #Assumes Player One Starts First, during init
        self.playerSymbol = 1

    #Function to get a board-hash state, to store the state value tuples as a dictionary for value updation
    def getHash(self):
        self.board_Hash = str(self.board.reshape((ROWS * COLS)))
        # print(self.board_Hash)
        return self.board_Hash

    #Function to return empty spaces on current GameState:
    def availablePos(self):
        availPos = []
        for i in range(ROWS):
            for j in range(COLS):
                if(self.board[i, j] == 0):
                    availPos.append((i, j))
        return availPos

    def getWinner(self):

        #Check for a winner
        #Checking ROWS
        for i in range(ROWS):
            SUM = sum(self.board[i, :])
            if SUM == 3:
                self.gameOver = True
                #print("Row is Winner Condition")
                return 1
            elif SUM == -3:
                self.gameOver = True
                #print("Row is Winner Condition")
                return -1
        
        #Checking COLS
        for i in range(COLS):
            SUM = sum(self.board[:, i])
            if SUM == 3:
                self.gameOver = True
                #print("col is Winner Condition")
                return 1
            elif SUM == -3:
                self.gameOver = True
                #print("col is Winner Condition")
                return -1
        
        #Checking Diagonals
        diagSUM1 = sum([self.board[i, i] for i in range(ROWS)])
        diagSUM2 = sum([self.board[i, COLS - i - 1] for i in range(ROWS)])

        if diagSUM1 == 3:
            self.gameOver = True
            #print("Diag is winner condition")
            return 1
        elif diagSUM1 == -3:
            self.gameOver = True
            #print("Diag is winner condition")
            return -1

        if diagSUM2 == 3:
            self.gameOver = True
            #print("Diag is winner condition")
            return 1
        elif diagSUM2 == -3:
            self.gameOver = True
            #print("Diag is winner condition")
            return -1

        #Check for a tie
        if(len(self.availablePos())== 0):
            self.gameOver = True
            return 0
        
        self.gameOver = False
        return None

    #function to play the move and change turn
    def updateState(self, move):
        self.board[move] = self.playerSymbol
        self.playerSymbol = 1 if self.playerSymbol == -1 else -1

    #back-propagate scores through all states when game is over
    def giveReward(self):
        result = self.getWinner()
        if result == 1:
            self.p1.feedReward(1)
            self.p2.feedReward(0)
        elif result == -1:
            self.p1.feedReward(0)
            self.p2.feedReward(1)
        else:
            self.p1.feedReward(0.1)
            self.p2.feedReward(0.5)
        
    #reset gameState when a game is over
    def gameReset(self):
        self.board = np.zeros((ROWS, COLS))
        self.boardHash = None
        self.gameOver = False
        self.playerSymbol = 1

    #two Ai players play each other and get trained simultaneously
    def play(self, rounds = 1000):
        for i in range(rounds):
            if i % 1000 == 0:
                print(f'Round => {i}')
            
            while not self.gameOver:
                #player-1
                positions = self.availablePos()
                p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
                
                #get move from AI player and play move
                self.updateState(p1_action)
                boardhash = self.getHash()
                self.p1.addState(boardhash)

                win = self.getWinner()

                if win is not None:
                    #self.printBoard()
                    self.giveReward()
                    self.p1.reset()
                    self.p2.reset()
                    self.gameReset()
                    break

                else:
                    positions = self.availablePos()
                    p2_action = self.p2.chooseAction(positions, self.board, self.playerSymbol)
                    
                    #get move from AI player and play move
                    self.updateState(p2_action)
                    boardhash = self.getHash()
                    self.p2.addState(boardhash)

                    win = self.getWinner()

                    if win is not None:
                        #self.printBoard()
                        self.giveReward()
                        self.p2.reset()
                        self.p1.reset()
                        self.gameReset()
                        break
    
    def playHuman(self):
        
        while not self.gameOver:
                #player-1
                positions = self.availablePos()
                p1_action = self.p1.chooseAction(positions, self.board, self.playerSymbol)
                
                #get move from AI player and play move
                self.updateState(p1_action)
                boardhash = self.getHash()
                self.p1.addState(boardhash)

                self.printBoard()
                print("--------------------------------------")
                win = self.getWinner()
                if win is not None:
                    if win == 1:
                        print(f'{self.p1.name} has Won')
                    elif win == 0:
                        print('Tie')
                    self.gameReset()
                    break
               
                else:
                    #Player 2 - Human makes move
                    positions = self.availablePos()
                    p2_action = self.p2.chooseAction(positions)

                    self.updateState(p2_action)
                    self.printBoard()

                    print("--------------------------------------")
                    win = self.getWinner()
                    if win is not None:
                        if win == -1:
                            print(f'{self.p2.name} has Won')
                        elif win == 0:
                            print('Tie')
                        self.gameReset()
                        break
                
    def printBoard(self):
        for row in range(ROWS):
            formattedRow = [XO_map[i] for i in self.board[row, :]]
            print(formattedRow)
    

class player:

    def __init__(self, name, expRate = 0.3):
        self.name = name
        self.states = [] # records all states
        self.learningRate = 0.3
        self.expRate = expRate
        self.decayGamma = 0.9
        self.states_value = {} #state-value mapping

    def getHash(self, gameBoard):
        boardHash = str(gameBoard.reshape(ROWS * COLS))
        return boardHash

    #chooses action, the move to take depending on exp rate, if exp rate is e => (1-e)*100 % times we take greedy choice, rest time random choice 
    def chooseAction(self, positions, board, symbol):
        
        if np.random.uniform(0, 1) <= self.expRate:
            #random Action, taken
            moveIdx = np.random.choice(len(positions))
            action = positions[moveIdx]
        else:
            maxValue = -999
            for p in positions:                
                nextBoard = board.copy()
                nextBoard[p] = symbol
                nextBoardHash = self.getHash(nextBoard)
                value = 0 if self.states_value.get(nextBoardHash) is None else self.states_value.get(nextBoardHash)
                if(value >= maxValue):
                    maxValue = value
                    action = p
            
        return action
    
    # append a hash state
    def addState(self, state):
        self.states.append(state)

    # at the end of game, backpropagate and update states value
    def feedReward(self, reward):
        for st in reversed(self.states):
            if self.states_value.get(st) is None:
                self.states_value[st] = 0
            self.states_value[st] += self.learningRate * (self.decayGamma * reward - self.states_value[st])
            reward = self.states_value[st]

    def reset(self):
        self.states = []

    #save state_values dict into a new file
    def savePolicy(self):
        fw = open('policy_' + str(self.name), 'wb')
        pickle.dump(self.states_value, fw)
        fw.close()

    #load a pre-existing state_value dict into a new AI player
    def loadPolicy(self, file):
        fr = open(file, 'rb')
        self.states_value = pickle.load(fr)
        fr.close()

#class to define humanplayer
class humanPlayer:

    def __init__(self, name):
        self.name = name
    
    def chooseAction(self, positions):
        while True:
            row = int(input("Enter Row: "))
            col = int(input("Enter Col: "))
            move = row, col
            if move in positions:
                return move
    
    def addState(self, state):
        pass

    def feedReward(self, reward):
        pass

    def reset(self):
        pass
    

if __name__ == "__main__":
    # training
    p1 = player("p1")
    p2 = player("p2")

    st = gameState(p1, p2)
    print("training...")
    st.play(10000)
    p1.savePolicy()

    print("Training Done, proceed to play. Beat Me if you can !!")
    
    p1 = player("Computer", expRate= 0)
    p1.loadPolicy("policy_p1")
    
    p2 = humanPlayer("Player")

    st = gameState(p1, p2)
    st.playHuman()

            