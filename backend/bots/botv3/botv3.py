from bots.botLib.libv2 import *
import yaml
from bots.botv3.value_tables import *
import math

with open("bots/botv3/config.yml", "r") as file:
    # safe_load is recommended for security (prevents code execution)
    config = yaml.safe_load(file)


piece_values = {
    "E": 0,      # en passant
    "P": config["piece_values"]["P"],
    "N": config["piece_values"]["N"],
    "B": config["piece_values"]["B"],
    "R": config["piece_values"]["R"],
    "Q": config["piece_values"]["Q"],
    "K": config["piece_values"]["K"]
}

def start_botv3_move_search(game, turn):
    min_piece_count = min(game.amount_of_white_pieces, game.amount_of_black_pieces)
    if min_piece_count < 6:
        return _get_botv3_move(game, turn, config["bot_settings"]["end_game_depth"])
    elif min_piece_count < 12:
        return _get_botv3_move(game, turn, config["bot_settings"]["mid_game_depth"])
    else:
        return _get_botv3_move(game, turn, config["bot_settings"]["opening_depth"])


def _get_botv3_move(game, turn, depth, alpha=-math.inf, beta=math.inf):
    possible_moves = []
    opponent_color = "b" if turn == "w" else "w"

    if turn == "w":
        moveable_pieces = game.get_white_pieces()
    else:
        moveable_pieces = game.get_black_pieces()

    # find all possible moves
    for piece in moveable_pieces:
        found_moves = game.find_legal_moves(piece.pos, piece, turn)
        for move in found_moves:
            # eval position
            simulated_game = game.clone()
            simulated_game.update_board(piece.pos, move)
            evaluation = evaluate_position(simulated_game, turn)
            possible_moves.append([piece.pos, move, evaluation])

    # Sort moves
    possible_moves.sort(key=lambda x: x[2], reverse=True)

    # no moves = draw or checkmate
    if len(possible_moves) == 0:
        if turn == "w":
            king = game.white_kings[0]
        else:
            king = game.black_kings[0]

        if game.check_attacks(turn, king):
            return [0, 0], -math.inf
        else:
            return [0, 0], 0

    # Default to the best immediate move in case all deeper searches get pruned
    best_move = possible_moves[0]
    best_eval = -math.inf

    if depth <= 1:
        return possible_moves[0], possible_moves[0][2]

    for move in possible_moves:
        simulated_game = game.clone()
        simulated_game.update_board(move[0], move[1])

        found_move, opponent_eval = _get_botv3_move(simulated_game, opponent_color, depth - 1, -beta, -alpha)
        found_eval = -opponent_eval

        # Update best move if we found a better evaluation
        if found_eval > best_eval:
            best_eval = found_eval
            best_move = move

        # update alpha
        alpha = max(alpha, found_eval)

        # Alpha-Beta Pruning: If our guaranteed minimum score is better than the
        # opponent's guaranteed maximum score (beta), they will avoid this path. Prune!
        if alpha >= beta:
            break

    return best_move, best_eval


def evaluate_position(game, turn):
    black_score = 0
    white_score = 0
    min_piece_count = min(game.amount_of_white_pieces, game.amount_of_black_pieces)
    if min_piece_count <= 9:
        active_value_table = end_game_value_tables
    elif min_piece_count <= 14:
        active_value_table = mid_game_value_tables
    else:
        active_value_table = opening_value_tables

    for piece in game.get_white_pieces():
        raw_piece_value = piece_values[piece.type]
        value_table_bonus = active_value_table[piece.type][63-piece.pos]
        white_score += raw_piece_value + value_table_bonus
    for piece in game.get_black_pieces():
        raw_piece_value = piece_values[piece.type]
        value_table_bonus = active_value_table[piece.type][piece.pos]
        black_score += raw_piece_value + value_table_bonus

    if turn == "w":
        return white_score - black_score
    else:
        return black_score - white_score



