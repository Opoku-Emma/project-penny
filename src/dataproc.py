from pathlib import Path
import numpy as np
import pandas as pd
from typing import Union

from src.paths import PATH_DATA_RAW_DECKS, PATH_DATA_CLEAN


def read_raw_data(data_path: Path) -> np.ndarray:

    # list all .npy files in data_path
    data_paths = data_path.glob("*.npy")

    # convert to list so that we can check if empty
    # while keeping all the Path objects
    data_paths = list(data_paths)
    print(f"Found {len(data_paths)} data arrays")
    data_stack = []

    for file_path in data_paths:
        tmp = np.load(file_path)
        data_stack.append(tmp)

    # stack all data row-wise. synonymous to concatenating/stitching
    # the data on top of each other
    data_stack = np.vstack(data_stack)

    return data_stack


def convert_numpy_str(data_stack: np.ndarray) -> np.ndarray:
    """Convert data from integers to string type"""
    return data_stack.astype("str")


# def convert_nums_to_chr(data_stack: np.ndarray) -> np.ndarray:
#     '''Convert  '''
#     tmp = data_stack.copy()
#     nums_to_chr_dict = {"0": "R", "1": "B"}
#     tmp = [nums_to_chr_dict[num] for num in tmp]
#     return np.array(tmp)


def convert_chr_to_nums(data_stack: np.ndarray) -> np.ndarray:
    """Convert player card sequence (R, B) to integer strings"""
    tmp = data_stack.copy()
    nums_to_chr_dict = {"R": "0", "B": "1"}
    tmp = [nums_to_chr_dict[num] for num in tmp]
    return np.array(tmp)


def make_player_pairs(num_cards_per_player: int = 3) -> tuple:
    '''Generate possible pairs of player1 against player2'''
    # possible_combinations = 2 ** num_cards_per_player
    card_combination = ["RRR", "RRB", "RBR", "BRR", "BBB", "BBR", "BRB", "RBB"]
    possible_combinations = []

    # construct a pairing, while excluding duplicates
    for i, row in enumerate(card_combination):
        for j, col in enumerate(card_combination):
            if i != j:
                possible_combinations.append(np.array((row, col)))

    return possible_combinations, card_combination


def simulate_game(possible_combinations: list, card_combination: list) -> ...:
    combo_size = len(card_combination)
    results_df = pd.DataFrame(
        np.zeros((combo_size, combo_size)),
        columns=card_combination,
        index=card_combination,
        dtype=object
    )

    data = read_raw_data(PATH_DATA_RAW_DECKS)
    converted_data = convert_numpy_str(data)
    for combo in possible_combinations:
        player1_overall, player2_overall, h_n_ties, ron_ties = play_game(
            converted_data, combo[0], combo[1]
        )
        print('Player1 overall', player1_overall)

        results_df.loc[combo[0], combo[1]] = (player1_overall[0],  h_n_ties)
    results_df.to_csv(PATH_DATA_CLEAN/'datavis_test_input.csv', sep=',')

    return results_df


# TODO: fix linting of arguments
def play_game(data_stack: np.ndarray, player1, player2) -> tuple:
    """Simulate game by playing and counting wins, ties"""

    player1 = "".join(convert_chr_to_nums(player1))
    player2 = "".join(convert_chr_to_nums(player2))

    # original, ron's version
    player1_overall = [0, 0]
    player2_overall = [0, 0]
    h_n_ties = 0
    ron_ties = 0

    # loop through each array
    for i, simulation in enumerate(data_stack):
        # print(f"-- Starting Simulation {i+1} --")
        simulation = "".join(simulation)
        # use prev for counting and shifting
        prev = 0

        player1_tmp_result = [0, 0]
        player2_tmp_result = [0, 0]

        while (prev + 3) <= len(simulation):
            play = simulation[prev : prev + 3]

            # if a player wins, let's update their score
            # and slice all cards up to that point off
            # this way we solve both the original problem
            # and Ron's version

            if play == player1:
                player1_tmp_result[0] += 1
                cards_won = len(simulation[: prev + 3])
                player1_tmp_result[1] += cards_won
                simulation = simulation[cards_won:]
                # print(f"\tCards won {cards_won} | ", end="")

                # reset counter
                prev = 0
                continue

            elif play == player2:
                player2_tmp_result[0] += 1
                cards_won = len(simulation[: prev + 3])
                player2_tmp_result[1] += cards_won
                simulation = simulation[cards_won:]
                # print(f"\tCards won {cards_won} | ", end="")

                # reset counter
                prev = 0
                continue

            prev += 1
            # print(f"\tRunning total: {prev}")

        if player1_tmp_result[0] == player2_tmp_result[0]:
            h_n_ties += 1
        elif player1_tmp_result[0] > player2_tmp_result[0]:
            player1_overall[0] += 1
        else:
            player2_overall[0] += 1

        if player1_tmp_result[1] == player2_tmp_result[1]:
            ron_ties += 1
        elif player1_tmp_result[1] > player2_tmp_result[1]:
            player1_overall[1] += 1
        else:
            player2_overall[1] += 1

    # print(
    #     f"End of {len(data_stack)} simulations.\n"
    #     f"Humble-N Results: Player1 {player1_overall[0]} | "
    #     f"Player2 {player2_overall[0]} | Ties {h_n_ties}\n"
    #     f"Ron's Results:    Player1 {player1_overall[1]} | "
    #     f"Player2 {player2_overall[1]} | Ties {ron_ties}"
    # )
    return player1_overall, player2_overall, h_n_ties, ron_ties
