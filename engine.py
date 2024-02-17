import chess
import random

class Engine:
    def __init__(self, color):
        self.color = color

    def get_color(self):
        return self.color


    # Define your own evaluation function here
    # Input positions are a single string with characters representing pieces (lowercase black, uppercase white)
    # ie. the starting position is represented
    # rnbqkbnrpppppppp................................PPPPPPPPRNBQKBNR

    # ACTUALLY RN INPUT POSITIONS ARE chess.board objects!!!!   
    def evaluate(self, position):
        # YOUR CODE HERE

        return 0


    def search(self, position):
        # YOUR CODE HERE

        return 0
    

    # Returns a UCI move based on search and evaluation of position
    # Position is a chess board
    def make_move(self, position):
        # YOUR CODE HERE

        # Example engine that randomly selects a random legal move:
        move = list(position.legal_moves)[random.randint(0, position.legal_moves.count()-1)]

        return move
