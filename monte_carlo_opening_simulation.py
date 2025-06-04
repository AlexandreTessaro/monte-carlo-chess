import chess
import random
import pandas as pd
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor, as_completed

# === CONFIGURAÇÕES ===
N_SIMULATIONS = 10_000
MAX_PLIES = 40

OPENINGS = {
    "e4": ["e4"],
    "d4": ["d4"],
    "Sicilian Defense": ["e4", "c5"],
    "Ruy Lopez": ["e4", "e5", "Nf3", "Nc6", "Bb5"],
}

# === FUNÇÃO DE SIMULAÇÃO INDIVIDUAL ===
def simulate_one_game(opening_moves):
    board = chess.Board()
    try:
        for move in opening_moves:
            board.push_san(move)
    except:
        return "invalid"

    for _ in range(MAX_PLIES):
        if board.is_game_over():
            break
        move = random.choice(list(board.legal_moves))
        board.push(move)

    result = board.result()
    if result not in ["1-0", "0-1", "1/2-1/2"]:
        return "invalid"
    return result

# === FUNÇÃO PARA RODAR SIMULAÇÕES PARA UMA ABERTURA ===
def simulate_opening(opening_name_and_moves):
    opening_name, moves = opening_name_and_moves
    outcomes = {"1-0": 0, "0-1": 0, "1/2-1/2": 0, "invalid": 0}
    for _ in range(N_SIMULATIONS):
        result = simulate_one_game(moves)
        outcomes[result] += 1
    outcomes["opening"] = opening_name
    return outcomes

# === EXECUTAR EM PARALELO ===
if __name__ == "__main__":
    with ProcessPoolExecutor() as executor:
        futures = [
            executor.submit(simulate_opening, (name, moves))
            for name, moves in OPENINGS.items()
        ]

        results = []
        for future in tqdm(as_completed(futures), total=len(OPENINGS), desc="Simulating openings"):
            results.append(future.result())

    # === RESULTADOS EM TABELA ===
    df_results = pd.DataFrame(results)
    df_results = df_results[["opening", "1-0", "0-1", "1/2-1/2", "invalid"]]
    df_results["white_win_rate"] = df_results["1-0"] / N_SIMULATIONS
    df_results["black_win_rate"] = df_results["0-1"] / N_SIMULATIONS
    df_results["draw_rate"] = df_results["1/2-1/2"] / N_SIMULATIONS

    print("\n=== Resultados das Simulações ===")
    print(df_results.round(4))

    # (Opcional) salvar como CSV
    df_results.to_csv("opening_simulation_results.csv", index=False)
