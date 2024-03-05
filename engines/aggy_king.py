import random
import chess
from functools import wraps, lru_cache
import weakref
import time

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


class Engine:
    def __init__(self, color):
        self.depth = 3
        self.opening_prep = True
        self.color = color
        self.is_eg = False
        self.is_op = True
        self.eval_value = 0
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
            -74, -35, -18, -18, -11,  15,   4, -17,
            -12,  37,  34,  37,  37,  58,  43,  31,
            20,  37,  53,  45,  40,  65,  64,  33,
            -8,  42,  44,  47,  46,  53,  46,  13,
            -18,  16,  41,  44,  47,  43,  29, -1,
            -19,  17,  31,  41,  43,  36,   27,  -9,
            -27, 9,   24,  33,  34,  24,  15, -17,
            -53, -34, -21, -11, -28, -14, -24, -43]

        eg_king_table = [
            -74, -35, -18, -18, -11,  15,   4, -17,
            -12,  37,  34,  37,  37,  58,  43,  31,
            20,  37,  53,  45,  40,  65,  64,  33,
            -8,  42,  44,  47,  46,  53,  46,  13,
            -18,  16,  41,  44,  47,  43,  29, -1,
            -19,  17,  31,  41,  43,  36,   27,  -9,
            -27, 9,   24,  33,  34,  24,  15, -17,
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

        self.flip = [
            56,  57,  58,  59,  60,  61,  62,  63,
            48,  49,  50,  51,  52,  53,  54,  55,
            40,  41,  42,  43,  44,  45,  46,  47,
            32,  33,  34,  35,  36,  37,  38,  39,
            24,  25,  26,  27,  28,  29,  30,  31,
            16,  17,  18,  19,  20,  21,  22,  23,
            8,   9,  10,  11,  12,  13,  14,  15,
            0,   1,   2,   3,   4,   5,   6,   7
        ]

        self.cached_positions = {}
    
    class TreeNode:
        def __init__(self, state):
            self.state = state
            self.eval
            self.children = []

    def get_color(self):
        return self.color

    def lru_cache(maxsize=128, typed=False):
        def decorator(func):
            wraps(func)
            def wrapped_func(self, *args, **kwargs):
                self_weak = weakref.ref(self)
                wraps(func)
                lru_cache(maxsize=maxsize, typed=typed)
                def cached_method(*args, **kwargs):
                    return func(self_weak(), *args, **kwargs)
                setattr(self, func.__name__, cached_method)
                return cached_method(*args, **kwargs)
            return wrapped_func

        if callable(maxsize) and isinstance(typed, bool):
            # The user_function was passed in directly via the maxsize argument
            func, maxsize = maxsize, 128
            return decorator(func)
        return decorator
    

    def eval_value_adjust(self, board):
        fen = ''.join(str(board).split())
        score = 0
        for i in range(0, len(fen)):
            piece = fen[i]
            score += self.values[piece]

        #print(self.eval_value)

        if board.turn == chess.WHITE:
            self.eval_value = (self.eval_value-100)/100
            #if abs(score) < 110:
            #    self.eval_value = (self.eval_value+1700)/550
            #else:
            #    self.eval_value = (self.eval_value+1700)/200 + score/200
        else:
            self.eval_value = (self.eval_value+100)/100
            #if abs(score) < 110:
            #    self.eval_value = (self.eval_value+1700)/550
            #else:
            #    self.eval_value = (self.eval_value+1700)/200 + score/200

        #print(self.eval_value)

    # Define your own evaluation function here
    # Input positions are a single string with characters represeting pieces (lowercase black, uppercase white)
    # ie. the starting position is represented
    # rnbqkbnrpppppppp................................PPPPPPPPRNBQKBNR
    def evaluate(self, position):
        score = 0

        if position.is_checkmate():
            winner = position.outcome().winner
            if winner:
                return 100000
            else:
                return -100000
        
        if position.is_stalemate():    
            return 0
        
        fen = ''.join(str(position).split())

        for i in range(0, len(fen)):
            piece = fen[i]

            # Material values
            score += self.values[piece]
            # Piece square values
            if piece == ".":
                score  += 0

            elif piece == "q":
                flip_index = self.flip[i]
                if self.is_eg:
                    score -= self.eg_table[piece][flip_index] 
                elif self.is_op:
                    score -= self.op_queen_table[flip_index]
                else:
                    score -= self.mg_table[piece][flip_index]

            elif piece == "Q":
                piece = "q"
                if self.is_eg:
                    score += self.eg_table[piece][i]
                elif self.is_op:
                    score += self.op_queen_table[i]
                else:
                    score += self.mg_table[piece][i]

            elif piece.isupper():
                index = piece.lower()
                if self.is_eg:
                    score += self.eg_table[index][i]
                else:
                    score += self.mg_table[index][i]
            else:
                index = piece
                flip_index = self.flip[i]
                if self.is_eg:
                    score -= self.eg_table[index][flip_index]
                else:
                    score -= self.mg_table[index][flip_index]
       
            score += random.randint(-10, 10)
        return score


    def check_and_make_opening_move(self, board):
        start_pos = chess.Board()

        for opening_pos in self.opening_positions:
            for moves in self.opening_positions[opening_pos]:
                if board == chess.Board():
                    if moves == tuple([]):
                        return self.opening_positions[opening_pos][moves]
                
                else:
                    n_moves = len(moves)

                    for move in moves:
                        start_pos.push(move)

                    if board == start_pos:
                        return self.opening_positions[opening_pos][moves]
                    
                    for _ in range(0, n_moves):
                        start_pos.pop()

        self.opening_prep = False
        return moves    


    def check_game_phase(self, board):
        all_queens = True
        white_queen = False
        black_queen = False

        fen = ''.join(str(board).split())
        score = 0
        for i in range(0, len(fen)):
            piece = fen[i]
            if piece == "k" or piece == "K":
                continue
            score += abs(self.values[piece])
            if piece == 'q':
                black_queen = True
            if piece == "Q":
                white_queen = True
        
        if not white_queen or not black_queen:
            all_queens = False

        if score/100 < 69  or not all_queens:
            self.is_op = False

        # If in eg, deepen the search by 1
        if score/100 < 30 and not self.is_eg:
            self.depth = self.depth + 1
            self.is_eg = True



    def openings(self, board):
        moves = []
        moves = self.check_and_make_opening_move(board)

        if moves == []:
            self.opening_prep = False
            return moves, 0

        else:
            index = random.randint(0, len(moves)-1)
            return moves[index], 0.3


    # Returns a UCI move based on search and evaluation of position
    # Position is a chess board
    def make_move(self, board):
        #start_time = time.time()
        if self.opening_prep:
            move, eval = self.openings(board)
            self.eval_value = eval
            #print("Time to make move: " + str(time.time()-start_time))
            return move, eval

        self.check_game_phase(board)
        
        move = self.make_move_helper(board, depth=self.depth)

        self.eval_value_adjust(board)
        #print(self.eval)

        board.push(move)
        if board.can_claim_draw():
            board.pop()
            if self.color == "white" and self.eval_value > 0.5:
                return self.next_best_move(move, board, 3), self.eval_value
            
            elif self.color == "black" and self.eval_value < -0.5:
                return self.next_best_move(move, board, 3), self.eval_value
            
            else:
                self.eval_value = 0
                return move, 0

        else:
            board.pop()

        #print("Time to make move: " + str(time.time()-start_time))
        return move, self.eval_value

    def make_move_helper(self, board, depth):
        is_white = False
        if board.turn == chess.WHITE:
            is_white = True

        best_move = -10000000000 if is_white else 100000000000
        best_final = None
        moves = list(board.legal_moves)

        move_val_estimates = []
        for move in moves:
            board.push(move)
            move_val_estimates.append(self.evaluate(board))
            board.pop()
        rev = False
        if board.turn == chess.WHITE:
            rev = True
        moves = [x for _, x in sorted(zip(move_val_estimates, moves), key=lambda pair: pair[0], reverse=rev)]

        for move in moves:
            board.push(move)
            value = self.minimax_helper(depth - 1, board, -10000000000, 1000000000, not is_white)
            board.pop()
            if (is_white and value > best_move) or (not is_white and value < best_move):
                best_move = value
                best_final = move

        self.eval_value = best_move
        return best_final

    @lru_cache
    def minimax_helper(self, depth, board, alpha, beta, is_maximizing):
        if depth <= 0 or board.is_game_over():
            return self.evaluate(board)

        moves = list(board.legal_moves)
        if depth >= 4:
            move_val_estimates = []
            for move in moves:
                board.push(move)
                move_val_estimates.append(self.evaluate(board))
                board.pop()

            moves = [x for _, x in sorted(zip(move_val_estimates, moves), key=lambda pair: pair[0], reverse=is_maximizing)]

        if is_maximizing:
            best_move = -10000000
            for move in moves:
                board.push(move)
                value = self.minimax_helper(depth - 1, board, alpha, beta, False)
                board.pop()
                best_move = max(best_move, value)
                alpha = max(alpha, best_move)
                if beta <= alpha:
                    break
            return best_move
        
        else:
            best_move = 10000000
            for move in moves:
                board.push(move)
                value = self.minimax_helper(depth - 1, board, alpha, beta, True)
                board.pop()
                best_move = min(best_move, value)
                beta = min(beta, best_move)
                if beta <= alpha:
                    break
            return best_move
        
    def next_best_move(self, draw_move, board, depth):
        is_white = False
        if board.turn == chess.WHITE:
            is_white = True

        best_move = -10000000000 if is_white else 100000000000
        best_final = None
        moves = list(board.legal_moves)
        move_val_estimates = []
        for move in moves:
            board.push(move)
            move_val_estimates.append(self.evaluate(board))
            board.pop()
        
        moves = [x for _, x in sorted(zip(move_val_estimates, moves), key=lambda pair: pair[0])]
        moves.reverse()

        for move in moves:
            if draw_move == move:
                continue
            board.push(move)
            value = self.minimax_helper(depth - 1, board, -10000000000, 1000000000, not is_white)
            board.pop()
            if (is_white and value > best_move) or (not is_white and value < best_move):
                best_move = value
                best_final = move

        self.eval_value = best_move
        return best_final