import chess

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
        outcome = self.board.outcome()
        if outcome != None:
            print(str(outcome))
            return True
        return False
    
    def get_outcome(self):
        return self.board.outcome().winner