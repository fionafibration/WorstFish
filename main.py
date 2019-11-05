import chess
import chess.engine
import asyncio


class WorstFish:

    def __init__(self):
        self.transport, self.engine = await chess.engine.popen_uci(
            './stockfish-10-win/Windows/stockfish_10_x64_bmi2.exe'
        )

    def get_move(self, board=None):
        if board is None:
            board = chess.Board()

        ai_color = board.turn

        for move in board.legal_moves:
            pass


Done = 'done'

Wildcard = 'wildcard'


class AwfulOpening:

    def __init__(self, opening_tree):
        self.opening_tree = opening_tree
        self.moves_played = []

    def play(self):
        self.moves_played.append(self.opening_tree[0])
        return self.opening_tree[0]


# Openings starting from white
# Ignore odd indices, starting from 0
# So for example play f3 then g4 for fools, ignore black's moves
white_player_openings = {
    'fools': 'f3 e5 g4 Qh4',
    'reverse scholars': 'a4 e5 e4 Bc5 Nc3 Qh4 Nf3 Qxf2',
    'stupid f3': 'f3 e5 Kf2 d5 Ke3',
    'rook blunder': 'a4 e5 Ra3 Bxa3',
}


# Same but starting with black
# Ignore even indices, starting from 0
# So for example play f6 then g5 for fools, ignore white's moves
black_player_openings = {
    'scholars': 'e4 e5 Bc4 Nc6 Qh5 Nf6 Qxf7',
    'rook blunder': 'Nf3 h5 d3 Rh6 Bxh6',
    'stupid f3 reverse': 'Nf3 f6 e4 Kf7 d4 Ke6',
    'reverse fools': 'Nc3 f6 e4 g5 Qh5'
}