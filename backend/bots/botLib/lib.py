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
            if board[position - 16] == "" and 47 < position < 56:
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
            if board[position + 16] == "" and 7 < position < 16:
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
