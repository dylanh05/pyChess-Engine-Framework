import chess
import random
import stockfish
import time

class Engine:
    def __init__(self, color):
        self.color = color
        self.stock = stockfish.Stockfish()
        self.opening_prep = True
        self.opening_path = "./openings/Human.bin"
        self.sleep = False
        self.new_game = False
    def get_color(self):
        return self.color


    # Define your own evaluation function here
    # Input positions are chess.Board() objects
    def evaluate(self, position):
        # YOUR CODE HERE

        return 0


    def search(self, position):
        # YOUR CODE HERE

        return 0
    
    def openings(self, board):
        moves = []
        moves = self.check_and_make_opening_move(board)

        if moves == []:
            self.opening_prep = False
            return moves, 0.3

        else:
            index = random.randint(0, len(moves)-1)
            if self.sleep:
                time.sleep(0.001)
            return moves[index], 0.3

    def check_and_make_opening_move(self, board):
        with chess.polyglot.open_reader(self.opening_path) as reader:
            entries = []
            for entry in reader.find_all(board):
                entries.append(entry.move)

            random.shuffle(entries)
        return entries

    # Returns a UCI move based on search and evaluation of position
    # Position is a chess.Board() object
    def make_move(self, position):
        start_time = time.time()
        if self.opening_prep:
            move, eval = self.openings(position)
            self.eval_value = eval
            if not self.sleep:
                self.sleep = True
            #print("Time to make move for minimax: " + str(time.time()-start_time))
            return move, eval

        t1 = time.time()
        self.stock.set_fen_position(position.fen())
        move = self.stock.get_best_move_time(100)
        move = chess.Move.from_uci(move)
        position.push(move)
        self.stock.set_fen_position(position.fen())
        eval = self.stock.get_evaluation()
        position.pop()
        #print("Time for minimax with q iter and hash:" + str(time.time()-t1))
        with open("stockfish-evals.txt", "a") as f:
            if not move in position.legal_moves:
                if self.new_game:
                    f.write("New game!")
                    f.write('\n')

                    self.new_game = False
            else:
                self.new_game = True
                f.write(str(move)+","+str(eval['value']))
                f.write('\n')

        return move, eval['value']/100
