import chess
import random

class Engine:
    def __init__(self, color):
        self.color = color
        self.values = {
            "r": -5,
            "n": -3,
            "b": -3,
            "q": -9,
            "k": 0,
            "p": -1,
            "R": 5,
            "N": 3,
            "B": 3,
            "Q": 9,
            "K": 0,
            "P": 1,
            ".": 0
        }

    def get_color(self):
        return self.color


    # Define your own evaluation function here
    # Input positions are a single string with characters representing pieces (lowercase black, uppercase white)
    # ie. the starting position is represented
    # rnbqkbnrpppppppp................................PPPPPPPPRNBQKBNR

    # ACTUALLY RN INPUT POSITIONS ARE chess.board objects!!!!   
    def evaluate(self, position):
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


    def search(self, position):
        # YOUR CODE HERE
        return list(position.legal_moves)
    

    # Returns a UCI move based on search and evaluation of position
    # Position is a chess board
    def make_move(self, position):
        # YOUR CODE HERE
        moves = self.search(position)
        random.shuffle(moves)
        
        best_score = -10000
        best_move = "none"
        if self.color == "black":
            best_score = 10000
        
        for move in moves:
            position.push(move)
            score = self.evaluate(position)
            if self.color == "white":
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
            position.pop()

        return best_move
