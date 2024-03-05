import pygame
import draw
import engine
import sys
sys.path.insert(1, './engines')
sys.path.insert(2, './cengines/cppfiles')
import materialistic_engine
import minimax_quiescence
import minimax_quiescence_iter
import minimax
import aggy_king
import pystockfish
import cengine

def main():
    pygame.init()
    pygame.font.init()
    # Set engine to play as white, black, both or none for 2 player games
    chess_engine = cengine.Engine("black")
    render = draw.Render(chess_engine, "none")
    render.draw_screen()
    pygame.quit()

if __name__ == "__main__":
    main()
