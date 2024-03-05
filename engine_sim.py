import pygame
import draw
import engine
import sys
import settings
sys.path.insert(1, './engines')
sys.path.insert(2, './cengines/cppfiles')
# import any other engines here
import materialistic_engine
import minimax
import minimax_iter
import minimax_quiescence_iter
import minimax_quiescence_hash
import minimax_hash
import aggy_king
import cengine
#import pystockfish

def main():
    pygame.init()
    pygame.font.init()

    config = settings.Settings().get_engine_sim_settings()

    n_games = config.n_games

    white_wins = 0
    black_wins = 0
    draws = 0
    for _ in range(0, n_games):
        # Choose which engine plays w white and black
        white_engine = cengine.Engine("white")
        black_engine = cengine.Engine("black")

        render = draw.Render(white_engine, black_engine)
        outcome = render.draw_screen()
        if outcome == True:
            white_wins += 1
        elif outcome == False:
            black_wins += 1
        else:
            draws += 1

    print(str(n_games) + " games simulated")
    print(str(100*white_wins/n_games) + "% won by white")
    print(str(100*black_wins/n_games) + "% won by black")
    print(str(100*draws/n_games) + "% drawn")

    pygame.quit()

if __name__ == "__main__":
    main()
