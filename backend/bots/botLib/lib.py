piece_values = {
    "E": 0,      # en passant
    "P": 100,
    "N": 320,
    "B": 330,
    "R": 500,
    "Q": 900,
    "K": 900
}

def find_legal_moves(position: int, piece_with_flag: str, board: [], turn: str):
    # select all squares for now
    found_moves = []
    piece_type = piece_with_flag[:3]
    match piece_type:
        case "w-P":
            # move up one square
            if board[position - 8] == "":
                found_moves.append(position - 8)
            # move two squares
            if board[position - 16] == "" and board[position - 8] == "" and 47 < position < 56:
                found_moves.append(position - 16)
            # take diagonal
            if position % 8 != 0 and board[position - 9] != "" and board[position - 9][0] == "b":
                found_moves.append(position - 9)
            if position % 8 != 7 and board[position - 7] != "" and board[position - 7][0] == "b":
                found_moves.append(position - 7)

        case "b-P":
            # move up one square
            if board[position + 8] == "":
                found_moves.append(position + 8)
            # move two squares
            if board[position + 16] == "" and board[position + 8] == "" and 7 < position < 16:
                found_moves.append(position + 16)
            # take diagonal
            if position % 8 != 7 and board[position + 9] != "" and board[position + 9][0] == "w":
                found_moves.append(position + 9)

            if position % 8 != 0 and board[position + 7] != "" and board[position + 7][0] == "w":
                found_moves.append(position + 7)
        case "b-B" | "w-B":
            found_moves.extend(diagonal_ray(position, -7, board, turn))
            found_moves.extend(diagonal_ray(position, 7, board, turn))
            found_moves.extend(diagonal_ray(position, -9, board, turn))
            found_moves.extend(diagonal_ray(position, 9, board, turn))

        case "b-R" | "w-R":
            found_moves.extend(straight_ray(position, 1, board, turn))
            found_moves.extend(straight_ray(position, -1, board, turn))
            found_moves.extend(straight_ray(position, 8, board, turn))
            found_moves.extend(straight_ray(position, -8, board, turn))
        case "b-Q" | "w-Q":
            found_moves.extend(straight_ray(position, 1, board, turn))
            found_moves.extend(straight_ray(position, -1, board, turn))
            found_moves.extend(straight_ray(position, 8, board, turn))
            found_moves.extend(straight_ray(position, -8, board, turn))

            found_moves.extend(diagonal_ray(position, -7, board, turn))
            found_moves.extend(diagonal_ray(position, 7, board, turn))
            found_moves.extend(diagonal_ray(position, -9, board, turn))
            found_moves.extend(diagonal_ray(position, 9, board, turn))

        case "b-N" | "w-N":
            found_moves.extend(find_knight_moves(position, board, turn))

        case "w-K":
            # check castle
            if piece_with_flag[4:5] == "0" and board[63] == "w-R-0" and board[62] == "" and board[61] == "":
                found_moves.append(62)
            if (piece_with_flag[4:5] == "0" and board[56] == "w-R-0" and board[57] == "" and board[58] == ""
                    and board[59] == ""):
                found_moves.append(58)

            found_moves.extend(find_king_moves(position, board, turn))
        case "b-K":
            # check castle
            if piece_with_flag[4:5] == "0" and board[7] == "b-R-0" and board[6] == "" and board[5] == "":
                found_moves.append(6)
            if (piece_with_flag[4:5] == "0" and board[0] == "b-R-0" and board[1] == "" and board[2] == ""
                    and board[3] == ""):
                found_moves.append(2)

            found_moves.extend(find_king_moves(position, board, turn))

    for i in range(len(found_moves) - 1, -1, -1):
        move = found_moves[i]
        simulated_board = update_board(position, move, board)
        if check_check(turn, simulated_board):
            found_moves.pop(i)

    return found_moves


def diagonal_ray(start, delta, input_board, turn):
    board = list(input_board)
    square = start
    found_squares = []
    # check edge cases when bishop is on the edge of the board
    if (delta > 0 and square > 55) or (delta < 0 and square < 8):
        return found_squares

    if (
            ((delta == -9 or delta == 7) and square % 8 == 0) or
            ((delta == 9 or delta == -7) and square % 8 == 7)
    ):
        return found_squares

    for steps in range(7):
        # next square
        square = square + delta
        # remove enpassant pieces
        if board[square] != "" and len(board[square]) > 2 and board[square][2] == "E":
            board[square] = ""

        # enemy piece
        if board[square] != "" and board[square][0] != turn:
            found_squares.append(square)
            return found_squares

        # own piece
        if board[square] != "":
            return found_squares

        # border
        if square > 55 or square < 8:
            found_squares.append(square)
            return found_squares

        if square % 8 == 7 or square % 8 == 0:
            found_squares.append(square)
            return found_squares

        # empty square
        found_squares.append(square)

    return found_squares


def straight_ray(start, delta, input_board, turn):
    board = list(input_board)
    square = start
    found_squares = []
    # check edge cases when bishop is on the edge of the board
    if (
            (delta == 8 and square > 55) or
            (delta == -8 and square < 8) or
            (delta == -1 and square % 8 == 0) or
            (delta == 1 and square % 8 == 7)
    ):
        return found_squares

    for steps in range(7):
        # next square
        square = square + delta
        # remove enpassant pieces
        if board[square] != "" and len(board[square]) > 2 and board[square][2] == "E":
            board[square] = ""

        # enemy piece
        if board[square] != "" and board[square][0] != turn:
            found_squares.append(square)
            return found_squares

        # own piece
        if board[square] != "":
            return found_squares

        # border
        if (square > 55 and delta == 8) or (square < 8 and delta == -8):
            found_squares.append(square)
            return found_squares

        if (
                (square % 8 == 7 and delta == 1) or
                (square % 8 == 0 and delta == -1)
        ):
            found_squares.append(square)
            return found_squares

        # empty square
        found_squares.append(square)

    return found_squares


def find_king_moves(position, board, turn):
    found_squares = []
    if position > 7:
        if board[position - 8] == "" or board[position - 8][0] != turn:
            found_squares.append(position - 8)

        if position % 8 != 7:
            if board[position + 1] == "" or board[position + 1][0] != turn:
                found_squares.append(position + 1)
            if board[position + 1 - 8] == "" or board[position + 1 - 8][0] != turn:
                found_squares.append(position + 1 - 8)

        if position % 8 != 0:
            if board[position - 1] == "" or board[position - 1][0] != turn:
                found_squares.append(position - 1)
            if board[position - 1 - 8] == "" or board[position - 1 - 8][0] != turn:
                found_squares.append(position - 1 - 8)

    if position < 56:
        if board[position + 8] == "" or board[position + 8][0] != turn:
            found_squares.append(position + 8)

        if position % 8 != 7:
            if board[position + 1] == "" or board[position + 1][0] != turn:
                found_squares.append(position + 1)
            if board[position + 1 + 8] == "" or board[position + 1 + 8][0] != turn:
                found_squares.append(position + 1 + 8)

        if position % 8 != 0:
            if board[position - 1] == "" or board[position - 1][0] != turn:
                found_squares.append(position - 1)
            if board[position - 1 + 8] == "" or board[position - 1 + 8][0] != turn:
                found_squares.append(position - 1 + 8)

    return found_squares


def find_knight_moves(position, board, turn):
    found_squares = []

    if position > 15:
        if position % 8 != 0:
            if board[position - 16 - 1] == "" or board[position - 16 - 1][0] != turn:
                found_squares.append(position - 16 - 1)

        if position % 8 != 7:
            if board[position - 16 + 1] == "" or board[position - 16 + 1][0] != turn:
                found_squares.append(position - 16 + 1)

    if position < 48:
        if position % 8 != 0:
            # Duplicate logic from original source
            found_squares.append(position + 16 - 1)
            if board[position + 16 - 1] == "" or board[position + 16 - 1][0] != turn:
                found_squares.append(position + 16 - 1)

        if position % 8 != 7:
            # Duplicate logic from original source
            found_squares.append(position + 16 + 1)
            if board[position + 16 + 1] == "" or board[position + 16 + 1][0] != turn:
                found_squares.append(position + 16 + 1)

    if position % 8 > 1:
        if position > 7:
            if board[position - 8 - 2] == "" or board[position - 8 - 2][0] != turn:
                found_squares.append(position - 8 - 2)

        if position < 56:
            if board[position + 8 - 2] == "" or board[position + 8 - 2][0] != turn:
                found_squares.append(position + 8 - 2)

    if position % 8 < 6:
        if position > 7:
            if board[position - 8 + 2] == "" or board[position - 8 + 2][0] != turn:
                found_squares.append(position - 8 + 2)

        if position < 56:
            if board[position + 8 + 2] == "" or board[position + 8 + 2][0] != turn:
                found_squares.append(position + 8 + 2)

    return found_squares


def update_board(original_position, new_position, board):
    new_board = list(board)
    piece = new_board[original_position]
    if len(piece) < 4:   # safety check / fixes weired desync bugs
        return new_board

    piece_type = piece[:3]
    piece_taken = new_board[new_position]
    new_board[original_position] = ""
    move_counter = int(piece[4:] or 0) + 1
    piece = f"{piece_type}-{move_counter}"

    # castle logic
    if piece_type == "w-K" and new_position == 62:
        new_board = update_board(63, 61, new_board)  # move rook
    if piece_type == "w-K" and new_position == 58:
        new_board = update_board(56, 59, new_board)  # move rook
    if piece_type == "b-K" and new_position == 2:
        new_board = update_board(0, 3, new_board)  # move rook
    if piece_type == "b-K" and new_position == 6:
        new_board = update_board(7, 5, new_board)  # move rook

    # en passant
    if piece_type == "b-P" and new_position - original_position == 16:
        new_board[new_position - 8] = "b-E-0"
    if piece_type == "w-P" and original_position - new_position == 16:
        new_board[new_position + 8] = "w-E-0"

    if piece_taken == "b-E-0" and piece_type[2] == "P":
        new_board[new_position + 8] = ""
    if piece_taken == "w-E-0" and piece_type[2] == "P":
        new_board[new_position - 8] = ""

    new_board[new_position] = piece
    return new_board


def check_attacks(color, board, pos):
    attacks = {
        "P": 0,
        "N": 0,
        "B": 0,
        "R": 0,
        "Q": 0,
        "K": 0
    }

    # knight check
    knight_squares = find_knight_moves(pos, board, color)
    for sq in knight_squares:
        piece = board[sq]
        if piece != "" and len(piece) > 2 and piece[2] == "N" and piece[0] != color:
            attacks["N"] += 1

    # rook and queen check
    straight_rays = [
        straight_ray(pos, 1, board, color),   # Right
        straight_ray(pos, -1, board, color),  # Left
        straight_ray(pos, 8, board, color),   # Up
        straight_ray(pos, -8, board, color)   # Down
    ]

    for ray in straight_rays:
        if len(ray) > 0:
            target_sq = ray[-1]
            piece = board[target_sq]
            if piece != "" and len(piece) > 2 and piece[0] != color:
                if piece[2] == "R":
                    attacks["R"] += 1
                elif piece[2] == "Q":
                    attacks["Q"] += 1

    # bishop and queen check
    diagonal_rays = [
        diagonal_ray(pos, -7, board, color),  # up right
        diagonal_ray(pos, 7, board, color),   # down left
        diagonal_ray(pos, -9, board, color),  # up left
        diagonal_ray(pos, 9, board, color)    # down right
    ]

    for ray in diagonal_rays:
        if len(ray) > 0:
            target_sq = ray[-1]
            piece = board[target_sq]
            if piece != "" and len(piece) > 2 and piece[0] != color:
                if piece[2] == "B":
                    attacks["B"] += 1
                elif piece[2] == "Q":
                    attacks["Q"] += 1

    # pawn check
    if color == "b":
        if pos % 8 != 0 and (pos + 7) < 64:
            piece = board[pos + 7]
            if piece != "" and len(piece) > 2 and piece.startswith("w-P"):
                attacks["P"] += 1

        if pos % 8 != 7 and (pos + 9) < 64:
            piece = board[pos + 9]
            if piece != "" and len(piece) > 2 and piece.startswith("w-P"):
                attacks["P"] += 1

    elif color == "w":
        if pos % 8 != 7 and (pos - 7) >= 0:
            piece = board[pos - 7]
            if piece != "" and len(piece) > 2 and piece.startswith("b-P"):
                attacks["P"] += 1

        if pos % 8 != 0 and (pos - 9) >= 0:
            piece = board[pos - 9]
            if piece != "" and len(piece) > 2 and piece.startswith("b-P"):
                attacks["P"] += 1

    # king check
    king_moves = find_king_moves(pos, board, color)
    for sq in king_moves:
        piece = board[sq]
        if piece != "" and len(piece) > 2 and piece[0] != color and piece[2] == "K":
            attacks["K"] += 1
            break

    return attacks
def check_check(color, board):
    king_pos = find_king_pos("w", board) if color == "w" else find_king_pos("b", board)
    checks = check_attacks(color, board, king_pos)
    return any(checks.values())


def is_opponent_queen_or_rook(position, color, board):
    piece = board[position]
    if piece != "" and (piece[2] == "R" or piece[2] == "Q") and piece[0] != color:
        return True

    return False


def is_opponent_queen_or_bishop(position, color, board):
    piece = board[position]
    if piece != "" and (piece[2] == "B" or piece[2] == "Q") and piece[0] != color:
        return True

    return False


def find_king_pos(color, board):
    for i, piece in enumerate(board):
        if piece != "" and piece[:3] == color + "-K":
            return i

    return 0


def check_mate(color, board):
    in_check = check_check(color, board)
    possible_moves = []

    if in_check:
        # find all legal moves
        for pos in range(64):
            if board[pos] != "" and board[pos][0] == color:
                legal_moves_found = find_legal_moves(pos, board[pos], board, color)
                for move in legal_moves_found:
                    possible_moves.append([pos, move])

        return len(possible_moves) == 0

    return False
