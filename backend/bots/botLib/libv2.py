from typing import Optional
import copy


class Piece:
    def __init__(self, type, color, pos, move_counter):
        self.type = type
        self.pos = pos
        self.move_counter = move_counter
        self.color = color


class Game:
    def __init__(self):
        # saving all pieces in lists for performance
        self.black_enpassant_piece = []
        self.black_pawns = []
        self.black_knights = []
        self.black_bishops = []
        self.black_rooks = []
        self.black_queens = []
        self.black_kings = []

        self.white_enpassant_piece = []
        self.white_pawns = []
        self.white_knights = []
        self.white_bishops = []
        self.white_rooks = []
        self.white_queens = []
        self.white_kings = []

        self.amount_of_black_pieces = 0
        self.amount_of_white_pieces = 0

        self.board: list[Optional[Piece]] = [None] * 64

        # (original_pos, piece, new_pos, piece_taken, true_move)
        # true_move = an actual move not a recursive function call to perform a castle or enpassant
        # revert move reverses moves until one true move is reverted and stops
        self.history = []

    def import_board_string(self, string_board):

        self.black_enpassant_piece.clear()
        self.black_pawns.clear()
        self.black_knights.clear()
        self.black_bishops.clear()
        self.black_rooks.clear()
        self.black_queens.clear()
        self.black_kings.clear()

        self.white_enpassant_piece.clear()
        self.white_pawns.clear()
        self.white_knights.clear()
        self.white_bishops.clear()
        self.white_rooks.clear()
        self.white_queens.clear()
        self.white_kings.clear()

        for i, string in enumerate(string_board):
            if len(string) > 3:
                type = string[2]
                color = string[0]
                new_piece = Piece(type=type, color=color, pos=i, move_counter=int(string[4:] or 0))

                self._place_piece(new_piece)

    def add_piece_to_list(self, piece):
        if piece.color == "w":
            self.amount_of_white_pieces += 1
        else:
            self.amount_of_black_pieces += 1
        match piece.type:
            case "E":
                if piece.color == "w":
                    self.white_enpassant_piece.append(piece)
                else:
                    self.black_enpassant_piece.append(piece)
            case "P":
                if piece.color == "w":
                    self.white_pawns.append(piece)
                else:
                    self.black_pawns.append(piece)
            case "N":
                if piece.color == "w":
                    self.white_knights.append(piece)
                else:
                    self.black_knights.append(piece)
            case "B":
                if piece.color == "w":
                    self.white_bishops.append(piece)
                else:
                    self.black_bishops.append(piece)
            case "R":
                if piece.color == "w":
                    self.white_rooks.append(piece)
                else:
                    self.black_rooks.append(piece)
            case "Q":
                if piece.color == "w":
                    self.white_queens.append(piece)
                else:
                    self.black_queens.append(piece)
            case "K":
                if piece.color == "w":
                    self.white_kings.append(piece)
                else:
                    self.black_kings.append(piece)

    def _place_piece(self, piece):
        self.board[piece.pos] = piece
        self.add_piece_to_list(piece)

    def _remove_piece(self, i: int):
        removed_piece = self.board[i]
        self.board[i] = None
        if removed_piece is None:
            return
        if removed_piece.color == "w":
            self.amount_of_white_pieces -= 1
        else:
            self.amount_of_black_pieces -= 1

        list_to_remove_from = []
        match removed_piece.type:
            case "E":
                if removed_piece.color == "w":
                    list_to_remove_from = self.white_enpassant_piece
                else:
                    list_to_remove_from = self.black_enpassant_piece
            case "P":
                if removed_piece.color == "w":
                    list_to_remove_from = self.white_pawns
                else:
                    list_to_remove_from = self.black_pawns
            case "N":
                if removed_piece.color == "w":
                    list_to_remove_from = self.white_knights
                else:
                    list_to_remove_from = self.black_knights
            case "B":
                if removed_piece.color == "w":
                    list_to_remove_from = self.white_bishops
                else:
                    list_to_remove_from = self.black_bishops
            case "R":
                if removed_piece.color == "w":
                    list_to_remove_from = self.white_rooks
                else:
                    list_to_remove_from = self.black_rooks
            case "Q":
                if removed_piece.color == "w":
                    list_to_remove_from = self.white_queens
                else:
                    list_to_remove_from = self.black_queens
            case "K":
                if removed_piece.color == "w":
                    list_to_remove_from = self.white_kings
                else:
                    list_to_remove_from = self.black_kings

        for piece in list_to_remove_from:
            if piece.pos == i:
                list_to_remove_from.remove(piece)
                break

    def find_legal_moves(self, position: int, piece: Piece, turn: str):
        # select all squares for now
        found_moves = []
        match (piece.color, piece.type):
            case ("w", "P"):
                # move up one square
                if not self.board[position - 8]:
                    found_moves.append(position - 8)
                # move two squares
                if position - 16 >= 0 and not self.board[position - 16] and not self.board[position - 8] and 47 < position < 56:
                    found_moves.append(position - 16)
                # take diagonal
                if position - 9 >= 0 and position % 8 != 0 and self.board[position - 9] and self.board[position - 9].color == "b":
                    found_moves.append(position - 9)
                if position - 7 >= 0 and position % 8 != 7 and self.board[position - 7] and self.board[position - 7].color == "b":
                    found_moves.append(position - 7)

            case ("b", "P"):
                # move up one square
                if not self.board[position + 8]:
                    found_moves.append(position + 8)
                # move two squares
                if position + 16 < 64 and not self.board[position + 16] and not self.board[position + 8] and 7 < position < 16:
                    found_moves.append(position + 16)
                # take diagonal
                if position + 9 < 64 and position % 8 != 7 and self.board[position + 9] and self.board[position + 9].color == "w":
                    found_moves.append(position + 9)

                if position % 8 != 0 and self.board[position + 7] and self.board[position + 7].color == "w":
                    found_moves.append(position + 7)

            case ("b", "B") | ("w", "B"):
                found_moves.extend(self._diagonal_ray(position, -7, self.board, turn))
                found_moves.extend(self._diagonal_ray(position, 7, self.board, turn))
                found_moves.extend(self._diagonal_ray(position, -9, self.board, turn))
                found_moves.extend(self._diagonal_ray(position, 9, self.board, turn))

            case ("b", "R") | ("w", "R"):
                found_moves.extend(self._straight_ray(position, 1, self.board, turn))
                found_moves.extend(self._straight_ray(position, -1, self.board, turn))
                found_moves.extend(self._straight_ray(position, 8, self.board, turn))
                found_moves.extend(self._straight_ray(position, -8, self.board, turn))
            case ("b", "Q") | ("w", "Q"):
                found_moves.extend(self._straight_ray(position, 1, self.board, turn))
                found_moves.extend(self._straight_ray(position, -1, self.board, turn))
                found_moves.extend(self._straight_ray(position, 8, self.board, turn))
                found_moves.extend(self._straight_ray(position, -8, self.board, turn))

                found_moves.extend(self._diagonal_ray(position, -7, self.board, turn))
                found_moves.extend(self._diagonal_ray(position, 7, self.board, turn))
                found_moves.extend(self._diagonal_ray(position, -9, self.board, turn))
                found_moves.extend(self._diagonal_ray(position, 9, self.board, turn))

            case ("b", "N") | ("w", "N"):
                found_moves.extend(self._find_knight_moves(position, self.board, turn))

            case ("w", "K"):
                # check castle
                if (piece.move_counter == 0 and self.check_for_piece(pos=63, color="w", type="R", move_counter=0)
                        and not self.board[62] and not self.board[61] and not self.check_attacks("w", position)):
                    found_moves.append(62)
                if (piece.move_counter == 0 and self.check_for_piece(pos=56, color="w", type="R", move_counter=0)
                        and not self.board[57] and not self.board[58] and not self.board[59]
                        and not self.check_attacks("w", position)):
                    found_moves.append(58)

                found_moves.extend(self._find_king_moves(position, turn))
            case ("b", "K"):
                # check castle
                if (piece.move_counter == 0 and self.check_for_piece(pos=7, color="b", type="R", move_counter=0)
                        and not self.board[6] and not self.board[5] and not self.check_attacks("b", position)):
                    found_moves.append(6)
                if (piece.move_counter == 0 and self.check_for_piece(pos=0, color="b", type="R", move_counter=0)
                        and not self.board[1] and not self.board[2] and not self.board[3]
                        and not self.check_attacks("b", position)):
                    found_moves.append(2)

                found_moves.extend(self._find_king_moves(position, turn))

        return found_moves

    def update_board(self, original_position, new_position, recursion=False):
        piece = self.board[original_position]
        piece_taken = self.board[new_position]
        self._remove_piece(new_position)
        self._remove_piece(original_position)

        # promote to queen
        promoted = False
        if piece.type == "P" and (new_position < 8 or new_position > 57):
            piece.type = "Q"
            promoted = True

        # save move to history
        if not recursion:
            self.history.append((original_position, piece, new_position, piece_taken, promoted, True))
        else:
            self.history.append((original_position, piece, new_position, piece_taken, promoted, False))

        # castle logic
        if piece.type == "K" and piece.move_counter == 0 and new_position == 62:
            self.update_board(63, 61, recursion=True)  # move rook
        if piece.type == "K" and piece.move_counter == 0 and new_position == 58:
            self.update_board(56, 59, recursion=True)  # move rook
        if piece.type == "K" and piece.move_counter == 0 and new_position == 2:
            self.update_board(0, 3, recursion=True)  # move rook
        if piece.type == "K" and piece.move_counter == 0 and new_position == 6:
            self.update_board(7, 5, recursion=True)  # move rook

        # en passant
        if piece_taken and piece_taken.type == "E" and piece_taken.color == "b" and piece.type == "P":
            self.history.append((None, None, None, self.board[new_position + 8], False, False))
            self._remove_piece(new_position + 8)
        if piece_taken and piece_taken.type == "E" and piece_taken.color == "w" and piece.type == "P":
            self.history.append((None, None, None, self.board[new_position - 8], False, False))
            self._remove_piece(new_position - 8)

        # remove enpassant pieces
        for enpassant_piece in self.white_enpassant_piece:
            self.history.append((None, None, None, enpassant_piece, False, False))
            self._remove_piece(enpassant_piece.pos)
        for enpassant_piece in self.black_enpassant_piece:
            self.history.append((None, None, None, enpassant_piece, False, False))
            self._remove_piece(enpassant_piece.pos)

        if piece.type == "P" and new_position - original_position == 16:
            enpassant_piece = Piece(color="b", type="E", pos=new_position - 8, move_counter=0)
            self._place_piece(enpassant_piece)
            self.history.append((None, enpassant_piece, enpassant_piece.pos, None, False, False))
        if piece.type == "P" and new_position - original_position == -16:
            enpassant_piece = Piece(color="w", type="E", pos=new_position + 8, move_counter=0)
            self._place_piece(enpassant_piece)
            self.history.append((None, enpassant_piece, enpassant_piece.pos, None, False, False))

        piece.move_counter += 1
        piece.pos = new_position
        self._place_piece(piece)

    def check_attacks(self, color, pos):
        # knight check
        knight_squares = self._find_knight_moves(pos, self.board, color)
        for square in knight_squares:
            piece = self.board[square]
            if piece and piece.type == "N" and piece.color != color:
                return True

        opponent_queens_rooks = []
        opponent_queens_bishops = []
        if color == "w":
            opponent_queens_rooks.extend(self.black_rooks)
            opponent_queens_rooks.extend(self.black_queens)
            opponent_queens_bishops.extend(self.black_queens)
            opponent_queens_bishops.extend(self.black_bishops)
        else:
            opponent_queens_rooks.extend(self.white_rooks)
            opponent_queens_rooks.extend(self.white_queens)
            opponent_queens_bishops.extend(self.white_queens)
            opponent_queens_bishops.extend(self.white_bishops)

        # rook and queen check
        straight_rays = []
        check_right = False
        check_left = False
        check_up = False
        check_down = False

        for piece in opponent_queens_rooks:
            if piece.pos % 8 == pos % 8:
                if piece.pos > pos:
                    check_down = True
                else:
                    check_up = True

            if abs(piece.pos - pos) < 8:
                if piece.pos > pos:
                    check_right = True
                else:
                    check_left = True

        if check_down:
            straight_rays.append(self._straight_ray(pos, 8, self.board, color))
        if check_up:
            straight_rays.append(self._straight_ray(pos, -8, self.board, color))
        if check_right:
            straight_rays.append(self._straight_ray(pos, 1, self.board, color))
        if check_left:
            straight_rays.append(self._straight_ray(pos, -1, self.board, color))

        for ray in straight_rays:
            if len(ray) > 0:
                target_square = ray[-1]
                piece = self.board[target_square]
                if piece and piece.color != color:
                    if piece.type == "R":
                        return True
                    elif piece.type == "Q":
                        return True

        # bishop and queen check
        diagonal_rays = []
        check_up_right = False
        check_down_left = False
        check_up_left = False
        check_down_right = False

        for piece in opponent_queens_bishops:
            piece_row, piece_col = divmod(piece.pos, 8)
            pos_row, pos_col = divmod(pos, 8)

            if piece_row - pos_row == piece_col - pos_col:
                if piece.pos > pos:
                    check_down_right = True
                else:
                    check_up_left = True

            if -1 * (piece_row - pos_row) == piece_col - pos_col:
                if piece.pos > pos:
                    check_down_left = True
                else:
                    check_up_right = True

        if check_up_right:
            diagonal_rays.append(self._diagonal_ray(pos, -7, self.board, color))  # up right
        if check_down_left:
            diagonal_rays.append(self._diagonal_ray(pos, 7, self.board, color))  # down left
        if check_up_left:
            diagonal_rays.append(self._diagonal_ray(pos, -9, self.board, color))  # up left
        if check_down_right:
            diagonal_rays.append(self._diagonal_ray(pos, 9, self.board, color))     # down right

        for ray in diagonal_rays:
            if len(ray) > 0:
                target_square = ray[-1]
                piece = self.board[target_square]
                if piece and piece.color != color:
                    if piece.type == "B":
                        return True
                    elif piece.type == "Q":
                        return True

        # pawn check
        if color == "b":
            if pos % 8 != 0 and (pos + 7) < 64:
                piece = self.board[pos + 7]
                if piece and piece.color == "w" and piece.type == "P":
                    return True

            if pos % 8 != 7 and (pos + 9) < 64:
                piece = self.board[pos + 9]
                if piece and piece.color == "w" and piece.type == "P":
                    return True

        elif color == "w":
            if pos % 8 != 7 and (pos - 7) >= 0:
                piece = self.board[pos - 7]
                if piece and piece.color == "b" and piece.type == "P":
                    return True

            if pos % 8 != 0 and (pos - 9) >= 0:
                piece = self.board[pos - 9]
                if piece and piece.color == "b" and piece.type == "P":
                    return True

        # king check
        king_moves = self._find_king_moves(pos, color)
        for square in king_moves:
            piece = self.board[square]
            if piece and piece.color != color and piece.type == "K":
                return True

        return False

    def _find_king_moves(self, position, turn):
        found_squares = []
        if position > 7:
            if not self.board[position - 8] or self.board[position - 8].color != turn:
                found_squares.append(position - 8)

            if position % 8 != 7:
                if not self.board[position + 1] or self.board[position + 1].color != turn:
                    found_squares.append(position + 1)
                if not self.board[position + 1 - 8] or self.board[position + 1 - 8].color != turn:
                    found_squares.append(position + 1 - 8)

            if position % 8 != 0:
                if not self.board[position - 1] or self.board[position - 1].color != turn:
                    found_squares.append(position - 1)
                if not self.board[position - 1 - 8] or self.board[position - 1 - 8].color != turn:
                    found_squares.append(position - 1 - 8)

        if position < 56:
            if not self.board[position + 8] or self.board[position + 8].color != turn:
                found_squares.append(position + 8)

            if position % 8 != 7:
                if not self.board[position + 1] or self.board[position + 1].color != turn:
                    found_squares.append(position + 1)
                if not self.board[position + 1 + 8] or self.board[position + 1 + 8].color != turn:
                    found_squares.append(position + 1 + 8)

            if position % 8 != 0:
                if not self.board[position - 1] or self.board[position - 1].color != turn:
                    found_squares.append(position - 1)
                if not self.board[position - 1 + 8] or self.board[position - 1 + 8].color != turn:
                    found_squares.append(position - 1 + 8)

        return found_squares

    def _diagonal_ray(self, start, delta, board, turn):
        square = start
        found_squares = []
        # check edge cases when bishop is on the edge of the board
        if (
                (delta > 0 and square > 55) or (delta < 0 and square < 8) or
                ((delta == -9 or delta == 7) and square % 8 == 0) or
                ((delta == 9 or delta == -7) and square % 8 == 7)
        ):
            return found_squares

        for steps in range(7):
            # next square
            square = square + delta

            # enemy piece
            if board[square] and board[square].color != turn and board[square].type != "E":
                found_squares.append(square)
                return found_squares

            # own piece
            if board[square] and board[square].type != "E":
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

    def _straight_ray(self, start, delta, board, turn):
        square = start
        found_squares = []
        # check if bishop is on the edge of the board
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

            # enemy piece
            if board[square] and board[square].color != turn and board[square].type != "E":
                found_squares.append(square)
                return found_squares

            # own piece
            if board[square] and board[square].type != "E":
                return found_squares

            # border
            if (square > 55 and delta == 8) or (square < 8 and delta == -8):
                found_squares.append(square)
                return found_squares

            if (square % 8 == 7 and delta == 1) or (square % 8 == 0 and delta == -1):
                found_squares.append(square)
                return found_squares

            # empty square
            found_squares.append(square)

        return found_squares

    def _find_knight_moves(self, position, board, turn):
        found_squares = []

        if position > 15:
            if position % 8 != 0:
                if not board[position - 16 - 1] or board[position - 16 - 1].color != turn:
                    found_squares.append(position - 16 - 1)

            if position % 8 != 7:
                if not board[position - 16 + 1] or board[position - 16 + 1].color != turn:
                    found_squares.append(position - 16 + 1)

        if position < 48:
            if position % 8 != 0:
                if not board[position + 16 - 1] or board[position + 16 - 1].color != turn:
                    found_squares.append(position + 16 - 1)

            if position % 8 != 7:
                if not board[position + 16 + 1] or board[position + 16 + 1].color != turn:
                    found_squares.append(position + 16 + 1)

        if position % 8 > 1:
            if position > 7:
                if not board[position - 8 - 2] or board[position - 8 - 2].color != turn:
                    found_squares.append(position - 8 - 2)

            if position < 56:
                if not board[position + 8 - 2] or board[position + 8 - 2].color != turn:
                    found_squares.append(position + 8 - 2)

        if position % 8 < 6:
            if position > 7:
                if not board[position - 8 + 2] or board[position - 8 + 2].color != turn:
                    found_squares.append(position - 8 + 2)

            if position < 56:
                if not board[position + 8 + 2] or board[position + 8 + 2].color != turn:
                    found_squares.append(position + 8 + 2)

        return found_squares

    def check_for_piece(self, pos, color, type, move_counter):
        piece = self.board[pos]
        if not piece:
            return False
        if piece.color != color or piece.type != type or piece.move_counter != move_counter:
            return False
        return True

    def get_white_pieces(self):
        pieces = []
        pieces.extend(self.white_pawns)
        pieces.extend(self.white_bishops)
        pieces.extend(self.white_knights)
        pieces.extend(self.white_rooks)
        pieces.extend(self.white_queens)
        pieces.extend(self.white_kings)
        return pieces

    def get_black_pieces(self):
        pieces = []
        pieces.extend(self.black_pawns)
        pieces.extend(self.black_bishops)
        pieces.extend(self.black_knights)
        pieces.extend(self.black_rooks)
        pieces.extend(self.black_queens)
        pieces.extend(self.black_kings)
        return pieces

    def revert_move(self):
        move = self.history.pop()
        original_position = move[0]
        piece = move[1]
        new_position = move[2]
        piece_taken = move[3]
        promoted = move[4]
        is_main_move = move[5]

        if piece is not None:
            self._remove_piece(new_position)
            if original_position is not None:
                piece.move_counter -= 1
                piece.pos = original_position
                if promoted:
                    piece.type = "P"
                self._place_piece(piece)

        if piece_taken:
            self._place_piece(piece_taken)

        if not is_main_move:
            self.revert_move()

    def clone(self):
        new_game = Game()

        for i, piece in enumerate(self.board):
            if piece is not None:
                new_piece = Piece(
                    type=piece.type,
                    color=piece.color,
                    pos=piece.pos,
                    move_counter=piece.move_counter
                )
                new_game._place_piece(new_piece)

        return new_game
