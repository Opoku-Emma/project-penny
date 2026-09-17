from src.dataproc import make_player_pairs, simulate_game, read_raw_data
from src.paths import PATH_DATA_RAW_DECKS

def test_simulate_game():
    print("Checking if data exists")
    _, num_files = read_raw_data(PATH_DATA_RAW_DECKS)

    if num_files == 0:
        print("No data present!\nGenerating new data")

    print("Simulating game")
    possible_combinations, card_combination = make_player_pairs(3)
    simulate_game(possible_combinations, card_combination)

    return


if __name__ == "__main__":
    test_simulate_game()
