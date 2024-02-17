import pygame
import draw
import engine
import sys
sys.path.insert(1, './engines')
# import any other engines here
import materialistic_engine
import minimax

def main():
    pygame.init()

    # Choose which engine plays w white and black
    white_engine = materialistic_engine.Engine("white")
    black_engine = materialistic_engine.Engine("black")

    white_wins = 0
    black_wins = 0
    draws = 0
    n_games = 10

    for _ in range(0, n_games):
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
