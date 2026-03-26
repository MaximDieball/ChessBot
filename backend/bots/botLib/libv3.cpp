

// ------------------------------------------
// Python to C++ Conversion by Gemini
// ------------------------------------------


#include "libv3.h"
#include <algorithm> // Required for std::remove
#include <utility> // for std::move
#include <cmath> // Required for std::abs
#include <stdexcept>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h> // Essential for auto-converting std::vector and std::shared_ptr

// Piece Constructor Implementation
Piece::Piece(std::string type, std::string color, int pos, int move_counter)
    : type(std::move(type)),
      color(std::move(color)),
      pos(pos),
      move_counter(move_counter) {}

// Game Constructor Implementation
Game::Game()
    : amount_of_black_pieces(0),
      amount_of_white_pieces(0),
      board(64, nullptr) // Initialize board with 64 nullptrs
{
    // C++ std::vectors are empty by default, so we don't need to manually
    // instantiate the history or the individual piece lists like in Python.
    // They are ready to have pieces appended to them using .push_back().
}


void Game::add_piece_to_list(std::shared_ptr<Piece> piece) {
    if (piece->color == "w") {
        amount_of_white_pieces++;
    } else {
        amount_of_black_pieces++;
    }

    if (piece->type == "E") {
        if (piece->color == "w") white_enpassant_piece.push_back(piece);
        else black_enpassant_piece.push_back(piece);
    } else if (piece->type == "P") {
        if (piece->color == "w") white_pawns.push_back(piece);
        else black_pawns.push_back(piece);
    } else if (piece->type == "N") {
        if (piece->color == "w") white_knights.push_back(piece);
        else black_knights.push_back(piece);
    } else if (piece->type == "B") {
        if (piece->color == "w") white_bishops.push_back(piece);
        else black_bishops.push_back(piece);
    } else if (piece->type == "R") {
        if (piece->color == "w") white_rooks.push_back(piece);
        else black_rooks.push_back(piece);
    } else if (piece->type == "Q") {
        if (piece->color == "w") white_queens.push_back(piece);
        else black_queens.push_back(piece);
    } else if (piece->type == "K") {
        if (piece->color == "w") white_kings.push_back(piece);
        else black_kings.push_back(piece);
    }
}

void Game::_place_piece(std::shared_ptr<Piece> piece) {
    board[piece->pos] = piece;
    add_piece_to_list(piece);
}

void Game::_remove_piece(int i) {
    std::shared_ptr<Piece> removed_piece = board[i];
    board[i] = nullptr;

    if (!removed_piece) {
        return;
    }

    if (removed_piece->color == "w") {
        amount_of_white_pieces--;
    } else {
        amount_of_black_pieces--;
    }

    // Use a pointer to point to the vector we need to modify
    std::vector<std::shared_ptr<Piece>>* list_to_remove_from = nullptr;

    if (removed_piece->type == "E") {
        list_to_remove_from = (removed_piece->color == "w") ? &white_enpassant_piece : &black_enpassant_piece;
    } else if (removed_piece->type == "P") {
        list_to_remove_from = (removed_piece->color == "w") ? &white_pawns : &black_pawns;
    } else if (removed_piece->type == "N") {
        list_to_remove_from = (removed_piece->color == "w") ? &white_knights : &black_knights;
    } else if (removed_piece->type == "B") {
        list_to_remove_from = (removed_piece->color == "w") ? &white_bishops : &black_bishops;
    } else if (removed_piece->type == "R") {
        list_to_remove_from = (removed_piece->color == "w") ? &white_rooks : &black_rooks;
    } else if (removed_piece->type == "Q") {
        list_to_remove_from = (removed_piece->color == "w") ? &white_queens : &black_queens;
    } else if (removed_piece->type == "K") {
        list_to_remove_from = (removed_piece->color == "w") ? &white_kings : &black_kings;
    }

    // Safely remove the shared pointer matching the exact instance
    if (list_to_remove_from) {
        list_to_remove_from->erase(
            std::remove(list_to_remove_from->begin(), list_to_remove_from->end(), removed_piece),
            list_to_remove_from->end()
        );
    }
}

bool Game::check_for_piece(int pos, const std::string& color, const std::string& type, int move_counter) {
    std::shared_ptr<Piece> piece = board[pos];
    if (!piece) {
        return false;
    }
    if (piece->color != color || piece->type != type || piece->move_counter != move_counter) {
        return false;
    }
    return true;
}

std::vector<std::shared_ptr<Piece>> Game::get_white_pieces() {
    std::vector<std::shared_ptr<Piece>> pieces;
    // Pre-allocate memory to avoid multiple reallocations
    pieces.reserve(white_pawns.size() + white_bishops.size() + white_knights.size() +
                   white_rooks.size() + white_queens.size() + white_kings.size());

    pieces.insert(pieces.end(), white_pawns.begin(), white_pawns.end());
    pieces.insert(pieces.end(), white_bishops.begin(), white_bishops.end());
    pieces.insert(pieces.end(), white_knights.begin(), white_knights.end());
    pieces.insert(pieces.end(), white_rooks.begin(), white_rooks.end());
    pieces.insert(pieces.end(), white_queens.begin(), white_queens.end());
    pieces.insert(pieces.end(), white_kings.begin(), white_kings.end());
    return pieces;
}

std::vector<std::shared_ptr<Piece>> Game::get_black_pieces() {
    std::vector<std::shared_ptr<Piece>> pieces;
    pieces.reserve(black_pawns.size() + black_bishops.size() + black_knights.size() +
                   black_rooks.size() + black_queens.size() + black_kings.size());

    pieces.insert(pieces.end(), black_pawns.begin(), black_pawns.end());
    pieces.insert(pieces.end(), black_bishops.begin(), black_bishops.end());
    pieces.insert(pieces.end(), black_knights.begin(), black_knights.end());
    pieces.insert(pieces.end(), black_rooks.begin(), black_rooks.end());
    pieces.insert(pieces.end(), black_queens.begin(), black_queens.end());
    pieces.insert(pieces.end(), black_kings.begin(), black_kings.end());
    return pieces;
}


// ... existing implementations ...

std::vector<int> Game::_find_king_moves(int position, const std::string& turn) {
    std::vector<int> found_squares;

    if (position > 7) {
        if (!board[position - 8] || board[position - 8]->color != turn) {
            found_squares.push_back(position - 8);
        }

        if (position % 8 != 7) {
            if (!board[position + 1] || board[position + 1]->color != turn) {
                found_squares.push_back(position + 1);
            }
            if (!board[position + 1 - 8] || board[position + 1 - 8]->color != turn) {
                found_squares.push_back(position + 1 - 8);
            }
        }

        if (position % 8 != 0) {
            if (!board[position - 1] || board[position - 1]->color != turn) {
                found_squares.push_back(position - 1);
            }
            if (!board[position - 1 - 8] || board[position - 1 - 8]->color != turn) {
                found_squares.push_back(position - 1 - 8);
            }
        }
    }

    if (position < 56) {
        if (!board[position + 8] || board[position + 8]->color != turn) {
            found_squares.push_back(position + 8);
        }

        if (position % 8 != 7) {
            if (!board[position + 1] || board[position + 1]->color != turn) {
                found_squares.push_back(position + 1);
            }
            if (!board[position + 1 + 8] || board[position + 1 + 8]->color != turn) {
                found_squares.push_back(position + 1 + 8);
            }
        }

        if (position % 8 != 0) {
            if (!board[position - 1] || board[position - 1]->color != turn) {
                found_squares.push_back(position - 1);
            }
            if (!board[position - 1 + 8] || board[position - 1 + 8]->color != turn) {
                found_squares.push_back(position - 1 + 8);
            }
        }
    }

    return found_squares;
}

std::vector<int> Game::_diagonal_ray(int start, int delta, const std::vector<std::shared_ptr<Piece>>& b, const std::string& turn) {
    int square = start;
    std::vector<int> found_squares;

    // check edge cases when piece is on the edge of the board
    if ((delta > 0 && square > 55) || (delta < 0 && square < 8) ||
        ((delta == -9 || delta == 7) && square % 8 == 0) ||
        ((delta == 9 || delta == -7) && square % 8 == 7)) {
        return found_squares;
    }

    for (int steps = 0; steps < 7; ++steps) {
        // next square
        square = square + delta;

        // enemy piece
        if (b[square] && b[square]->color != turn && b[square]->type != "E") {
            found_squares.push_back(square);
            return found_squares;
        }

        // own piece
        if (b[square] && b[square]->type != "E") {
            return found_squares;
        }

        // border
        if (square > 55 || square < 8) {
            found_squares.push_back(square);
            return found_squares;
        }

        if (square % 8 == 7 || square % 8 == 0) {
            found_squares.push_back(square);
            return found_squares;
        }

        // empty square
        found_squares.push_back(square);
    }

    return found_squares;
}

std::vector<int> Game::_straight_ray(int start, int delta, const std::vector<std::shared_ptr<Piece>>& b, const std::string& turn) {
    int square = start;
    std::vector<int> found_squares;

    // check if piece is on the edge of the board
    if ((delta == 8 && square > 55) ||
        (delta == -8 && square < 8) ||
        (delta == -1 && square % 8 == 0) ||
        (delta == 1 && square % 8 == 7)) {
        return found_squares;
    }

    for (int steps = 0; steps < 7; ++steps) {
        // next square
        square = square + delta;

        // enemy piece
        if (b[square] && b[square]->color != turn && b[square]->type != "E") {
            found_squares.push_back(square);
            return found_squares;
        }

        // own piece
        if (b[square] && b[square]->type != "E") {
            return found_squares;
        }

        // border
        if ((square > 55 && delta == 8) || (square < 8 && delta == -8)) {
            found_squares.push_back(square);
            return found_squares;
        }

        if ((square % 8 == 7 && delta == 1) || (square % 8 == 0 && delta == -1)) {
            found_squares.push_back(square);
            return found_squares;
        }

        // empty square
        found_squares.push_back(square);
    }

    return found_squares;
}

std::vector<int> Game::_find_knight_moves(int position, const std::vector<std::shared_ptr<Piece>>& b, const std::string& turn) {
    std::vector<int> found_squares;

    if (position > 15) {
        if (position % 8 != 0) {
            if (!b[position - 16 - 1] || b[position - 16 - 1]->color != turn) {
                found_squares.push_back(position - 16 - 1);
            }
        }
        if (position % 8 != 7) {
            if (!b[position - 16 + 1] || b[position - 16 + 1]->color != turn) {
                found_squares.push_back(position - 16 + 1);
            }
        }
    }

    if (position < 48) {
        if (position % 8 != 0) {
            if (!b[position + 16 - 1] || b[position + 16 - 1]->color != turn) {
                found_squares.push_back(position + 16 - 1);
            }
        }
        if (position % 8 != 7) {
            if (!b[position + 16 + 1] || b[position + 16 + 1]->color != turn) {
                found_squares.push_back(position + 16 + 1);
            }
        }
    }

    if (position % 8 > 1) {
        if (position > 7) {
            if (!b[position - 8 - 2] || b[position - 8 - 2]->color != turn) {
                found_squares.push_back(position - 8 - 2);
            }
        }
        if (position < 56) {
            if (!b[position + 8 - 2] || b[position + 8 - 2]->color != turn) {
                found_squares.push_back(position + 8 - 2);
            }
        }
    }

    if (position % 8 < 6) {
        if (position > 7) {
            if (!b[position - 8 + 2] || b[position - 8 + 2]->color != turn) {
                found_squares.push_back(position - 8 + 2);
            }
        }
        if (position < 56) {
            if (!b[position + 8 + 2] || b[position + 8 + 2]->color != turn) {
                found_squares.push_back(position + 8 + 2);
            }
        }
    }

    return found_squares;
}

// ... existing implementations ...

bool Game::check_attacks(const std::string& color, int pos) {
    // 1. Knight check
    std::vector<int> knight_squares = _find_knight_moves(pos, board, color);
    for (int square : knight_squares) {
        std::shared_ptr<Piece> piece = board[square];
        if (piece && piece->type == "N" && piece->color != color) {
            return true;
        }
    }

    // Combine opponent piece lists dynamically
    std::vector<std::shared_ptr<Piece>> opponent_queens_rooks;
    std::vector<std::shared_ptr<Piece>> opponent_queens_bishops;

    if (color == "w") {
        opponent_queens_rooks.insert(opponent_queens_rooks.end(), black_rooks.begin(), black_rooks.end());
        opponent_queens_rooks.insert(opponent_queens_rooks.end(), black_queens.begin(), black_queens.end());
        opponent_queens_bishops.insert(opponent_queens_bishops.end(), black_queens.begin(), black_queens.end());
        opponent_queens_bishops.insert(opponent_queens_bishops.end(), black_bishops.begin(), black_bishops.end());
    } else {
        opponent_queens_rooks.insert(opponent_queens_rooks.end(), white_rooks.begin(), white_rooks.end());
        opponent_queens_rooks.insert(opponent_queens_rooks.end(), white_queens.begin(), white_queens.end());
        opponent_queens_bishops.insert(opponent_queens_bishops.end(), white_queens.begin(), white_queens.end());
        opponent_queens_bishops.insert(opponent_queens_bishops.end(), white_bishops.begin(), white_bishops.end());
    }

    // 2. Rook and Queen check
    std::vector<std::vector<int>> straight_rays;
    bool check_right = false;
    bool check_left = false;
    bool check_up = false;
    bool check_down = false;

    for (const auto& piece : opponent_queens_rooks) {
        if (piece->pos % 8 == pos % 8) {
            if (piece->pos > pos) {
                check_down = true;
            } else {
                check_up = true;
            }
        }

        if (std::abs(piece->pos - pos) < 8) {
            if (piece->pos > pos) {
                check_right = true;
            } else {
                check_left = true;
            }
        }
    }

    if (check_down) straight_rays.push_back(_straight_ray(pos, 8, board, color));
    if (check_up) straight_rays.push_back(_straight_ray(pos, -8, board, color));
    if (check_right) straight_rays.push_back(_straight_ray(pos, 1, board, color));
    if (check_left) straight_rays.push_back(_straight_ray(pos, -1, board, color));

    for (const auto& ray : straight_rays) {
        if (!ray.empty()) {
            int target_square = ray.back();
            std::shared_ptr<Piece> piece = board[target_square];
            if (piece && piece->color != color) {
                if (piece->type == "R" || piece->type == "Q") {
                    return true;
                }
            }
        }
    }

    // 3. Bishop and Queen check
    std::vector<std::vector<int>> diagonal_rays;
    bool check_up_right = false;
    bool check_down_left = false;
    bool check_up_left = false;
    bool check_down_right = false;

    for (const auto& piece : opponent_queens_bishops) {
        int piece_row = piece->pos / 8;
        int piece_col = piece->pos % 8;
        int pos_row = pos / 8;
        int pos_col = pos % 8;

        if (piece_row - pos_row == piece_col - pos_col) {
            if (piece->pos > pos) check_down_right = true;
            else check_up_left = true;
        }

        if (-1 * (piece_row - pos_row) == piece_col - pos_col) {
            if (piece->pos > pos) check_down_left = true;
            else check_up_right = true;
        }
    }

    if (check_up_right) diagonal_rays.push_back(_diagonal_ray(pos, -7, board, color)); // up right
    if (check_down_left) diagonal_rays.push_back(_diagonal_ray(pos, 7, board, color)); // down left
    if (check_up_left) diagonal_rays.push_back(_diagonal_ray(pos, -9, board, color));  // up left
    if (check_down_right) diagonal_rays.push_back(_diagonal_ray(pos, 9, board, color));   // down right

    for (const auto& ray : diagonal_rays) {
        if (!ray.empty()) {
            int target_square = ray.back();
            std::shared_ptr<Piece> piece = board[target_square];
            if (piece && piece->color != color) {
                if (piece->type == "B" || piece->type == "Q") {
                    return true;
                }
            }
        }
    }

    // 4. Pawn check
    if (color == "b") {
        if (pos % 8 != 0 && (pos + 7) < 64) {
            std::shared_ptr<Piece> piece = board[pos + 7];
            if (piece && piece->color == "w" && piece->type == "P") return true;
        }
        if (pos % 8 != 7 && (pos + 9) < 64) {
            std::shared_ptr<Piece> piece = board[pos + 9];
            if (piece && piece->color == "w" && piece->type == "P") return true;
        }
    } else if (color == "w") {
        if (pos % 8 != 7 && (pos - 7) >= 0) {
            std::shared_ptr<Piece> piece = board[pos - 7];
            if (piece && piece->color == "b" && piece->type == "P") return true;
        }
        if (pos % 8 != 0 && (pos - 9) >= 0) {
            std::shared_ptr<Piece> piece = board[pos - 9];
            if (piece && piece->color == "b" && piece->type == "P") return true;
        }
    }

    // 5. King check
    std::vector<int> king_moves = _find_king_moves(pos, color);
    for (int square : king_moves) {
        std::shared_ptr<Piece> piece = board[square];
        if (piece && piece->color != color && piece->type == "K") {
            return true;
        }
    }

    return false;
}

// ... existing implementations ...

std::vector<int> Game::find_legal_moves(int position, std::shared_ptr<Piece> piece, const std::string& turn) {
    std::vector<int> found_moves;

    // Helper lambda to mimic Python's list.extend()
    auto extend_moves = [&](const std::vector<int>& new_moves) {
        found_moves.insert(found_moves.end(), new_moves.begin(), new_moves.end());
    };

    if (piece->color == "w" && piece->type == "P") {
        // move up one square
        if (position - 8 >= 0 && !board[position - 8]) {
            found_moves.push_back(position - 8);
        }
        // move two squares
        if (position - 16 >= 0 && !board[position - 16] && !board[position - 8] && position > 47 && position < 56) {
            found_moves.push_back(position - 16);
        }
        // take diagonal
        if (position - 9 >= 0 && position % 8 != 0 && board[position - 9] && board[position - 9]->color == "b") {
            found_moves.push_back(position - 9);
        }
        if (position - 7 >= 0 && position % 8 != 7 && board[position - 7] && board[position - 7]->color == "b") {
            found_moves.push_back(position - 7);
        }

    } else if (piece->color == "b" && piece->type == "P") {
        // move up one square
        if (position + 8 < 64 && !board[position + 8]) {
            found_moves.push_back(position + 8);
        }
        // move two squares
        if (position + 16 < 64 && !board[position + 16] && !board[position + 8] && position > 7 && position < 16) {
            found_moves.push_back(position + 16);
        }
        // take diagonal
        if (position + 9 < 64 && position % 8 != 7 && board[position + 9] && board[position + 9]->color == "w") {
            found_moves.push_back(position + 9);
        }
        if (position % 8 != 0 && board[position + 7] && board[position + 7]->color == "w") {
            found_moves.push_back(position + 7);
        }

    } else if (piece->type == "B") { // Covers both "w" and "b"
        extend_moves(_diagonal_ray(position, -7, board, turn));
        extend_moves(_diagonal_ray(position, 7, board, turn));
        extend_moves(_diagonal_ray(position, -9, board, turn));
        extend_moves(_diagonal_ray(position, 9, board, turn));

    } else if (piece->type == "R") { // Covers both "w" and "b"
        extend_moves(_straight_ray(position, 1, board, turn));
        extend_moves(_straight_ray(position, -1, board, turn));
        extend_moves(_straight_ray(position, 8, board, turn));
        extend_moves(_straight_ray(position, -8, board, turn));

    } else if (piece->type == "Q") { // Covers both "w" and "b"
        extend_moves(_straight_ray(position, 1, board, turn));
        extend_moves(_straight_ray(position, -1, board, turn));
        extend_moves(_straight_ray(position, 8, board, turn));
        extend_moves(_straight_ray(position, -8, board, turn));

        extend_moves(_diagonal_ray(position, -7, board, turn));
        extend_moves(_diagonal_ray(position, 7, board, turn));
        extend_moves(_diagonal_ray(position, -9, board, turn));
        extend_moves(_diagonal_ray(position, 9, board, turn));

    } else if (piece->type == "N") { // Covers both "w" and "b"
        extend_moves(_find_knight_moves(position, board, turn));

    } else if (piece->color == "w" && piece->type == "K") {
        // check castle
        if (piece->move_counter == 0 && check_for_piece(63, "w", "R", 0)
            && !board[62] && !board[61] && !check_attacks("w", position)) {
            found_moves.push_back(62);
        }
        if (piece->move_counter == 0 && check_for_piece(56, "w", "R", 0)
            && !board[57] && !board[58] && !board[59] && !check_attacks("w", position)) {
            found_moves.push_back(58);
        }

        extend_moves(_find_king_moves(position, turn));

    } else if (piece->color == "b" && piece->type == "K") {
        // check castle
        if (piece->move_counter == 0 && check_for_piece(7, "b", "R", 0)
            && !board[6] && !board[5] && !check_attacks("b", position)) {
            found_moves.push_back(6);
        }
        if (piece->move_counter == 0 && check_for_piece(0, "b", "R", 0)
            && !board[1] && !board[2] && !board[3] && !check_attacks("b", position)) {
            found_moves.push_back(2);
        }

        extend_moves(_find_king_moves(position, turn));
    }

    return found_moves;
}


// ... existing implementations ...

void Game::update_board(int original_position, int new_position, bool recursion) {
    std::shared_ptr<Piece> piece = board[original_position];
    std::shared_ptr<Piece> piece_taken = board[new_position];

    _remove_piece(new_position);
    _remove_piece(original_position);

    // Promote to queen
    bool promoted = false;
    if (piece->type == "P" && (new_position < 8 || new_position > 55)) {
        piece->type = "Q";
        promoted = true;
    }

    // Save move to history (!recursion matches the True/False logic of true_move)
    history.push_back({original_position, piece, new_position, piece_taken, promoted, !recursion});

    // Castle logic
    if (piece->type == "K" && piece->move_counter == 0 && new_position == 62) {
        update_board(63, 61, true);  // move rook
    }
    if (piece->type == "K" && piece->move_counter == 0 && new_position == 58) {
        update_board(56, 59, true);  // move rook
    }
    if (piece->type == "K" && piece->move_counter == 0 && new_position == 2) {
        update_board(0, 3, true);  // move rook
    }
    if (piece->type == "K" && piece->move_counter == 0 && new_position == 6) {
        update_board(7, 5, true);  // move rook
    }

    // En passant capture cleanup
    if (piece_taken && piece_taken->type == "E" && piece_taken->color == "b" && piece->type == "P") {
        history.push_back({std::nullopt, nullptr, std::nullopt, board[new_position + 8], false, false});
        _remove_piece(new_position + 8);
    }
    if (piece_taken && piece_taken->type == "E" && piece_taken->color == "w" && piece->type == "P") {
        history.push_back({std::nullopt, nullptr, std::nullopt, board[new_position - 8], false, false});
        _remove_piece(new_position - 8);
    }

    // Remove enpassant pieces (using copies to prevent iterator invalidation)
    std::vector<std::shared_ptr<Piece>> white_ep_copy = white_enpassant_piece;
    for (const auto& enpassant_piece : white_ep_copy) {
        history.push_back({std::nullopt, nullptr, std::nullopt, enpassant_piece, false, false});
        _remove_piece(enpassant_piece->pos);
    }

    std::vector<std::shared_ptr<Piece>> black_ep_copy = black_enpassant_piece;
    for (const auto& enpassant_piece : black_ep_copy) {
        history.push_back({std::nullopt, nullptr, std::nullopt, enpassant_piece, false, false});
        _remove_piece(enpassant_piece->pos);
    }

    // Creating new enpassant targets
    if (piece->type == "P" && new_position - original_position == 16) {
        std::shared_ptr<Piece> enpassant_piece = std::make_shared<Piece>("E", "b", new_position - 8, 0);
        _place_piece(enpassant_piece);
        history.push_back({std::nullopt, enpassant_piece, enpassant_piece->pos, nullptr, false, false});
    }
    if (piece->type == "P" && new_position - original_position == -16) {
        std::shared_ptr<Piece> enpassant_piece = std::make_shared<Piece>("E", "w", new_position + 8, 0);
        _place_piece(enpassant_piece);
        history.push_back({std::nullopt, enpassant_piece, enpassant_piece->pos, nullptr, false, false});
    }

    piece->move_counter += 1;
    piece->pos = new_position;
    _place_piece(piece);
}

void Game::revert_move() {
    if (history.empty()) {
        return;
    }

    // Pop the last move from history
    MoveRecord move = history.back();
    history.pop_back();

    std::optional<int> original_position = move.original_pos;
    std::optional<int> new_position = move.new_pos;
    std::shared_ptr<Piece> piece = move.piece;
    std::shared_ptr<Piece> piece_taken = move.piece_taken;
    bool promoted = move.promoted;
    bool is_main_move = move.true_move;

    if (piece) {
        // We must check if new_position actually holds a value before using it!
        if (new_position.has_value()) {
            _remove_piece(new_position.value());
        }

        // Check if original_position has a value instead of checking != -1
        if (original_position.has_value()) {
            piece->move_counter -= 1;
            piece->pos = original_position.value();
            if (promoted) {
                piece->type = "P";
            }
            _place_piece(piece);
        }
    }

    if (piece_taken) {
        _place_piece(piece_taken);
    }

    // Recursively revert if it wasn't a true move (e.g., reverting the rook part of a castle)
    if (!is_main_move) {
        revert_move();
    }
}

void Game::import_board_string(const std::vector<std::string>& string_board) {
    // Clear all piece lists
    black_enpassant_piece.clear();
    black_pawns.clear();
    black_knights.clear();
    black_bishops.clear();
    black_rooks.clear();
    black_queens.clear();
    black_kings.clear();

    white_enpassant_piece.clear();
    white_pawns.clear();
    white_knights.clear();
    white_bishops.clear();
    white_rooks.clear();
    white_queens.clear();
    white_kings.clear();

    // Reset board and counters
    std::fill(board.begin(), board.end(), nullptr);
    amount_of_black_pieces = 0;
    amount_of_white_pieces = 0;
    history.clear(); // Good practice to wipe history on fresh import

    for (size_t i = 0; i < string_board.size(); ++i) {
        const std::string& str = string_board[i];
        if (str.length() > 3) {
            std::string color = str.substr(0, 1);
            std::string type = str.substr(2, 1);
            int move_counter = 0;

            if (str.length() > 4) {
                try {
                    move_counter = std::stoi(str.substr(4));
                } catch (const std::invalid_argument&) {
                    move_counter = 0;
                }
            }

            std::shared_ptr<Piece> new_piece = std::make_shared<Piece>(type, color, i, move_counter);
            _place_piece(new_piece);
        }
    }
}

std::shared_ptr<Game> Game::clone() {
    std::shared_ptr<Game> new_game = std::make_shared<Game>();

    for (const auto& piece : board) {
        if (piece) {
            // Create a brand new piece allocation so memory isn't shared
            std::shared_ptr<Piece> new_piece = std::make_shared<Piece>(
                piece->type,
                piece->color,
                piece->pos,
                piece->move_counter
            );
            new_game->_place_piece(new_piece);
        }
    }

    return new_game;
}

namespace py = pybind11;

PYBIND11_MODULE(libv3, m) {
    m.doc() = "C++ Chess Core optimized with pybind11";

    py::class_<Piece, std::shared_ptr<Piece>>(m, "Piece")
        .def(py::init<std::string, std::string, int, int>(),
             py::arg("type"), py::arg("color"), py::arg("pos"), py::arg("move_counter"))
        .def_readwrite("type", &Piece::type)
        .def_readwrite("color", &Piece::color)
        .def_readwrite("pos", &Piece::pos)
        .def_readwrite("move_counter", &Piece::move_counter);

    py::class_<Game, std::shared_ptr<Game>>(m, "Game")
        .def(py::init<>())
        // Variables
        .def_readwrite("amount_of_white_pieces", &Game::amount_of_white_pieces)
        .def_readwrite("amount_of_black_pieces", &Game::amount_of_black_pieces)

        .def_readwrite("white_kings", &Game::white_kings)
        .def_readwrite("black_kings", &Game::black_kings)
        .def_readwrite("board", &Game::board)

        // Methods
        .def("import_board_string", &Game::import_board_string, py::arg("string_board"))
        .def("get_white_pieces", &Game::get_white_pieces)
        .def("get_black_pieces", &Game::get_black_pieces)
        .def("find_legal_moves", &Game::find_legal_moves, py::arg("position"), py::arg("piece"), py::arg("turn"))
        .def("update_board", &Game::update_board,
             py::arg("original_position"), py::arg("new_position"), py::arg("recursion") = false)
        .def("revert_move", &Game::revert_move)
        .def("check_attacks", &Game::check_attacks, py::arg("color"), py::arg("pos"))
        .def("clone", &Game::clone);
}