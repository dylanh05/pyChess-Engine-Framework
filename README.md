# Python Chess Engine Framework and Test Environment

## Features
### Framework features
- Fully functional chess game built with python chess library.
- Starter file for chess engine, which can be used to build custom chess engines.
- Play against chess engines as white or black, or play a game without engines for two player mode.
- Test environment which simulates games between engines. Prints statistics about game outcomes.
  
### Minimax features
- Minimax algorithm with customizable depth (default=3).
- Opening database to play book moves for the first two turns.
- Evaluation function with piece square tables to encourage strategic piece placement. Piece square tables change based on phase of the game.
- Alpha-beta pruning optimization.
- Move ordering to search high value captures first when depth >= 4.

## How to use
### Run a game
1. From the root directory, run main.py. By default main.py will start a game with the minimax engine playing as black.
2. To change the game settings, open main.py.
3. To play against a different engine, edit the line chess_engine = minimax.Engine("black") to get the Engine class from a different file. You can also set the color to "white" to give the engine the white pieces.
4. To play against someone else, edit the line chess_engine = minimax.Engine("black") and set the color to "none".
5. Rerun main.py once the settings have been updated.
   
### Run the test environement
1. From the root directory, run engine_sim.py. By default engine_sim.py will begin a 10 game match between minimax engines of depth 3.
2. To change the environment settings, open engin_sim.py.
3. To change the number of games played, edit the line n_games = 10 to the number of games you wish to simulate.
4. To change the white or black engine, edit the line white_engine = minimax.Engine("white") (or black_engine =...) to get the Engine class from a different file.
5. Rerun engin_sim.py with the updated settings.

### Building engines
1. Make a copy of engine.py and save it as {ENGINE_NAME}.py.
2. Fill in the functions as directed by the starter file. In order to make a fully functioning bot, only the make_move() function needs to be completed. It must return a legal move and associated evaluation of the position to work.
3. For more complex bots, update the search() and evaluate() functions.
4. Once bot has been completed, play against it by running main.py after updating the game settings (see Run a game), or test it against other bots by running engin_sim.py after updating the test environment settings (see Run the test environment).

## Example
Real time example of minimax with depth 3 playing itself:
<p align="center">
<img src = 'https://github.com/dylanh05/pyChess-Engine-Framework/blob/main/python-chess-engine.gif' alt="animated">
</p>
