// ------------------------------------------
// Python to C++ Bot Search Translation By Gemini
// ------------------------------------------

#include "../botLib/libv3.h"
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>
#include <vector>
#include <string>
#include <unordered_map>
#include <algorithm>
#include <cmath>
#include <limits>
#include <tuple>

namespace py = pybind11;

// A simple struct to hold our move evaluation data for easy sorting
struct ScoredMove {
    int original_pos;
    int new_pos;
    double evaluation;
};

// ---------------------------------------------------------
// 1. The Evaluation Function
// ---------------------------------------------------------
double evaluate_position_cpp(
    const std::shared_ptr<Game>& game,
    const std::string& turn,
    const std::unordered_map<std::string, int>& piece_values,
    const std::unordered_map<std::string, std::vector<int>>& end_game_table,
    const std::unordered_map<std::string, std::vector<int>>& mid_game_table,
    const std::unordered_map<std::string, std::vector<int>>& opening_table
) {
    double black_score = 0;
    double white_score = 0;
    int min_piece_count = std::min(game->amount_of_white_pieces, game->amount_of_black_pieces);

    // Pointer to the active table so we don't copy the whole dictionary
    const std::unordered_map<std::string, std::vector<int>>* active_value_table;

    if (min_piece_count <= 9) {
        active_value_table = &end_game_table;
    } else if (min_piece_count <= 14) {
        active_value_table = &mid_game_table;
    } else {
        active_value_table = &opening_table;
    }

    // Evaluate White Pieces
    for (const auto& piece : game->get_white_pieces()) {
        if (!piece) continue;
        double raw_val = piece_values.at(piece->type);
        double table_bonus = active_value_table->at(piece->type)[63 - piece->pos];
        white_score += (raw_val + table_bonus);
    }

    // Evaluate Black Pieces
    for (const auto& piece : game->get_black_pieces()) {
        if (!piece) continue;
        double raw_val = piece_values.at(piece->type);
        double table_bonus = active_value_table->at(piece->type)[piece->pos];
        black_score += (raw_val + table_bonus);
    }

    if (turn == "w") {
        return white_score - black_score;
    } else {
        return black_score - white_score;
    }
}


// ---------------------------------------------------------
// 2. The Recursive Minimax Search
// ---------------------------------------------------------
std::tuple<std::vector<int>, double, int> _get_botv5_move_cpp(
    std::shared_ptr<Game> game,
    std::string turn,
    int depth,
    double alpha,
    double beta,
    const std::unordered_map<std::string, int>& piece_values,
    const std::unordered_map<std::string, std::vector<int>>& end_game_table,
    const std::unordered_map<std::string, std::vector<int>>& mid_game_table,
    const std::unordered_map<std::string, std::vector<int>>& opening_table
) {
    std::vector<ScoredMove> possible_moves;
    std::string opponent_color = (turn == "w") ? "b" : "w";

    std::vector<std::shared_ptr<Piece>> moveable_pieces = (turn == "w") ? game->get_white_pieces() : game->get_black_pieces();

    for (const auto& piece : moveable_pieces) {
        if (!piece) continue;
        std::vector<int> found_moves = game->find_legal_moves(piece->pos, piece, turn);
        for (int move : found_moves) {
            game->update_board(piece->pos, move);
            double eval = evaluate_position_cpp(game, turn, piece_values, end_game_table, mid_game_table, opening_table);
            game->revert_move();
            possible_moves.push_back({piece->pos, move, eval});
        }
    }

    std::sort(possible_moves.begin(), possible_moves.end(), [](const ScoredMove& a, const ScoredMove& b) {
        return a.evaluation > b.evaluation;
    });

    // Added depth to the return statements
    if (game->white_kings.empty()) {
        if (turn == "w") return {{0, 0}, -INFINITY, depth};
        else return {{0, 0}, INFINITY, depth};
    }
    if (game->black_kings.empty()) {
        if (turn == "w") return {{0, 0}, INFINITY, depth};
        else return {{0, 0}, -INFINITY, depth};
    }

    if (possible_moves.empty()) {
        return {{0, 0}, -10000.0, depth};
    }

    ScoredMove best_move = possible_moves[0];
    double best_eval = -INFINITY;
    int best_move_depth = depth; // NEW

    if (depth <= 1) {
        return {{possible_moves[0].original_pos, possible_moves[0].new_pos}, possible_moves[0].evaluation, depth};
    }

    for (const auto& move : possible_moves) {
        game->update_board(move.original_pos, move.new_pos);

        // NEW: Unpack 3 values using C++17 structured bindings
        auto [found_move, opponent_eval, found_depth] = _get_botv5_move_cpp(
            game, opponent_color, depth - 1, -beta, -alpha,
            piece_values, end_game_table, mid_game_table, opening_table
        );

        double found_eval = -opponent_eval;
        game->revert_move();

        // NEW: Your checkmate delay logic
        if (found_eval > best_eval) {
            best_eval = found_eval;
            best_move = move;
            best_move_depth = found_depth;
        }
        else if (found_eval == -INFINITY && best_eval == -INFINITY && found_depth > best_move_depth) {
            best_eval = found_eval;
            best_move = move;
            best_move_depth = found_depth;
        }

        alpha = std::max(alpha, found_eval);

        if (alpha >= beta) {
            break;
        }
    }

    if (best_eval == -INFINITY) {
        std::shared_ptr<Piece> king = nullptr;
        if (turn == "w" && !game->white_kings.empty()) king = game->white_kings[0];
        else if (turn == "b" && !game->black_kings.empty()) king = game->black_kings[0];

        if (king && !game->check_attacks(turn, king->pos)) {
            return {{best_move.original_pos, best_move.new_pos}, 0.0, depth};
        }
    }

    return {{best_move.original_pos, best_move.new_pos}, best_eval, best_move_depth};
}

// ---------------------------------------------------------
// 3. Pybind11 Export
// ---------------------------------------------------------
PYBIND11_MODULE(bot_search, m) {
    m.doc() = "C++ Minimax Search Loop";

    m.def("start_cpp_search", [](
        std::shared_ptr<Game> game,
        std::string turn,
        int depth,
        std::unordered_map<std::string, int> piece_values,
        std::unordered_map<std::string, std::vector<int>> end_game_table,
        std::unordered_map<std::string, std::vector<int>> mid_game_table,
        std::unordered_map<std::string, std::vector<int>> opening_table
    ) {
        // Run the 3-value search
        auto [move, eval, result_depth] = _get_botv5_move_cpp(
            game, turn, depth, -INFINITY, INFINITY,
            piece_values, end_game_table, mid_game_table, opening_table
        );

        // Return ONLY 2 values back to Python so main.py doesn't crash!
        return std::make_pair(move, eval);
    });
}