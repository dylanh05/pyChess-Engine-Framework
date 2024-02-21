import chess

e4 = chess.Move.from_uci("e2e4")
e5 = chess.Move.from_uci("e7e5")
e6 = chess.Move.from_uci("e7e6")
d4 = chess.Move.from_uci("d2d4")
d5 = chess.Move.from_uci("d7d5")
c4 = chess.Move.from_uci("c2c4")
c5 = chess.Move.from_uci("c7c5")
nf3 = chess.Move.from_uci("g1f3")
nc3 = chess.Move.from_uci("b1c3")
f4 = chess.Move.from_uci("f2f4")
e3 = chess.Move.from_uci("e2e3")
g3 = chess.Move.from_uci("g2g3")
nf6 = chess.Move.from_uci("g8f6")
nc6 = chess.Move.from_uci("b8c6")
c6 = chess.Move.from_uci("c7c6")

class Minimax_Helper:
    def __init__(self):
        self.values = {
            "p": -100,
            "n": -320,
            "b": -330,
            "r": -500,
            "q": -900,
            "k": -9000,
            "P": 100,
            "N": 320,
            "B": 330,
            "R": 500,
            "Q": 900,
            "K": 9000,
            ".": 0,
        }     

        self.opening_positions = {
            "move_1_white": {
                tuple([]): [e4, d4, c4, f4, nf3, g3],
            },
            "move_1_black": {
                tuple([e4]) : [e5, c5, c6],
                tuple([d4]) : [d5, chess.Move.from_uci("g8f6")],
                tuple([c4]) : [c5, e5, chess.Move.from_uci("e7e6")],
                tuple([g3]) : [c5, d5, e5],
                tuple([nf3]) : [c5, d5, c6, 
                                chess.Move.from_uci("e7e6"), chess.Move.from_uci("g8f6")],
            },
            "move_2_white": {
                tuple([e4,e5]) : [nf3, nc3, chess.Move.from_uci("f1c4"), d4, f4],
                tuple([e4, c6]) : [d4, c4, nc3, nf3],
                tuple([e4, c5]) : [d4, nf3, chess.Move.from_uci("c2c3"), nc3],
                tuple([d4, d5]) : [g3, nf3, c4, chess.Move.from_uci("c1f4")],
                tuple([c4, c5]) : [e3, nf3, e4, nc3],
                tuple([c4, e5]) : [chess.Move.from_uci("g2g3"), nf3, chess.Move.from_uci("e2e3"), nc3],
            },
            "move_2_black": {
                tuple([e4, e5, nf3]) : [chess.Move.from_uci("b8c6"), chess.Move.from_uci("g8f6"),
                                        chess.Move.from_uci("d7d6")],
                tuple([e4, e5, nc3]) : [chess.Move.from_uci("b8c6"), chess.Move.from_uci("g8f6"),
                                        chess.Move.from_uci("d7d6"), chess.Move.from_uci("f8b4"), chess.Move.from_uci("f8c5")],
                tuple([e4, e5, d4]) : [chess.Move.from_uci("e5d4")],

                tuple([e4, c6, d4]) : [d5, e6],
                tuple([e4, c6, c4]) : [d5],
                tuple([e4, c6, nc3]) : [d5, e5, e6],
                tuple([e4, c6, nf3]) : [d5, e6],

                tuple([e4, c5, d4]) : [chess.Move.from_uci("c5d4")],
                tuple([e4, c5, nf3]) : [chess.Move.from_uci("d7d6"), e6, nf6, nc6],
                tuple([e4, c5, nc3]) : [e6, nc6, chess.Move.from_uci("d7d6")],

                tuple([d4, d5, g3]) : [c6],
                tuple([d4, d5, nf3]) : [c6, e6, nf6, chess.Move.from_uci("c8f5")],
                tuple([d4, d5, c4]) : [c6, e6, chess.Move.from_uci("d5c4"), c5],

            },
        }

        mg_pawn_table = [
            0,   0,   0,   0,   0,   0,   0,   0,
            5,  10,  15,  20,  20,  15,  10,   5,
            4,   8,  12,  16,  16,  12,   8,   4,
            3,   6,   9,  12,  12,   9,   6,   3,
            2,   4,   6,   8,   8,   6,   4,   2,
            1,   2,   3, -10, -10,   3,   2,   1,
            0,   0,   0, -40, -40,   0,   0,   0,
            0,   0,   0,   0,   0,   0,   0,   0
        ]

        eg_pawn_table = [
            0,   0,   0,   0,   0,   0,   0,   0,
            30,  40,  45,  50,  50,  45,  40,   30,
            20,   18,  16,  16,  16,  16,   18,   20,
            3,   6,   9,  12,  12,   9,   6,   3,
            2,   4,   6,   8,   8,   6,   4,   2,
            1,   2,   3, -10, -10,   3,   2,   1,
            0,   0,   0, -40, -40,   0,   0,   0,
            0,   0,   0,   0,   0,   0,   0,   0
        ]

        mg_knight_table = [
            -167, -89, -34, -49,  61, -97, -15, -107,
            -73, -41,  5,  3,  2,  4,   1,  -17,
            -47,  31,  2,  4,  7, 6,  3,   3,
            -9,  1,  2,  5,  3,  3,  1,   2,
            -13,   2,  1,  3,  2,  1,  2,   -8,
            -23,  -9,  1,  1,  1,  1,  25,  -16,
            -29, -53, -12,  -3,  -1,  18, -14,  -19,
            -105, -21, -58, -33, -17, -28, -19,  -23]

        eg_knight_table = [
            -58, -38, -13, -28, -31, -27, -63, -99,
            -25,  -8, -25,  -2,  -9, -25, -24, -52,
            -24, -20,  10,   3,  -1,  -9, -19, -41,
            -17,   -4,  2,  2,  2,  1,   8, -18,
            -18,  -6,  1,  1,  1,  1,   1, -18,
            -23,  -3,  -1,  15,  10,  -3, -20, -22,
            -42, -20, -10,  -5,  -2, -20, -23, -44,
            -29, -51, -23, -15, -22, -18, -50, -64]

        mg_bishop_table = [
            -29,   4, -82, -37, -25, -42,   7,  -8,
            -26,  16, -18, -13,  30,  59,  18, -47,
            -16,  37,  43,  40,  35,  50,  37,  -2,
            -4,   5,  19,  50,  37,  37,   7,  -2,
            -6,  13,  13,  26,  34,  12,  10,   4,
            0,  15,  15,  15,  14,  27,  18,  10,
            4,  15,  16,   0,   7,  21,  33,   1,
            -33,  -3, -14, -21, -13, -12, -39, -21]

        eg_bishop_table = [
            -14, -21, -11,  -8, -7,  -9, -17, -24,
            -8,  -4,   7, -12, -3, -13,  -4, -14,
            2,  -8,   0,  -1, -2,   6,   0,   4,
            -3,   9,  12,   9, 14,  10,   3,   2,
            -6,   3,  13,  19,  7,  10,  -3,  -9,
            -12,  -3,   8,  10, 13,   3,  -7, -15,
            -14, -18,  -7,  -1,  4,  -9, -15, -27,
            -23,  -9, -23,  -5, -9, -16,  -5, -17]

        mg_rook_table = [
            32,  42,  32,  51, 63,  9,  31,  43,
            27,  32,  58,  62, 80, 67,  26,  44,
            -5,  19,  26,  36, 17, 45,  61,  16,
            -24, -11,   7,  26, 24, 35,  -8, -20,
            -36, -26, -12,  -1,  9, -7,   6, -23,
            -45, -25, -16, -17,  3,  0,  -5, -33,
            -44, -16, -20,  -9, -1, 11,  -6, -71,
            -19, -13,   1,  17, 16,  7, -37, -26]

        eg_rook_table = [
            13, 10, 18, 15, 12,  12,   8,   5,
            11, 13, 13, 11, -3,   3,   8,   3,
            7,  7,  7,  5,  4,  -3,  -5,  -3,
            4,  3, 13,  1,  2,   1,  -1,   2,
            3,  5,  8,  4, -5,  -6,  -8, -11,
            -4,  0, -5, -1, -7, -12,  -8, -16,
            -6, -6,  0,  2, -9,  -9, -11,  -3,
            -9,  2,  3, -1, -5, -13,   4, -20]

        mg_queen_table = [
            -28,   0,  29,  12,  59,  44,  43,  45,
            -24, -39,  -5,   1, -16,  57,  28,  54,
            -13, -17,   7,   8,  29,  56,  47,  57,
            -27, -27, -16, -16,  -1,  17,  -2,   1,
            -9, -26,  -9, -10,  -2,  -4,   3,  -3,
            -14,   2, -11,  -2,  -5,   2,  14,   5,
            -35,  -8,  11,   2,   8,  15,  -3,   1,
            -1, -18,  -9,  10, -15, -25, -31, -50,
        ]

        eg_queen_table = [
            -9,  22,  22,  27,  27,  19,  10,  20,
            -17,  20,  32,  41,  58,  25,  30,   0,
            -20,   6,   9,  49,  47,  35,  19,   9,
            3,  22,  24,  45,  57,  40,  57,  36,
            -18,  28,  19,  47,  31,  34,  39,  23,
            -16, -27,  15,   6,   9,  17,  10,   5,
            -22, -23, -30, -16, -16, -23, -36, -32,
            -33, -28, -22, -43,  -5, -32, -20, -41]

        mg_king_table = [
            -65,  23,  16, -15, -56, -34,   2,  13,
            29,  -1, -20,  -7,  -8,  -4, -38, -29,
            -9,  24,   2, -16, -20,   6,  22, -22,
            -17, -20, -12, -27, -30, -25, -14, -36,
            -49,  -1, -27, -39, -46, -44, -33, -51,
            -14, -14, -22, -46, -44, -30, -15, -27,
            1,   7,  -54, -64, -43, -40,   9,   8,
            -15,  36,  -54, -28,  -28, -28,  24,  14]

        eg_king_table = [
            -74, -35, -18, -18, -11,  15,   4, -17,
            -12,  17,  14,  17,  17,  38,  23,  11,
            10,  17,  23,  15,  20,  45,  44,  13,
            -8,  22,  24,  27,  26,  33,  26,   3,
            -18,  -4,  21,  24,  27,  23,   9, -11,
            -19,  -3,  11,  21,  23,  16,   7,  -9,
            -27, -11,   4,  13,  14,   4,  -5, -17,
            -53, -34, -21, -11, -28, -14, -24, -43]

        self.op_queen_table = [
            -50, -50, -50, -50, -50, -50, -50, -50,
            -50, -50, -50, -50, -50, -50, -50, -50,
            -50, -50, -50, -50, -50, -50, -50, -50,
            -50, -50, -50, -50, -50, -50, -50, -50,
            -50, -50, -50, -50, -50, -50, -50, -50,
            -50, -50, -50, -50, -50, -50, -50, -50,
            -50, -50, -50, -50, -50, -50, -50, -50,
            -50, -50, -50, 50, -50, -50, -50, -50,
        ]

        self.mg_table = {
            "p": mg_pawn_table,
            "n": mg_knight_table,
            "b": mg_bishop_table,
            "r": mg_rook_table,
            "q": mg_queen_table,
            "k": mg_king_table
        }

        self.eg_table = {
            "p": eg_pawn_table,
            "n": eg_knight_table,
            "b": eg_bishop_table,
            "r": eg_rook_table,
            "q": eg_queen_table,
            "k": eg_king_table
        }

    def get_piece_values(self):
        return self.values
    
    def get_openings(self):
        return self.opening_positions
    
    def get_mg_table(self):
        return self.mg_table
    
    def get_eg_table(self):
        return self.eg_table
    
    def get_op_queen_table(self):
        return self.op_queen_table