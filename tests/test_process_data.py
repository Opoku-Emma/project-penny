from src.dataproc import read_raw_data, convert_numpy_str, simulate_game
from src.paths import PATH_DATA_RAW_DECKS


def test_process_data():
    data = read_raw_data(PATH_DATA_RAW_DECKS)
    return


def test_convert_numpy_to_str():
    data = read_raw_data(PATH_DATA_RAW_DECKS)
    converted_data = convert_numpy_str(data)
    return


def test_simulate_game():
    data = read_raw_data(PATH_DATA_RAW_DECKS)
    print("Converting data")
    converted_data = convert_numpy_str(data)
    print("Simulating game")
    simulate_game(converted_data)

    return


if __name__ == "__main__":
    # data = test_process_data()
    test_convert_numpy_to_str()
