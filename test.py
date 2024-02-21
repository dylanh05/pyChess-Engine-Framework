import chess
import random
import chess.polyglot

board = chess.Board()
board.push(chess.Move.from_uci("c2c4"))

with chess.polyglot.open_reader("./openings/baron30.bin") as reader:
    entries = list(reader.find_all(board))
    for entry in reader.find_all(board):
        print(entry.move, entry.weight, entry.learn)

    print(entries[random.randint(0, len(entries)-1)].move)
