from src.dataproc import make_player_pairs, simulate_game


def test_simulate_game():
    print("Simulating game")
    possible_combinations, card_combination = make_player_pairs(3)
    results = simulate_game(possible_combinations, card_combination)

    return


if __name__ == "__main__":
    test_simulate_game()
