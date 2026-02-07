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

def get_botv1_move(board, turn):
    possible_moves = []
    best_move = []
    best_eval = -100001
    # find all possible moves
    for i, piece in enumerate(board):
        if piece != "" and piece[0] == turn:
            found_moves = find_legal_moves(i, piece, board, turn)
            for move in found_moves:
                possible_moves.append([i, move])
    if len(possible_moves) <= 0:
        raise ValueError("possible moves cant be 0")

    # evaluate every move
    for i, move in enumerate(possible_moves):
        simulated_board = update_board(move[0], move[1], board)
        evaluation = evaluate_position(simulated_board)
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
        if piece != "":
            piece_color = piece[0]
            opponent_color = "b" if piece_color == "w" else "w"
            score += piece_values[piece[2]]
            if piece[2] == "K":
                if check_mate(piece_color, board):  # mate :(
                    if piece_color == "w":
                        return -100000
                    else:
                        return 100000
            # check control
            found_moves = find_legal_moves(i, piece, board, piece_color)
            for move in found_moves:
                if len(board[move]) > 2:
                    # score += piece_values[board[move][2]] * 0.2   # attacking enemy
                    score += 10  # controller square
                else:
                    score += 10   # controller square

            if piece_color == "b":
                black_score += score
            else:
                white_score += score

    return white_score - black_score
