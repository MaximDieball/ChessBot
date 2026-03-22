opening_pawn_value_table = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 5, 0, 0, 0, 0, 5, 5,
    0, 5, 10, 10, 10, 10, 5, 0,
    0, 5, 15, 20, 20, 15, 5, 0,
    0, 0, 20, 30, 30, 20, 0,  0,
    0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0,  0,  0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0
]

mid_game_pawn_value_table = [
    0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  20, 20, 20, 20, 0,  0,
    0,  10, 20, 20, 20, 20, 10, 0,
    0,  10,  20, 20, 20, 20, 10,  0,
    30,  30,  30,  30,  30,  30,  30,  30,
    0,  0,  0,  0,  0,  0,  0,  0
]

end_game_pawn_value_table = [
    0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,
    10,  10, 10, 10, 10, 10, 10, 10,
    30,  30, 30, 30, 30, 30, 30, 30,
    70,  70, 70, 70, 70, 70, 70, 70,
    100, 100, 100, 100, 100, 100, 100, 100,
    0,  0,  0,  0,  0,  0,  0,  0
]

# Knights (Base 320)
general_knight_value_table = [
    0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,
    0,  20, 30, 30, 30, 30, 20, 0,
    0,  20, 30, 30, 30, 30, 20, 0,
    0,  30, 40, 40, 40, 40, 30, 0,
    0,  30, 40, 40, 40, 40, 30, 0,
    0,  28, 28, 28, 28, 28, 28, 0,
    0,  0,  0,  0,  0,  0,  0,  0
]

general_bishop_value_table = [0] * 64

# Rooks (Base 500)
general_rook_value_table = [
    -10, 0,  10,  20, 20, 10,  0, -10,
    0,    0,  0,  0,   0,   0,  0,  0,
    0,    0,  0,  0,   0,   0,  0,  0,
    0,    0,  0,  0,   0,   0,  0,  0,
    0,   0, 0, 0,  0,  0, 0, 0,
    50,  50, 50, 50, 50, 50, 50, 50,
    100,  100, 100, 100, 100, 100, 100, 100,
    100,  100, 100, 100, 100, 100, 100, 100
]

# Queens (Base 900)
general_queen_value_table = [
    0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,
    0,  0,  0,  0,  0,  0,  0,  0,
    20, 0,  0,  0,  0,  0,  0,  20,
    20, 0,  0,  0,  0,  0,  0,  20,
    20, 20, 20, 20, 20, 20, 20, 20,
    100, 100, 100, 100, 100, 100, 100, 100,
    100, 100, 100, 100, 100, 100, 100, 100
]

# King (Base 20000)
opening_king_value_table = [
    35,  35,  21,  0, 0, 21,  35,  35,
    0, -28, -28, -28, -28, -28, -28, 0,
    -100, -100, -100, -100, -100, -100, 100, -100,
    -100, -100, -100, -100, -100, -100, 100, -100,
    -100, -100, -100, -100, -100, -100, 100, -100,
    -100, -100, -100, -100, -100, -100, 100, -100,
    -100, -100, -100, -100, -100, -100, 100, -100,
    -100, -100, -100, -100, -100, -100, 100, -100
]

mid_game_king_value_table = [
    35,  35,  21,  0, 0, 21,  35,  35,
    0, -28, -28, -28, -28, -28, -28, 0,
    -100, -100, -100, -100, -100, -100, 100, -100,
    -100, -100, -100, -100, -100, -100, 100, -100,
    -100, -100, -100, -100, -100, -100, 100, -100,
    -100, -100, -100, -100, -100, -100, 100, -100,
    -100, -100, -100, -100, -100, -100, 100, -100,
    -100, -100, -100, -100, -100, -100, 100, -100
]

end_game_king_value_table = [0] * 64

# Dictionaries
opening_value_tables = {
    "E": end_game_king_value_table,
    "P": opening_pawn_value_table,
    "N": general_knight_value_table,
    "B": general_bishop_value_table,
    "R": general_rook_value_table,
    "Q": general_queen_value_table,
    "K": opening_king_value_table
}

mid_game_value_tables = {
    "E": end_game_king_value_table,
    "P": mid_game_pawn_value_table,
    "N": general_knight_value_table,
    "B": general_bishop_value_table,
    "R": general_rook_value_table,
    "Q": general_queen_value_table,
    "K": mid_game_king_value_table
}

end_game_value_tables = {
    "E": end_game_king_value_table,
    "P": end_game_pawn_value_table,
    "N": general_knight_value_table,
    "B": general_bishop_value_table,
    "R": general_rook_value_table,
    "Q": general_queen_value_table,
    "K": end_game_king_value_table
}