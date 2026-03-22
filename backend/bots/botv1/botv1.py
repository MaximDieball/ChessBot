from bots.botLib.lib import *
import random

piece_values = {
    "E": 0,      # en passant
    "P": 100,
    "N": 320,
    "B": 330,
    "R": 500,
    "Q": 900,
    "K": 20000
}

def get_botv1_move(game, turn):
    possible_moves = []
    best_move = []
    best_eval = -100001

    # find all possible moves
    for i, piece in enumerate(game.board):
        if piece and piece.color == turn:
            found_moves = game.find_legal_moves(i, piece, turn)
            for move in found_moves:
                possible_moves.append([i, move])
    if len(possible_moves) <= 0:
        raise ValueError("possible moves cant be 0")

    # evaluate every move
    for i, move in enumerate(possible_moves):
        simulated_game = game.clone()
        simulated_game.update_board(move[0], move[1])
        evaluation = evaluate_position(simulated_game.board)
        if turn == "b":
            evaluation = -1*evaluation
        if evaluation > best_eval:
            best_move = move
            best_eval = evaluation

    return best_move


def evaluate_position(board):
    black_score = 1
    white_score = 1

    for i, piece in enumerate(board):
        score = 0
        if piece:

            score += piece_values[piece.type]

            if piece.color == "b":
                black_score += score
            else:
                white_score += score

    return white_score - black_score
