from src.dataproc import read_raw_data, convert_numpy_str, make_player_pairs, simulate_game
from src.paths import PATH_DATA_RAW_DECKS


def test_process_data():
    data = read_raw_data(PATH_DATA_RAW_DECKS)
    return


def test_convert_numpy_to_str():
    data = read_raw_data(PATH_DATA_RAW_DECKS)
    # converted_data = convert_numpy_str(data)
    return


def test_simulate_game():
    # data = read_raw_data(PATH_DATA_RAW_DECKS)
    # print("Converting data")
    # converted_data = convert_numpy_str(data)
    print("Simulating game")
    possible_combinations, card_combination = make_player_pairs(3)
    results = simulate_game(possible_combinations, card_combination)

    return


if __name__ == "__main__":
    # data = test_process_data()
    test_simulate_game()
