import chess
import random

class Engine:
    def __init__(self, color):
        self.color = color
        self.values = {
            "p": -10,
            "n": -30,
            "b": -30,
            "r": -50,
            "q": -90,
            "k": -900,
            "P": 10,
            "N": 30,
            "B": 30,
            "R": 50,
            "Q": 90,
            "K": 900,
            ".": 0,
        }
    
    class TreeNode:
        def __init__(self, state):
            self.state = state
            self.eval
            self.children = []

    def get_color(self):
        return self.color


    # Define your own evaluation function here
    # Input positions are a single string with characters representing pieces (lowercase black, uppercase white)
    # ie. the starting position is represented
    # rnbqkbnrpppppppp................................PPPPPPPPRNBQKBNR
    def evaluate(self, position):
        # YOUR CODE HERE
        if position.is_checkmate():
            if self.color == "black":
                return -10000
            else:
                return 10000
        
        if position.is_stalemate():    
            return 0
        
        # YOUR CODE HERE
        fen = ''.join(str(position).split())
        
        score = 0
        for i in range(0, len(fen)):
            score += self.values[fen[i]]
        
        return score

    # Returns a UCI move based on search and evaluation of position
    # Position is a chess board
    def make_move(self, board):
        return self.make_move_helper(board, 3)

    def make_move_helper(self, board, depth=3):
        is_white = False
        if self.color == "white":
            is_white = True

        best_move = -100000 if is_white else 100000
        best_final = None
        moves = list(board.legal_moves)
        random.shuffle(moves)
        for move in moves:
            board.push(move)
            value = self._minimax_helper(depth - 1, board, -10000, 10000, not is_white)
            board.pop()
            if (is_white and value > best_move) or (not is_white and value < best_move):
                best_move = value
                best_final = move
        return best_final

    def _minimax_helper(self, depth, board, alpha, beta, is_maximizing):
        if depth <= 0 or board.is_game_over():
            return self.evaluate(board)

        if is_maximizing:
            best_move = -100000
            moves = list(board.legal_moves)
            random.shuffle(moves)
            for move in moves:
                board.push(move)
                value = self._minimax_helper(depth - 1, board, alpha, beta, False)
                board.pop()
                best_move = max(best_move, value)
                alpha = max(alpha, best_move)
                if beta <= alpha:
                    break
            return best_move
        
        else:
            best_move = 100000
            for move in board.legal_moves:
                board.push(move)
                value = self._minimax_helper(depth - 1, board, alpha, beta, True)
                board.pop()
                best_move = min(best_move, value)
                beta = min(beta, best_move)
                if beta <= alpha:
                    break
            return best_move