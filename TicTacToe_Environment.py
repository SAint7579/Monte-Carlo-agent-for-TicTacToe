##Class for the environment
import numpy as np

#Defining variables
LENGTH = 3


class Environment:
    def __init__(self):
        self.board = np.zeros((LENGTH,LENGTH))
        self.x = -1.0
        self.o = 1.0
        self.winner = None
        self.ended = False
        self.num_states = 3 ** (LENGTH*LENGTH)
        
        
    def is_empty(self,i,j):
        '''
            Checks if a place is empty
        '''
        return self.board[i,j]==0
    
    
    def reward(self,sym):
        # no reward until the game is over
        if not self.game_over():
            return 0
        
        #if we get here, game is over
        #sym will be self.x or self.o
        
        return 1 if self.winner == sym else -1
    
    def get_state(self):
        #returns the current state
        #this is equivalent to a base 3 number since |S| = 3 ** 9
        #We will represent each state with an int value in the multiples of power of 3
        k =0
        h =0
        for i in range(LENGTH):
            for j in range(LENGTH):
                if self.board[i,j] == 0:
                    v = 0
                elif self.board[i,j] == self.x:
                    v = 1
                elif self.board[i,j] == self.o:
                    v = 2
                #updating the state value
                h += 3**k *v
                #for the next row iteration
                k += 1
        #returning the state number
        return h
    
    
    def game_over(self, force_recalculate= False):
        if not force_recalculate and self.ended:
            return self.ended
        
        #For rows
        for i in range(LENGTH):
            for player in (self.x, self.o):
                #Sum will be -3 for x and +3 for 0
                if self.board[i].sum() == player*LENGTH:
                    self.winner = player
                    self.ended = True
                    return True
        #For columns
        for j in range(LENGTH):
            for player in (self.x, self.o):
                #Sum will be -3 for x and +3 for 0
                if self.board[:,j].sum() == player*LENGTH:
                    self.winner = player
                    self.ended = True
                    return True
        
        #For diagonals
        for player in (self.x,self.o):
            #top-left -> bottom-right diagonal
            if self.board.trace() == player*LENGTH:
                self.winner = player
                self.ended = True
                return True
            
            #top-right -> bottom-left diagonal
            if np.fliplr(self.board).trace() == player*LENGTH:
                self.winner = player
                self.ended = True
                return True
        #For draws
        if np.all((self.board==0) == False):
            self.winner = None
            self.ended= True
            return True
        
        #not over
        self.winner = None
        return False
    
    def draw_board(self):
        for i in range(LENGTH):
            print("-------------")
            for j in range(LENGTH):
                print("  ", end="")
                if self.board[i,j] == self.x:
                    print("x ", end="")
                elif self.board[i,j] == self.o:
                    print("o ", end="")
                else:
                    print("  ", end="")
            print("")
        print("-------------")
            

#Init functions

#Triples (state,winner,ended) generator
def get_state_hash_and_winner(env,i=0,j=0):
    '''
    Here, we will enumerate all game states recursively to get tripples to initialize the V funtions
    '''
    results = []
    for v in (0,env.x, env.o):
        env.board[i,j] = v
        if j == 2:
            if i == 2:
                #means the borad is full
                state = env.get_state()
                ended = env.game_over(True)
                winner = env.winner
                results.append((state,winner,ended))
            else:
                results += get_state_hash_and_winner(env,i+1,0)
        else:
            results += get_state_hash_and_winner(env,i,j+1)
            
    return results  
                

#initializing the value function
def initV_x(env,state_winner_triples):
    V = np.zeros(env.num_states)
    for state,winner,ended in state_winner_triples:
        if ended:
            if winner == env.x:
                #V=1 if x won
                v = 1
            else:
                #V = 0 if x lost
                v = 0
        else:
            #if the game is still going
            v = 0.5
        V[state] = v
    return V

def initV_o(env,state_winner_triples):
    V = np.zeros(env.num_states)
    for state,winner,ended in state_winner_triples:
        if ended:
            if winner == env.o:
                #V=1 if x won
                v = 1
            else:
                #V = 0 if x lost
                v = 0
        else:
            #if the game is still going
            v = 0.5
        V[state] = v
    return V
                    
    

                
                
