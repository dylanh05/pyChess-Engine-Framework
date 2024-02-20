import pygame
import draw
import engine
import sys
sys.path.insert(1, './engines')
import materialistic_engine
import minimax

def main():
    pygame.init()
    pygame.font.init()
    # Set engine to play as white, black, both or none for 2 player games
    chess_engine = minimax.Engine("black")
    render = draw.Render(chess_engine, "none")
    render.draw_screen()
    pygame.quit()

if __name__ == "__main__":
    main()
