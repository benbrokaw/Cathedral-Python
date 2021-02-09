import math
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt

import game_peices

def setup_game():
    w_peices = game_peices.white_peices.copy()
    b_peices = game_peices.black_peices.copy()
    game_board = np.zeros((10,10,3),dtype=np.int)
    
    return w_peices, b_peices, game_board    

def place_peice(peice, board, top_left, player):
    tmp_board = board.copy()
    for row in range(peice.shape()[0]):
        for col in range(peice.shape()[1]):
            # place square & set player
            tmp_board[0][top_left[0]+row][top_left[1]+col] = peice[row][col]
            tmp_board[0][top_left[0]+row][top_left[1]+col] = player
            if tmp_board[1][top_left[0]+row][top_left[1]+col] > 1:
                return False, board

def white_turn(board, w_peices):
    if np.all((board == 0)):
        return place_cathedral(board), w_peices
        
    else:
        return 
    
def place_cathedral():
    cathedral = game_peices.cathedral
    
    
        
def main():
    w,b,board = setup_game()
    
    

if __name__ == "__main__":
    main()