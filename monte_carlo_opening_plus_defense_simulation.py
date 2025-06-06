import chess
import chess.engine
import random
import pandas as pd
from tqdm import tqdm

# Configurações
SIMULATIONS_PER_OPENING = 10000
MIN_MOVES_VALID = 10  # mínimo de lances para partida válida
ENGINE_PATH = "stockfish"  # caminho para o motor Stockfish (ajuste se necessário)
TIME_LIMIT = 0.01  # tempo por jogada (em segundos)

# Aberturas + defesas para simular
OPENING_PLUS_DEFENSES = {
    "Sicilian Defense": ["e4", "c5"],
    "French Defense": ["e4", "e6"],
    "Caro-Kann Defense": ["e4", "c6"],
    "Ruy Lopez": ["e4", "e5", "Nf3", "Nc6", "Bb5"]
}

# Inicializa motor de xadrez
engine = chess.engine.SimpleEngine.popen_uci(ENGINE_PATH)

def simulate_game(moves):
    """
    Simula uma partida começando com uma sequência inicial de movimentos (abertura + defesa).
    Retorna resultado, número de lances e flag se a partida foi inválida.
    """
    board = chess.Board()

    # Aplica os movimentos iniciais da abertura + defesa
    try:
        for move_san in moves:
            move = board.parse_san(move_san)
            board.push(move)
    except Exception:
        # Movimento inválido na abertura inicial (não deve acontecer)
        return None, 0, True

    move_count = len(moves)
    invalid = False

    while not board.is_game_over(claim_draw=True):
        result = engine.play(board, chess.engine.Limit(time=TIME_LIMIT))
        board.push(result.move)
        move_count += 1

        # Para evitar partidas muito longas, limite de 100 lances
        if move_count > 100:
            break

    # Verifica se a partida foi válida
    if move_count < MIN_MOVES_VALID:
        invalid = True

    # Verifica resultado final
    outcome = board.outcome()
    if outcome is None:
        # Partida terminou sem resultado claro (ex: limite de lances)
        invalid = True
        result = None
    else:
        result = outcome.result()

    return result, move_count, invalid

def main():
    results = []

    for opening_name, moves in OPENING_PLUS_DEFENSES.items():
        print(f"Simulating {opening_name}...")
        white_wins = 0
        black_wins = 0
        draws = 0
        invalids = 0

        for _ in tqdm(range(SIMULATIONS_PER_OPENING)):
            result, move_count, invalid = simulate_game(moves)

            if invalid:
                invalids += 1
                continue

            if result == "1-0":
                white_wins += 1
            elif result == "0-1":
                black_wins += 1
            elif result == "1/2-1/2":
                draws += 1

        total_valid = SIMULATIONS_PER_OPENING - invalids
        results.append({
            "opening_plus_defense": opening_name,
            "1-0": white_wins,
            "0-1": black_wins,
            "1/2-1/2": draws,
            "invalid": invalids,
            "white_win_rate": white_wins / SIMULATIONS_PER_OPENING,
            "black_win_rate": black_wins / SIMULATIONS_PER_OPENING,
            "draw_rate": draws / SIMULATIONS_PER_OPENING,
            "valid_games": total_valid
        })

    df = pd.DataFrame(results)
    print("\n=== Resultados das Simulações ===")
    print(df)

if __name__ == "__main__":
    main()
    engine.quit()
