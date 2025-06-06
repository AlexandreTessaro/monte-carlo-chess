import chess
import random
from tqdm import tqdm
import pandas as pd

def simulate_defense_game(opening_moves, defense_moves, max_moves=100):
    board = chess.Board()

    # Executa os movimentos da abertura
    for move_uci in opening_moves:
        board.push_uci(move_uci)

    # Executa os movimentos da defesa
    for move_uci in defense_moves:
        board.push_uci(move_uci)

    moves_played = 0
    while not board.is_game_over() and moves_played < max_moves:
        moves = list(board.legal_moves)
        if not moves:
            break
        move = random.choice(moves)
        board.push(move)
        moves_played += 1

    result = board.result()  # Pode ser '1-0', '0-1', '1/2-1/2' ou '*'

    if result == '*':  # Jogo não terminou dentro do limite
        return 'invalid'
    return result

def run_simulation(defense_name, opening_moves, defense_moves, num_simulations=10000, max_moves=100):
    results = {'1-0': 0, '0-1': 0, '1/2-1/2': 0, 'invalid': 0}

    for _ in tqdm(range(num_simulations), desc=f"Simulating {defense_name}"):
        res = simulate_defense_game(opening_moves, defense_moves, max_moves)
        results[res] += 1

    valid_games = num_simulations - results['invalid']
    white_win_rate = results['1-0'] / valid_games if valid_games > 0 else 0
    black_win_rate = results['0-1'] / valid_games if valid_games > 0 else 0
    draw_rate = results['1/2-1/2'] / valid_games if valid_games > 0 else 0

    return {
        'defense': defense_name,
        '1-0': results['1-0'],
        '0-1': results['0-1'],
        '1/2-1/2': results['1/2-1/2'],
        'invalid': results['invalid'],
        'white_win_rate': white_win_rate,
        'black_win_rate': black_win_rate,
        'draw_rate': draw_rate,
    }

if __name__ == "__main__":
    # Definições dos movimentos em notação UCI para abrir + defesa
    # Exemplos simplificados; você pode adaptar para sequências maiores
    sicilian_opening = ["e2e4", "c7c5"]
    french_opening = ["e2e4", "e7e6"]
    caro_kann_opening = ["e2e4", "c7c6"]

    defenses = [
        ("Sicilian Defense", ["e2e4"], ["c7c5"]),
        ("French Defense", ["e2e4"], ["e7e6"]),
        ("Caro-Kann Defense", ["e2e4"], ["c7c6"]),
    ]

    num_simulations = 10000
    max_moves = 1000

    results_list = []
    for defense_name, opening_moves, defense_moves in defenses:
        result = run_simulation(defense_name, opening_moves, defense_moves, num_simulations, max_moves)
        results_list.append(result)

    df_results = pd.DataFrame(results_list)
    print("\n=== Resultados das Simulações ===")
    print(df_results)
