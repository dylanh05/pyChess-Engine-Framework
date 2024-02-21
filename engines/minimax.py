import sys
sys.path.insert(1, './engines')

import random
import chess
import minimax_helper
from functools import wraps, lru_cache
import weakref
#import time

class Engine:
    def __init__(self, color):
        self.depth = 2
        self.opening_prep = True
        self.color = color
        self.is_eg = False
        self.is_op = True
        self.eval_value = 0

        helper = minimax_helper.Minimax_Helper()
        self.values = helper.get_piece_values()
        self.opening_positions = helper.get_openings()
        self.mg_table = helper.get_mg_table()
        self.eg_table = helper.get_eg_table()
        self.op_queen_table = helper.get_op_queen_table()
        
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

        if board.turn == chess.WHITE:
            if abs(score) < 110:
                self.eval_value = (self.eval_value-100)/400
            else:
                self.eval_value = (self.eval_value-100)/100
        else:
            if abs(score) < 110:
                self.eval_value = (self.eval_value+100)/400
            else:
                self.eval_value = (self.eval_value+100)/100

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
            #self.depth = self.depth + 1
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