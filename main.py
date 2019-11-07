import chess
import chess.engine
import asyncio
import sys
import random
from chess import WHITE, BLACK

NotOpening = 1
Opening = 2
DoneOpening = 3


class WorstFish:
    def __init__(self):
        self.engine = chess.engine.SimpleEngine.popen_uci("./stockfish-10-win/Windows/stockfish_10_x64_bmi2.exe")
        self.opening_status = NotOpening
        self.opening_type = None

    def _get_worst_move(self, board):
        ai_color = board.turn

        move_scores = {}

        for move in board.legal_moves:
            board.push(move)
            board_score = self.engine.analyse(board, chess.engine.Limit(time=0.2), info=chess.engine.INFO_ALL)
            move_scores[move] = board_score["score"].white()
            board.pop()

        if ai_color == WHITE:
            # Find the move that is most detrimental to the AI's chance of winning
            best_move = min(move_scores, key=move_scores.get)
        else:
            best_move = max(move_scores, key=move_scores.get)

        return best_move

    def _get_opening_move(self, board):
        ai_color = board.turn

        moves = self.opening_type.split()
        if ai_color == WHITE:
            playable_moves = moves[::2]
        else:
            playable_moves = moves[1::2]
        try:
            move = chess.Move.from_uci(playable_moves[board.fullmove_number - 1])
        except:
            self.opening_status = DoneOpening
            return self._get_worst_move(board)
        else:
            if move in board.legal_moves:
                return move
            else:
                print("Move %s failed!" % move)
                return self._get_worst_move(board)

    def get_move(self, board=None):
        if board is None:
            board = chess.Board()

        ai_color = board.turn

        if board.fullmove_number == 1:
            if random.randrange(0, 1000) <= 10:
                self.opening_status = Opening
                self.opening_type = random.choice(
                    list(white_player_openings.values()) if ai_color == WHITE else
                    list(black_player_openings.values())
                )

                print(self.opening_type)

        if self.opening_status == Opening:
            return self._get_opening_move(board)

        else:
            return self._get_worst_move(board)

    def close(self):
        self.engine.kill()


# Openings starting from white
# Ignore odd indices, starting from 0
# So for example play f3 then g4 for fools, ignore black's moves
white_player_openings = {
    # 'fools': 'f3 e5 g4 Qh4',
    # 'reverse scholars': 'a4 e5 e4 Bc5 Nc3 Qh4 Nf3 Qxf2',
    # 'stupid f3': 'f3 e5 Kf2 d5 Ke3',
    # 'rook blunder': 'a4 e5 Ra3 Bxa3',

    'fools': 'f2f3 e7e5 g2g4 d8h4',
    'reverse scholars': 'a2a4 e7e5 e2e4 f8c5 b1c3 d8h4 g1f3 h4f2',
    'stupid f3': 'f2f3 e7e5 e1f2 d2d5 f2e3',
    'rook blunder': 'a2a4 e7e5 a1a3 f8a3',
}

# Same but starting with black
# Ignore even indices, starting from 0
# So for example play f6 then g5 for fools, ignore white's moves
black_player_openings = {
    # 'scholars': 'e4 e5 Bc4 Nc6 Qh5 Nf6 Qxf7',
    # 'rook blunder': 'Nf3 h5 d3 Rh6 Bxh6',
    # 'stupid f3 reverse': 'Nf3 f6 e4 Kf7 d4 Ke6',
    # 'reverse fools': 'Nc3 f6 e4 g5 Qh5'

    'scholars': 'e2e4 e7e5 f1c4 b8c6 d1h5 g8f6 h5f7',
    'rook blunder': 'g1f3 h7h5 d2d3 h8h6 c1h6',
    'stupid f3 reverse': 'g1f3 f7f6 e2e4 e8f7 d2d4 f7e6',
    'reverse fools': 'b1c3 f7f6 e2e4 g7g5 d1h5'
}


def main():
    wf = WorstFish()

    board = chess.Board()
    while not board.is_game_over():
        print(str(board))
        print('Turn: %s' % ('White' if board.turn else 'Black'))
        print()

        if board.turn:
            bad_move = wf.get_move(board)
        else:
            bad_move = chess.Move.from_uci(input())
        if bad_move in board.legal_moves:
            board.push(bad_move)
        else:
            print("Invalid move")
            continue

        print("%s plays %s" % ('White' if not board.turn else 'Black', bad_move))


    print(board)
    print(board.result())


if __name__ == '__main__':
    # asyncio.run(main())
    main()
