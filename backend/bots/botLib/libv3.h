
// ------------------------------------------
// Python to C++ Conversion by Gemini
// ------------------------------------------

#pragma once

#include <string>
#include <vector>
#include <memory>
#include <optional>

// Forward declarations if necessary
class Piece;

struct MoveRecord {
   std::optional<int> original_pos;
    std::shared_ptr<Piece> piece;
    std::optional<int> new_pos;
    std::shared_ptr<Piece> piece_taken;
    bool promoted;
    bool true_move;
};

class Piece {
public:
    std::string type;
    std::string color;
    int pos;
    int move_counter;

    Piece(std::string type, std::string color, int pos, int move_counter);
};

class Game {
public:
    // Black piece lists
    std::vector<std::shared_ptr<Piece>> black_enpassant_piece;
    std::vector<std::shared_ptr<Piece>> black_pawns;
    std::vector<std::shared_ptr<Piece>> black_knights;
    std::vector<std::shared_ptr<Piece>> black_bishops;
    std::vector<std::shared_ptr<Piece>> black_rooks;
    std::vector<std::shared_ptr<Piece>> black_queens;
    std::vector<std::shared_ptr<Piece>> black_kings;

    // White piece lists
    std::vector<std::shared_ptr<Piece>> white_enpassant_piece;
    std::vector<std::shared_ptr<Piece>> white_pawns;
    std::vector<std::shared_ptr<Piece>> white_knights;
    std::vector<std::shared_ptr<Piece>> white_bishops;
    std::vector<std::shared_ptr<Piece>> white_rooks;
    std::vector<std::shared_ptr<Piece>> white_queens;
    std::vector<std::shared_ptr<Piece>> white_kings;

    int amount_of_black_pieces;
    int amount_of_white_pieces;

    // 64-square board containing shared pointers to the pieces
    std::vector<std::shared_ptr<Piece>> board;

    // History of moves mapped to the new MoveRecord struct
    std::vector<MoveRecord> history;

    Game();


    // ... existing Game properties ...

    void add_piece_to_list(std::shared_ptr<Piece> piece);
    void _place_piece(std::shared_ptr<Piece> piece);
    void _remove_piece(int i);
    bool check_for_piece(int pos, const std::string& color, const std::string& type, int move_counter);
    std::vector<std::shared_ptr<Piece>> get_white_pieces();
    std::vector<std::shared_ptr<Piece>> get_black_pieces();

    // ... existing Game properties and methods ...

    std::vector<int> _find_king_moves(int position, const std::string& turn);
    std::vector<int> _diagonal_ray(int start, int delta, const std::vector<std::shared_ptr<Piece>>& b, const std::string& turn);
    std::vector<int> _straight_ray(int start, int delta, const std::vector<std::shared_ptr<Piece>>& b, const std::string& turn);
    std::vector<int> _find_knight_moves(int position, const std::vector<std::shared_ptr<Piece>>& b, const std::string& turn);

    // ... existing Game properties and methods ...

    bool check_attacks(const std::string& color, int pos);

    // ... existing Game properties and methods ...

    std::vector<int> find_legal_moves(int position, std::shared_ptr<Piece> piece, const std::string& turn);

    // ... existing Game properties and methods ...

    void update_board(int original_position, int new_position, bool recursion = false);
    void revert_move();


    // ... existing Game properties and methods ...

    void import_board_string(const std::vector<std::string>& string_board);
    std::shared_ptr<Game> clone();
};
