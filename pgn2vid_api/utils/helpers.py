import chess.pgn
import io

def is_pgn_valid(content):
    pgn = io.StringIO(content)
    game = chess.pgn.read_game(pgn)
    return game is not None
        