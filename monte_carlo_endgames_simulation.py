import chess
import chess.engine
import random
from tqdm import tqdm

NUM_SIMULATIONS = 1000
MAX_MOVES = 200  # Limite para evitar jogos infinitos

ENGINE_PATH = "stockfish.exe"  # Ajuste para o caminho do seu engine

def setup_king_rook_vs_king():
    board = chess.Board(None)  # Tabuleiro vazio
    # Colocar as peças nas posições iniciais do final
    board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
    board.set_piece_at(chess.A1, chess.Piece(chess.ROOK, chess.WHITE))
    board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))
    board.turn = chess.WHITE
    return board

def simulate_random_game(board, engine):
    moves_played = 0
    while not board.is_game_over() and moves_played < MAX_MOVES:
        legal_moves = list(board.legal_moves)
        if not legal_moves:
            break
        move = random.choice(legal_moves)
        board.push(move)
        moves_played += 1
    # Retorna resultado: "1-0", "0-1", "1/2-1/2" ou '*' (em andamento)
    return board.result()

def run_simulations_for_position(board_setup_func, name, engine):
    results = {"1-0": 0, "0-1": 0, "1/2-1/2": 0, "invalid": 0}

    for _ in tqdm(range(NUM_SIMULATIONS), desc=f"Simulating {name}"):
        board = board_setup_func()
        result = simulate_random_game(board, engine)
        if result not in results:
            # Resultado inesperado ou partida não terminada
            results["invalid"] += 1
        else:
            results[result] += 1

    print(f"\n=== Resultados para {name} ===")
    total = sum(results.values())
    for key, val in results.items():
        print(f"{key}: {val} ({val / total:.2%})")

def main():
    # Abre o engine (não utilizado neste exemplo, mas deixo aberto para caso queira usar avaliação)
    engine = None
    try:
        engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)
    except Exception as e:
        print(f"Não foi possível abrir o engine: {e}")

    run_simulations_for_position(setup_king_rook_vs_king, "Rei + Torre vs Rei", engine)

    if engine:
        engine.quit()

if __name__ == "__main__":
    main()
