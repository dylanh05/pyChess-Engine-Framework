import sys
import chess
import cengines.cengine as cengine

ceng = cengine.Engine("black")


board = chess.Board()

#ceng.print_moves()

move_and_eval = ceng.make_move(board)
print(move_and_eval)

