import numpy as np

#Defining variables
LENGTH = 3

class Agent:
    def __init__ (self,eps = 0.1, alpha = 0.5):
        self.eps = eps
        self.alpha = alpha
        self.verbose = False
        self.state_reward = []
        self.state_returns = []
        self.returns = {}
        self.gamma = 0.9
        
        
    def setV(self,V):
        self.V = V
    def set_symbol(self,sym):
        self.sym = sym
    def set_verbose(self,v):
        self.verbose = v

    def reset_state_reward_returns(self):
        self.state_reward = []
        self.state_returns = []
        
    def take_action(self,env):
        #usign epsilon greedy to select the next state
        r = np.random.rand()
        best_state = None
        if r<self.eps:
            #take random action
            if self.verbose:
                print("Taking a random action")
            possible_moves = []
            for i in range(LENGTH):
                for j in range(LENGTH):
                    if env.is_empty(i,j):
                        possible_moves.append((i,j))
            idx = np.random.choice(len(possible_moves))
            next_move = possible_moves[idx]
            
        else:
            #greedy strategy
            pos2value = {}
            next_move = None
            best_value = -1
            for i in range(LENGTH):
                for j in range(LENGTH):
                    if env.is_empty(i,j):
                        #placing a random marker
                        env.board[i,j] = self.sym
                        #getting next state
                        state = env.get_state()
                        #removing the marker
                        env.board[i,j] = 0
                        pos2value[(i,j)] = self.V[state]
                        
                        #checking best value S'
                        if self.V[state] > best_value:
                            best_value = self.V[state]
                            best_state = state
                            next_move = (i,j)
            # if verbose, draw the board w/ the values
            if self.verbose:
                print("Taking a greedy action")
                for i in range(LENGTH):
                    print("------------------")
                    for j in range(LENGTH):
                        if env.is_empty(i, j):
                            # print the value
                            print(" %.2f|" % pos2value[(i,j)], end="")
                        else:
                            print("  ", end="")
                            if env.board[i,j] == env.x:
                                print("x  |", end="")
                            elif env.board[i,j] == env.o:
                                print("o  |", end="")
                            else:
                                print("   |", end="")
                    print("")
                print("------------------")
        env.board[next_move[0],next_move[1]] = self.sym
    
    def update_state_rewards(self,s,r):
        self.state_reward.append((s,r))
    
    def calculate_state_returns(self):
        G = 0
        state_and_returns = []
        first = True
        for s,r in reversed(self.state_reward):
            if first:
                first = False
            else:
                self.state_returns.append((s,G))
            G = r + self.gamma *G
            
        self.state_returns.reverse()
        

    def update_value(self):
        '''
        First visit monte carlo update
        '''
        seen_states = set()
        for s,G in self.state_returns:
            if s not in seen_states:
                if s not in self.returns.keys():
                    self.returns[s] = []
                self.returns[s].append(G)
                self.V[s] = np.mean(self.returns[s])
                seen_states.add(s)
            
            
        self.reset_state_reward_returns()
    
                            
            
