import chess
import random
from build.cEngine import *
import time

class Engine:
    def __init__(self, color):
        self.run_cpp_file = False
        self.color = color
        self.cEngine = cEngine(color)

    def get_color(self):
        return self.color

    # Returns a UCI move based on search and evaluation of position
    # Position is a chess.Board() object
    def make_move(self, position):
        move = None
        eval = 0

        start_time = time.time()
        move, eval = self.cEngine.make_move(position.fen())
        print("Time to make move for C++ minimax iter: " + str(time.time()-start_time))
        move = chess.Move.from_uci(move)
        return move, eval