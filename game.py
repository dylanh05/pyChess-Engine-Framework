import chess
import time

class Game:
    def __init__(self):
        self.board = chess.Board()


    def get_board(self):
        return ''.join(str(self.board).split())
    

    def get_board_raw(self):
        return self.board


    def check_legal_move(self, move):
        move = chess.Move.from_uci(move)
        if move in self.board.legal_moves:
            return True
        return False

    # Gets all legal moves starting from square
    def get_legal_moves(self, square):
        return [str(move)[2:4] for move in self.board.legal_moves if str(move)[:2] == square]


    def make_move(self, move, print_move):
        if self.board.can_claim_draw():
            self.board.reset()
            return
        move = chess.Move.from_uci(move)

        first = bool((int(chess.square_name(move.to_square)[1]) == 8 or int(chess.square_name(move.to_square)[1]) == 1))
        second =  bool(str(self.board.piece_at(move.from_square)) == "P" or str(self.board.piece_at(move.from_square)) == "p")

        # Pawn promotions to queen
        if ((int(chess.square_name(move.to_square)[1]) == 8 or int(chess.square_name(move.to_square)[1]) == 1)
            and (str(self.board.piece_at(move.from_square)) == "P" or str(self.board.piece_at(move.from_square)) == "p")):
            move = chess.Move.from_uci(str(move)+"q")

        if print_move:
            print(self.board.san(move))
        if move != None:
            self.board.push(move)

    
    def make_move_uci(self, move, print_move):
        if self.board.can_claim_draw():
            self.board.reset()
            return
        if print_move:
            print(self.board.san(move))
        if move != None:
            self.board.push(move)


    def check_game_over(self):
        result = self.board.outcome(claim_draw = True)
        if result != None:
            time.sleep(2)
            print(str(result))
            return True
        return False
    
    def get_outcome(self):
        try:
            return self.board.outcome().winner
        except:
            return None
