import pygame
import game
import colors
import settings
from stockfish import Stockfish

class Render:
    def __init__(self, engine, engine_for_sim):
        cols = colors.Colors()
        #self.stock = Stockfish()

        self.font = pygame.font.SysFont("liberationserif", 14)

        config = settings.Settings().get_draw_settings()

        self.draw_eval_bar = config.draw_eval_bar
        self.draw_stock = config.draw_stock
        self.cell_size = config.cell_size
        self.eval_bar_thkness = config.eval_bar_thkness
        self.black_sq_color =  config.black_sq_color
        self.white_sq_color = config.white_sq_color
        self.highlight_color = config.highlight_color

        self.eval_bar_white_col = config.eval_bar_white_col
        self.eval_bar_black_col = config.eval_bar_black_col

        self.stock_white_col = config.stock_white_col
        self.stock_black_col = config.stock_black_col

        #self.stockfish = Stockfish(path=r"\\wsl$\Ubuntu\home\dylanah\stockfish-windows-x86-64-modern\stockfish\stockfish-windows-x86-64-modern.exe")
        self.screen = pygame.display.set_mode((self.cell_size*8+self.eval_bar_thkness, self.cell_size*8))

        if self.draw_stock:
            self.screen = pygame.display.set_mode((self.cell_size*8+2*self.eval_bar_thkness, self.cell_size*8))
        

        self.clock = pygame.time.Clock()

        self.xposition_map = {self.cell_size*i:chr(i+97) for i in range(0,8)}
        self.yposition_map = {self.cell_size*i:8-i for i in range(0,8)}

        self.san_to_xposition = {chr(i+97):self.cell_size*i for i in range(0,8)}
        self.san_to_yposition = {8-i:self.cell_size*i for i in range(0,8)}

        self.highlight_squares = []
        self.highlight = False

        self.assets = {
            "r": pygame.image.load("./assets/br.png").convert_alpha(),
            "n": pygame.image.load("./assets/bn.png").convert_alpha(),
            "b": pygame.image.load("./assets/bb.png").convert_alpha(),
            "q": pygame.image.load("./assets/bq.png").convert_alpha(),
            "k": pygame.image.load("./assets/bk.png").convert_alpha(),
            "p": pygame.image.load("./assets/bp.png").convert_alpha(),
            "R": pygame.image.load("./assets/wr.png").convert_alpha(),
            "N": pygame.image.load("./assets/wn.png").convert_alpha(),
            "B": pygame.image.load("./assets/wb.png").convert_alpha(),
            "Q": pygame.image.load("./assets/wq.png").convert_alpha(),
            "K": pygame.image.load("./assets/wk.png").convert_alpha(),
            "P": pygame.image.load("./assets/wp.png").convert_alpha(),
        }

        self.game = game.Game()
        self.move = ""
        self.turn = "white"
        self.eval = 0
        self.text = 0
        self.eval_text = 0
        self.stock_val = 0
        self.stock_text = 0
        self.game_over = False
        self.engine = engine
        self.engine_sim = engine_for_sim

        pygame.display.set_caption("pyChess Engine Framework")


    def draw_board(self):
        board = pygame.Surface((self.cell_size * 8, self.cell_size * 8))
        board.fill(self.white_sq_color)
        for x in range(0, 8, 2):
            for y in range(0, 8, 1):
                j = x
                if y % 2 == 0:
                    j += 1
                pygame.draw.rect(board, self.black_sq_color, (j*self.cell_size, y*self.cell_size, self.cell_size, self.cell_size))
        
        # draw highlighted
        if self.highlight:
            for rect in self.highlight_rects:
                pygame.draw.rect(board, (0,0,0), pygame.Rect(rect[0], rect[1], self.cell_size, self.cell_size))
        return board 
    

    def draw_pieces(self):
        game_state = self.game.get_board()
        j = 0
        for i in range(0, 64):
            if i % 8 == 0 and i != 0:
                j += 1
            piece = game_state[i]
            if(piece != "."):    
                self.screen.blit(self.assets[piece], (self.cell_size*(i%8), self.cell_size*j))


    def draw_highlighted_squares(self, board):
        if self.highlight:
            for rect in self.highlight_squares:
                s = pygame.Surface((self.cell_size,self. cell_size))  # the size of your rect
                s.set_alpha(128)                # alpha level
                s.fill(self.highlight_color)           # this fills the entire surface
                self.screen.blit(s, (rect[0],rect[1]))    # (0,0) are the top-left coordinates
        return board

    def draw_stock_bar(self, eval):
        if self.draw_stock:
            w = pygame.Surface((self.eval_bar_thkness, self.cell_size*8))
            w.fill(self.stock_white_col)
            height = -eval*30+self.cell_size*4
            if height < 0:
                height = 0
            b = pygame.Surface((self.eval_bar_thkness, height))
            b.fill(self.stock_black_col)
            self.screen.blit(w, (self.cell_size*8+self.eval_bar_thkness, 0))    # (0,0) are the top-left coordinates
            self.screen.blit(b, (self.cell_size*8+self.eval_bar_thkness, 0))
        else:
            b = pygame.Surface((self.eval_bar_thkness, self.cell_size*8))
            b.fill(self.stock_black_col)
            self.screen.blit(b, (self.cell_size*8, 0))

        self.screen.blit(self.stock_text, (self.cell_size*8 + self.eval_bar_thkness, 0))


    def draw_eval(self, eval):
        if self.draw_eval_bar:
                w = pygame.Surface((self.eval_bar_thkness, self.cell_size*8))
                w.fill(self.eval_bar_white_col)
                height = -eval*30+self.cell_size*4
                if height < 0:
                    height = 0
                b = pygame.Surface((self.eval_bar_thkness, height))
                b.fill(self.eval_bar_black_col)
                self.screen.blit(w, (self.cell_size*8, 0))    # (0,0) are the top-left coordinates
                self.screen.blit(b, (self.cell_size*8, 0))

        else:
            b = pygame.Surface((self.eval_bar_thkness, self.cell_size*8))
            b.fill(self.eval_bar_black_col)
            self.screen.blit(b, (self.cell_size*8, 0))

        self.screen.blit(self.text, self.eval_text)


    def map_coord_to_square(self, pos):
        x = pos[0] - pos[0] % self.cell_size
        y = pos[1] - pos[1] % self.cell_size
        if x < 640 and y < 640:
            square = self.xposition_map[x] + str(self.yposition_map[y])
        else:
            square = None

        return square
    

    def map_coord_to_index(self, pos):
        x = (pos[0] - pos[0] % self.cell_size)/self.cell_size
        y = (pos[1] - pos[1] % self.cell_size)/self.cell_size
        return int(y*8 + x) 


    def highlight_legal_moves(self, square):
        squares = self.game.get_legal_moves(square)
        rect_pos = []
        for coord in squares:
            rect_pos.append((self.san_to_xposition[coord[0]], self.san_to_yposition[int(coord[1])]))

        self.highlight_squares = rect_pos


    def handle_move(self, pos):
        square = self.map_coord_to_square(pos)
        index = self.map_coord_to_index(pos)
        game_state = self.game.get_board()

        if self.move == "": 
            try:   
                if game_state[index] != '.':
                    self.highlight_legal_moves(square)
                    self.highlight = True
                    self.move = square
            except:
                x = 0
        elif len(self.move) == 2 and self.move != square:
            if self.game.check_legal_move(self.move+square):
                self.game.make_move(self.move+square, True)
                self.highlight = False
                self.highlight_squares.clear()

                if self.turn == "white":
                    self.turn = "black"
                else:
                    self.turn = "white"

                if self.game.check_game_over():
                    self.game_over = True

                self.move = ""
            
            elif game_state[index] != '.': # AND IS THE SAME COLOR AS THE PLAYER WHOS TURN IT IS!!
                self.move = square
                self.highlight_legal_moves(square)
                self.highlight = True
                self.move = square


    def handle_engine_move(self):
        game_state = self.game.get_board_raw()

        print_move = False
        if self.engine_sim == "none":
            print_move = True

        move, eval = self.engine.make_move(game_state)
        if eval == None:
            eval = self.eval
        else:
            if move in list(self.game.get_board_raw().legal_moves):
                self.game.get_board_raw().push(move)
            else:
                return eval
        pos = self.game.get_board_raw()
        if pos.can_claim_draw():    
            self.eval = 0
        pos.pop()

        self.game.make_move_uci(move, print_move)

        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

        if self.game.check_game_over():
            self.game_over = True

        return eval


    def handle_black_engine_move(self):
        game_state = self.game.get_board_raw()
        move, eval = self.engine_sim.make_move(game_state)
        if eval == None:
            eval = self.eval
        else:
            if move in list(self.game.get_board_raw().legal_moves):
                self.game.get_board_raw().push(move)
            else:
                return eval

        pos = self.game.get_board_raw()
        if pos.can_claim_draw():    
            self.eval = 0
        pos.pop()

        self.game.make_move_uci(move, False)

        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

        if self.game.check_game_over():
            self.game_over = True

        return eval

    def go_back_one_move(self):
        try:
            self.game.get_board_raw().pop()
            eval = self.handle_engine_move() 
            if eval != None:
                self.eval = eval
            self.game.get_board_raw().pop()
            self.move = ""
        except:
            print("No moves made, cannot go back.")
            
        if self.turn == "black":
            self.turn = "white"
        else:
            self.turn = "black"


    def draw_screen(self):
        running = True
        board = self.draw_board()

        # Evaluation text
        self.text = self.font.render(str(round(self.eval, 1)), True, self.eval_bar_black_col)
        self.eval_text = self.text.get_rect()
        self.eval_text.center = (self.cell_size*8 + self.eval_bar_thkness // 3, self.cell_size*8 - 20)
        
        stock_txt = self.font.render(str(round(self.stock_val, 1)), True, self.stock_black_col)
        self.stock_text = stock_txt.get_rect()
        self.stock_text.center = (self.cell_size*8 + self.eval_bar_thkness + self.eval_bar_thkness // 3, self.cell_size*8 - 20)
        pygame.event.set_allowed([pygame.QUIT, pygame.MOUSEBUTTONUP, pygame.KEYUP])

        first = True
        while running:
            update_made = False
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if not self.game_over:
                        self.handle_move(pos)
                        update_made = True

                elif event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT:
                        update_made = True
                        self.go_back_one_move()

            if self.engine_sim == "none":
                if not self.game_over:
                    if self.turn == self.engine.get_color() or self.engine.get_color() == "both":
                        update_made = True
                        self.eval = self.handle_engine_move()

            else:
                if not self.game_over:
                    update_made = True
                    if self.turn == "white":
                        self.eval = self.handle_engine_move()
                    else:
                        self.eval = self.handle_black_engine_move()

                    if self.game.get_board_raw().is_game_over():
                        self.game_over = True
                else:
                    running = False        

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill(self.white_sq_color)

            # RENDER YOUR GAME HERE
            self.text = self.font.render(str(round(self.eval, 1)), True, self.eval_bar_black_col)
            self.stock_text = self.font.render(str(round(self.stock_val, 1)), True, self.stock_black_col)
            self.screen.blit(board, board.get_rect())
            self.draw_highlighted_squares(board)
            self.draw_pieces()
            self.draw_eval(self.eval)
            if self.draw_stock:
                self.stock_val = self.stock.get_evaluation()['value']/100
                self.draw_stock_bar(self.stock_val)
            
            # flip() the display to put your work on screen
            if first:
                first = False
                pygame.display.flip()
            if update_made:
                #self.stock.set_fen_position(self.game.get_board_raw().fen())
                pygame.display.flip()

            self.clock.tick(240)  # limits FPS to 60
            if self.game.get_board_raw().is_game_over():
                return self.game.get_outcome()
        
        return self.game.get_outcome()
