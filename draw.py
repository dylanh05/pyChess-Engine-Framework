import pygame
import game

class Render:
    def __init__(self, engine, engine_for_sim):
        self.cell_size = 80
        self.black_sq_color = (210, 180, 140)
        self.white_sq_color = (252, 248, 220)
        self.highlight_color = (255,255,153)

        self.screen = pygame.display.set_mode((self.cell_size*8, self.cell_size*8))
        self.clock = pygame.time.Clock()

        self.xposition_map = {self.cell_size*i:chr(i+97) for i in range(0,8)}
        self.yposition_map = {self.cell_size*i:8-i for i in range(0,8)}

        self.san_to_xposition = {chr(i+97):self.cell_size*i for i in range(0,8)}
        self.san_to_yposition = {8-i:self.cell_size*i for i in range(0,8)}

        self.highlight_squares = []
        self.highlight = False

        self.assets = {
            "r": pygame.image.load("./assets/br.png"),
            "n": pygame.image.load("./assets/bn.png"),
            "b": pygame.image.load("./assets/bb.png"),
            "q": pygame.image.load("./assets/bq.png"),
            "k": pygame.image.load("./assets/bk.png"),
            "p": pygame.image.load("./assets/bp.png"),
            "R": pygame.image.load("./assets/wr.png"),
            "N": pygame.image.load("./assets/wn.png"),
            "B": pygame.image.load("./assets/wb.png"),
            "Q": pygame.image.load("./assets/wq.png"),
            "K": pygame.image.load("./assets/wk.png"),
            "P": pygame.image.load("./assets/wp.png"),
        }

        self.game = game.Game()
        self.move = ""
        self.turn = "white"
        self.game_over = False
        self.engine = engine
        self.engine_sim = engine_for_sim


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


    def map_coord_to_square(self, pos):
        x = pos[0] - pos[0] % self.cell_size
        y = pos[1] - pos[1] % self.cell_size
        square = self.xposition_map[x] + str(self.yposition_map[y])
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
            if game_state[index] != '.':
                self.highlight_legal_moves(square)
                self.highlight = True
                self.move = square

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

        move = self.engine.make_move(game_state)
        self.game.make_move_uci(move, print_move)

        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

        if self.game.check_game_over():
            self.game_over = True


    def handle_black_engine_move(self):
        game_state = self.game.get_board_raw()
        move = self.engine_sim.make_move(game_state)
        self.game.make_move_uci(move, False)

        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

        if self.game.check_game_over():
            self.game_over = True


    def draw_screen(self):
        running = True
        board = self.draw_board()

        while running:
            # poll for events
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                elif event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    if not self.game_over:
                        self.handle_move(pos)

            if self.engine_sim == "none":
                if not self.game_over:
                    if self.turn == self.engine.get_color() or self.engine.get_color() == "both":
                        self.handle_engine_move()

            else:
                if not self.game_over:
                    if self.turn == "white":
                        self.handle_engine_move()
                    else:
                        self.handle_black_engine_move()

                else:
                    running = False        

            # fill the screen with a color to wipe away anything from last frame
            self.screen.fill("purple")

            # RENDER YOUR GAME HERE
            self.screen.blit(board, board.get_rect())
            self.draw_highlighted_squares(board)
            self.draw_pieces()

            # flip() the display to put your work on screen
            pygame.display.flip()

            self.clock.tick(240)  # limits FPS to 60
        
        return self.game.get_outcome()
