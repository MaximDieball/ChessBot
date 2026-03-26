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
std::pair<std::vector<int>, double> _get_botv5_move_cpp(
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

    // Find all possible moves
    for (const auto& piece : moveable_pieces) {
        if (!piece) continue;
        std::vector<int> found_moves = game->find_legal_moves(piece->pos, piece, turn);
        for (int move : found_moves) {
            // Eval position
            game->update_board(piece->pos, move);
            double eval = evaluate_position_cpp(game, turn, piece_values, end_game_table, mid_game_table, opening_table);
            game->revert_move();
            possible_moves.push_back({piece->pos, move, eval});
        }
    }

    // Sort moves descending (highest evaluation first)
    std::sort(possible_moves.begin(), possible_moves.end(), [](const ScoredMove& a, const ScoredMove& b) {
        return a.evaluation > b.evaluation;
    });

    // If the king could be taken, the path is a checkmate
    if (game->white_kings.empty()) {
        if (turn == "w") return {{0, 0}, -INFINITY};
        else return {{0, 0}, INFINITY};
    }
    if (game->black_kings.empty()) {
        if (turn == "w") return {{0, 0}, INFINITY};
        else return {{0, 0}, -INFINITY};
    }

    // Very weird situation. Don't know what should happen here but having no moves seems bad
    if (possible_moves.empty()) {
        return {{0, 0}, -10000.0};
    }

    // Default to the best immediate move in case all deeper searches get pruned
    ScoredMove best_move = possible_moves[0];
    double best_eval = -INFINITY;

    if (depth <= 1) {
        return {{possible_moves[0].original_pos, possible_moves[0].new_pos}, possible_moves[0].evaluation};
    }

    for (const auto& move : possible_moves) {
        game->update_board(move.original_pos, move.new_pos);

        // Recursive call
        auto [found_move, opponent_eval] = _get_botv5_move_cpp(
            game, opponent_color, depth - 1, -beta, -alpha,
            piece_values, end_game_table, mid_game_table, opening_table
        );

        double found_eval = -opponent_eval;
        game->revert_move();

        // Update best move if we found a better evaluation
        if (found_eval > best_eval) {
            best_eval = found_eval;
            best_move = move;
        }

        // Update alpha
        alpha = std::max(alpha, found_eval);

        // Alpha-Beta Pruning
        if (alpha >= beta) {
            break;
        }
    }

    // King will be taken in the next moves
    if (best_eval == -INFINITY) {
        std::shared_ptr<Piece> king = nullptr;
        if (turn == "w" && !game->white_kings.empty()) king = game->white_kings[0];
        else if (turn == "b" && !game->black_kings.empty()) king = game->black_kings[0];

        // If the king will be taken but is currently not under attack (Stalemate)
        if (king && !game->check_attacks(turn, king->pos)) {
            return {{best_move.original_pos, best_move.new_pos}, 0.0};
        }
    }

    return {{best_move.original_pos, best_move.new_pos}, best_eval};
}

// ---------------------------------------------------------
// 3. Pybind11 Export
// ---------------------------------------------------------
PYBIND11_MODULE(bot_search, m) {
    m.doc() = "C++ Minimax Search Loop";

    // Expose a single start function that kicks off the C++ loop with initial alpha/beta
    m.def("start_cpp_search", [](
        std::shared_ptr<Game> game,
        std::string turn,
        int depth,
        std::unordered_map<std::string, int> piece_values,
        std::unordered_map<std::string, std::vector<int>> end_game_table,
        std::unordered_map<std::string, std::vector<int>> mid_game_table,
        std::unordered_map<std::string, std::vector<int>> opening_table
    ) {
        // Starts the search with -INFINITY and INFINITY for alpha and beta
        return _get_botv5_move_cpp(
            game, turn, depth, -INFINITY, INFINITY,
            piece_values, end_game_table, mid_game_table, opening_table
        );
    });
}