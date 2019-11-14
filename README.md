
# WorstFish 

A sub 60 line file that wraps the Stockfish chess engine and plays 
the move that was found to be the *worst* move by Stockfish's eval function.

It's extraordinarily good at getting itself checkmated.

# Usage

```python3
import chess
from worstfish import *


engine = chess.engine.SimpleEngine.popen_uci("stockfish_10_x64_popcnt" if os.name == 'nt' else './stockfish_10_x64_modern')

board = chess.Board()

w = WorstFish(engine)

move = w.get_move(board)

board.push(move)
```

Have Fun!