from bots.botLib.lib import *
import yaml
import random

with open("bots/botv2/config.yml", "r") as file:
    # safe_load is recommended for security (prevents code execution)
    config = yaml.safe_load(file)


piece_values = {
    "E": config["piece_values"]["P"],      # en passant
    "P": config["piece_values"]["P"],
    "N": config["piece_values"]["N"],
    "B": config["piece_values"]["B"],
    "R": config["piece_values"]["R"],
    "Q": config["piece_values"]["Q"],
    "K": config["piece_values"]["K"]
}


def get_botv2_move(board, turn, depth=config["bot_settings"]["depth"]):
    possible_moves = []
    best_move = []
    best_eval = -100001
    opponent_color = "b" if turn == "w" else "w"

    # find all possible moves
    for i, piece in enumerate(board):
        if piece != "" and piece[0] == turn:
            found_moves = find_legal_moves(i, piece, board, turn)
            for move in found_moves:
                # eval position and sort possible moves by eval
                simulated_board = update_board(i, move, board)
                evaluation = evaluate_position(simulated_board)
                if turn == "b":
                    evaluation = -1 * evaluation
                inserted_new_move = False
                for j, p_move in enumerate(possible_moves):
                    if p_move[2] < evaluation:
                        possible_moves.insert(j, [i, move, evaluation])
                        inserted_new_move = True
                        break
                if not inserted_new_move or len(possible_moves) == 0:
                    possible_moves.append([i, move, evaluation])
    # no moves = bad
    if len(possible_moves) <= 0:
        if turn == "w":
            return [0, 0], -10000
        else:
            return [0, 0], 10000

    if depth <= 0:
        best_move = possible_moves[0]
        best_eval = possible_moves[0][2]
        return best_move, best_eval

    else:
        branches = 0
        for i, move in enumerate(possible_moves):
            simulated_board = update_board(move[0], move[1], board)
            found_move, found_eval = get_botv2_move(simulated_board, opponent_color, depth-1)
            found_eval = found_eval*-1
            if found_eval > best_eval:
                best_move = move
                best_eval = found_eval
            branches += 1
            if branches >= config["bot_settings"]["max_branches"]:
                break

    return best_move, best_eval


def evaluate_position(board):
    black_score = 1
    white_score = 1

    for i, piece in enumerate(board):
        score = 0
        if piece != "":
            piece_color = piece[0]
            opponent_color = "b" if piece_color == "w" else "w"
            score += piece_values[piece[2]]

            if piece_color == "b":
                black_score += score
            else:
                white_score += score

    return white_score - black_score
