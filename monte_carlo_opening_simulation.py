import chess
import random
from tqdm import tqdm
import pandas as pd

MAX_PLIES = 100

OPENINGS = {
    "e4": ["e4"],
    "d4": ["d4"],
    "Sicilian Defense": ["e4", "c5"],
    "Ruy Lopez": ["e4", "e5", "Nf3", "Nc6", "Bb5"]
}

def simulate_random_game(opening_moves):
    board = chess.Board()

    for move in opening_moves:
        try:
            board.push_san(move)
        except:
            return "*"

    plies = 0
    while not board.is_game_over() and plies < MAX_PLIES:
        legal_moves = list(board.legal_moves)
        move = random.choice(legal_moves)
        board.push(move)
        plies += 1

    if board.is_game_over():
        return board.result()
    else:
        return evaluate_material(board)

def evaluate_material(board):
    values = {'P': 1, 'N': 3, 'B': 3, 'R': 5, 'Q': 9}
    white_score = 0
    black_score = 0
    for piece in board.piece_map().values():
        symbol = piece.symbol()
        value = values.get(symbol.upper(), 0)
        if symbol.isupper():
            white_score += value
        else:
            black_score += value

    if white_score > black_score:
        return "1-0"
    elif black_score > white_score:
        return "0-1"
    else:
        return "1/2-1/2"

def run_simulations(num_simulations):
    results = []

    print(f"\nSimulating {num_simulations} games per opening:")
    for name, moves in tqdm(OPENINGS.items()):
        outcomes = {"1-0": 0, "0-1": 0, "1/2-1/2": 0, "*": 0}

        for _ in range(num_simulations):
            result = simulate_random_game(moves)
            outcomes[result] += 1

        results.append({
            "opening": name,
            "num_simulations": num_simulations,
            "1-0": outcomes["1-0"],
            "0-1": outcomes["0-1"],
            "1/2-1/2": outcomes["1/2-1/2"],
            "invalid": outcomes["*"],
            "white_win_rate": outcomes["1-0"] / num_simulations,
            "black_win_rate": outcomes["0-1"] / num_simulations,
            "draw_rate": outcomes["1/2-1/2"] / num_simulations
        })

    return pd.DataFrame(results)

if __name__ == "__main__":
    all_results = pd.concat([
        run_simulations(1000),
        run_simulations(5000),
        run_simulations(10000)
    ], ignore_index=True)

    print("\n=== Resultados Comparativos ===")
    print(all_results)

    # Exportar para CSV (opcional)
    all_results.to_csv("resultados_aberturas_monte_carlo.csv", index=False)
