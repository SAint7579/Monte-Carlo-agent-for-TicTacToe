from MonteCarloAgent import *
from TicTacToe_Environment import *
import numpy as np

#This will let us play the game
class Human:
    def __init__(self):
        pass

    def set_symbol(self, sym):
        self.sym = sym

    def take_action(self, env):
        while True:
            # break if we make a legal move
            move = input("Enter coordinates i,j for your next move (i,j=0..2): ")
            i, j = move.split(',')
            i = int(i)
            j = int(j)
            if env.is_empty(i, j):
                env.board[i,j] = self.sym
            break

    def update(self, env):
        pass
    
    def update_state_history(self, s):
        pass
    
    def update_value(self):
        pass
    
    def calculate_state_returns(self):
        pass
    
    def update_state_rewards(self,s,r):
        pass
    


def play_game_montecarlo(p1,p2,grid,draw= False):
    # loops until the game is over
    current_player = None
    while not grid.game_over():
        #pdb.set_trace()
        if current_player == p1:
            current_player = p2
        else:
            current_player = p1
        
        if draw is not False:
            if draw == 1 and current_player == p1:
                grid.draw_board()
            if draw == 2 and current_player == p2:
                grid.draw_board()
                
        current_player.take_action(grid)
        r = grid.reward(current_player.sym)
        s = grid.get_state()

        #Updating the state-reward pair
        current_player.update_state_rewards(s,r)
        
    #to check who won
    if draw:
        grid.draw_board()
    
    #Calculating the return for the game
    p1.calculate_state_returns()
    p2.calculate_state_returns()
    
    #Updating the value function using monte carlo
    p1.update_value()
    p2.update_value()


#### Training via self-play ####
p1 = Agent()
p2 = Agent()

env = Environment()

#initializing V functions
state_winner_tripplet = get_state_hash_and_winner(env)

Vx = initV_x(env,state_winner_triples=state_winner_tripplet)
p1.setV(Vx)
Vo = initV_o(env,state_winner_triples=state_winner_tripplet)
p2.setV(Vo)

#setting symbol
p1.set_symbol(env.x)
p2.set_symbol(env.o)

for t in range(20000):
    if t % 2000 == 0:
        print(t," Games played")
    #we will create a new environment on every iteration
    play_game_montecarlo(p1,p2,Environment())

#### AI vs Human ####
human = Human()
human.set_symbol(env.o)
while True:
    p1.set_verbose(True)
    #only take greedy actions
    p1.eps = 0
    play_game_montecarlo(p1, human, Environment(), draw=2)

    answer = input("Play again? [Y/n]: ")
    if answer and answer.lower()[0] == 'n':
        break

    
