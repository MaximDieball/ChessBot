from bots.botLib.lib import *
import random


def get_random_bot_move(board, turn):
    possible_moves = []
    for i, piece in enumerate(board):
        if piece != "" and piece[0] == turn:
            found_moves = find_legal_moves(i, piece, board, turn)
            for move in found_moves:
                possible_moves.append([i, move])
    if len(possible_moves) <= 0:
        raise ValueError("possible moves cant be 0")
    return random.choice(possible_moves)
