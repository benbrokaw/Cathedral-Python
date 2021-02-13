import math
import numpy as np
import matplotlib as mpl
from matplotlib import pyplot as plt
from numpy.lib.function_base import piecewise, select

import envs.game_pieces

WHITE = 1
BLACK = 2

def setup_game():
    w_pieces = game_pieces.white_pieces.copy()
    b_pieces = game_pieces.black_pieces.copy()
    
    game_board = np.zeros((10,10,3),dtype=np.int) # [pieces,player,owner]
    
    return w_pieces, b_pieces, game_board    

def place_piece(piece, board, top_left, player):
    tmp_board = board.copy()
    for row in range(piece.shape[0]):
        for col in range(piece.shape[1]):
            
            # check if on board (no need to check zeros)
            if top_left[0]+row >= board.shape[0] or top_left[1]+col >= board.shape[1]:
                print('the played piece is falling off the board!')
                return False, board
            
            # check if other player owns space
            if  tmp_board[2][top_left[0]+row][top_left[1]+col] != player or \
                tmp_board[2][top_left[0]+row][top_left[1]+col] != 0:
                print('the other player owns this space!')
                return False, board
            # place square & set player
            tmp_board[0][top_left[0]+row][top_left[1]+col] = piece[row][col]
            tmp_board[1][top_left[0]+row][top_left[1]+col] = player
            
            # check if the piece is valid
            if tmp_board[1][top_left[0]+row][top_left[1]+col] > 1:
                print('the played piece does not fit here!')
                return False, board
            
    return True, tmp_board

def white_turn(board, pieces):
    if np.all((board == 0)):
        return place_cathedral(board), pieces
    else:
        piece, p_index = select_piece(board, pieces)
        loc = select_location(piece, board)
        succ, new_board = place_piece(piece, board, loc, WHITE)
        if not succ:
            "invalid position please pick a valid location"
            white_turn(board,pieces)
        else:
            # remove the piece from the list
            return new_board, np.delete(pieces,p_index,0)

def black_turn(board, pieces):
    piece, p_index = select_piece(board, pieces)
    loc = select_location(piece, board)
    succ, new_board = place_piece(piece, board, loc, WHITE)
    if not succ:
        "invalid position please pick a valid location"
        black_turn(board,pieces)
    else:
        # remove the piece from the list
        return new_board, np.delete(pieces,p_index,0)
    
def place_cathedral(board):
    cathedral = game_pieces.cathedral
    loc = select_location(cathedral, board)
    succ, new_board = place_piece(cathedral, board, loc, WHITE)
    if not succ:
        "invalid position please pick a valid location"
        place_cathedral(board)
    else:
        return new_board
    
def select_piece(board, pieces):
    # TODO:: make allow piece selection
    piece = np.array
    piece_index = 0
    # piece_index is outter most index in piece list - the one to remove
    return piece, piece_index

# return top left corner of piece
def select_location(piece, board):
    # TODO:: allow for location selection
    location = (0,0)
    return location

def game_over(board, wp, bp):
    # TODO:: Check if no players can make a move
    return False

def score_game(wp,bp):
    wTotal, bTotal = 0,0
    for wpiece in wp:
        wTotal += np.sum(wpiece[1])
        
    for bpiece in bp:
        bTotal += np.sum(bpiece[1])
        
    winner = ''
        
    if wpiece < bpiece:
        winner = 'white'
        print('White Wins!')
    elif bpiece < wpiece:
        winner = 'black'
        print('Black Wins!')
    else:
        print('Tie Game!')
    print('Remaining Squares - White: %i Black: %i' % wpiece, bpiece)
    
    return wpiece, bpiece, winner
        
def main():
    w,b,board = setup_game()
    while not game_over(board,w,b):
        board, w = white_turn(board, w)
        
        if game_over(board,w,b): break
        
        board, b = black_turn(board, b)
        
    score_game(w,b)

if __name__ == "__main__":
    main()