from bots.botLib.lib import *
import random


def get_random_bot_move(game, turn):
    possible_moves = []
    for i, piece in enumerate(game.board):
        if piece and piece.color == turn:
            found_moves = game.find_legal_moves(i, piece, turn)
            for move in found_moves:
                possible_moves.append([i, move])
    if len(possible_moves) <= 0:
        raise ValueError("possible moves cant be 0")

    return random.choice(possible_moves)
