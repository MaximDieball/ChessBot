from bots.botLib.libv3wrapper import *
import yaml
from bots.botv5.value_tables import *
import math
from bots.botv5.build import bot_search

with open("bots/botv5/config.yml", "r") as file:
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

def start_botv5_move_search(game, turn):
    min_piece_count = min(game.amount_of_white_pieces, game.amount_of_black_pieces)
    if min_piece_count < 8:
        depth = config["bot_settings"]["end_game_depth"]
    elif min_piece_count < 13:
        depth = config["bot_settings"]["mid_game_depth"]
    else:
        depth = config["bot_settings"]["opening_depth"]

    # hand of calculation to cpp
    return bot_search.start_cpp_search(
        game, turn, depth,
        piece_values,
        end_game_value_tables,
        mid_game_value_tables,
        opening_value_tables
    )


# converted to cpp
"""
def _get_botv5_move(game, turn, depth, alpha=-math.inf, beta=math.inf):
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
            game.update_board(piece.pos, move)
            evaluation = evaluate_position(game, turn)
            game.revert_move()
            possible_moves.append([piece.pos, move, evaluation])

    # Sort moves
    possible_moves.sort(key=lambda x: x[2], reverse=True)

    # if the king could be taken the path is a checkmate
    if len(game.white_kings) == 0:
        if turn == "w":
            return [0, 0], -math.inf
        else:
            return [0, 0], math.inf

    if len(game.black_kings) == 0:
        if turn == "w":
            return [0, 0], math.inf
        else:
            return [0, 0], -math.inf

    # very weird situation. dont know what should happen here but having no moves seems bad
    if len(possible_moves) == 0:
        return [0, 0], -10000


    # Default to the best immediate move in case all deeper searches get pruned
    best_move = possible_moves[0]
    best_eval = -math.inf

    if depth <= 1:
        return possible_moves[0], possible_moves[0][2]

    for move in possible_moves:
        game.update_board(move[0], move[1])

        found_move, opponent_eval = _get_botv5_move(game, opponent_color, depth - 1, -beta, -alpha)
        found_eval = -opponent_eva

        game.revert_move()

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

    # king will be taken in the next moves
    if best_eval == -math.inf:
        king = game.white_kings[0] if turn == "w" else game.black_kings[0]
        # if the king will be taken in the next move but is currently not under attack
        if not game.check_attacks(turn, king.pos):
            # its stalemate
            return best_move, 0
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


"""
