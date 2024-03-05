from stockfish import Stockfish
import chess
import chess.polyglot
import random
import sys
import time
sys.path.insert(1, './engines')
import minimax_iter

def check_and_make_opening_move(board):
    with chess.polyglot.open_reader("./openings/baron30.bin") as reader:
        entries = []
        for entry in reader.find_all(board):
            entries.append(entry.move)
        random.shuffle(entries)
    return entries

stock = Stockfish()


with open("stockfish-evals.txt", "a") as f:
    n_games = 4
    time_per_move = 0.05

    stock_play_states = ["white", "black", "both"]

    for i in range(0, n_games):
        stock_play_state = stock_play_states[random.randint(0, len(stock_play_states)-1)]
        minimax = None
        if stock_play_state == "black":
            minimax = minimax_iter.Engine("black")

        elif stock_play_state == "white":
            minimax = minimax_iter.Engine("white")

        board = chess.Board()
        turn = 0
        first = True
        while board.outcome() == None:
            if first:
                f.write("New game begins!")
                f.write('\n')
                first = False

            if stock_play_state == "both":
                move = stock.get_best_move()
                try:
                    board.push(chess.Move.from_uci(move))
                    if board.is_game_over():
                        break
                    board.pop()
                except:
                    print("Trying again")
                if move != None:
                    try:
                        board.push(chess.Move.from_uci(move))
                        stock.set_fen_position(board.fen())
                        eval = stock.get_evaluation()
                        f.write(str(move) +"," + str(eval['value']))
                        f.write('\n')
                    except:
                        print("Trying again")
                else:
                    continue

            elif stock_play_state == "black":
                if turn == 0:
                    if minimax != None:
                        move, eval = minimax.make_move(board)
                        if move != []:
                            board.push(move)
                            stock.set_fen_position(board.fen())
                            eval = stock.get_evaluation()
                            f.write(str(move) + "," + str(eval['value']))
                            f.write('\n')
                            turn = 1
                        else:
                            break
                    else:
                        break
                else:
                    move = stock.get_best_move()
                    if move != None:
                        try:
                            board.push(chess.Move.from_uci(move))
                            stock.set_fen_position(board.fen())
                            eval = stock.get_evaluation()
                            f.write(str(move) + "," + str(eval['value']))
                            f.write('\n')
                            turn = 0
                        except:
                            continue
                    else:
                        break


            elif stock_play_state == "white":
                if turn == 1:
                    if minimax != None:
                        move, eval = minimax.make_move(board)
                        if move != []:
                            board.push(move)
                            stock.set_fen_position(board.fen())
                            eval = stock.get_evaluation()
                            f.write(str(move) + "," + str(eval['value']))
                            f.write('\n')
                            turn = 0
                        else:
                            break
                    else:
                        break
                else:
                    move = stock.get_best_move()
                    if move != None:
                        try:
                            board.push(chess.Move.from_uci(move))
                            stock.set_fen_position(board.fen())
                            eval = stock.get_evaluation()
                            f.write(str(move) + "," + str(eval['value']))
                            f.write('\n')
                            turn = 1
                        except:
                            continue
                    else:
                        break
