from itertools import combinations, product
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

from src import datagen
from src.paths import PATH_DATA_CLEAN, PATH_DATA_RAW_DECKS


def read_raw_data(data_path: Path) -> tuple:
    """Get file paths for all numpy data in the data_path
    Args:
        data_path (Path): path to raw deck simulation numpy records
    Returns:
        tuple: list[numpy_paths], number of numpy files"""
    # list all .npy files in data_path
    data_paths = data_path.glob("*.npy")

    # convert to list so that we can check if empty
    # while keeping all the Path objects
    data_paths = list(data_paths)
    print(f"Found {len(data_paths)} data arrays")

    return data_paths, len(data_paths)


def concat_raw_data(data_paths: list[Path]) -> np.ndarray:
    """Load data from the list of Paths provided. Concat into one big stack
    Returns:
        np.ndarray: numpy arrays from raw simulation stacked vertically"""

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


def convert_chr_to_nums(data_stack: np.ndarray) -> np.ndarray:
    """Convert player card sequence (R, B) to integer strings"""
    tmp = data_stack.copy()
    nums_to_chr_dict = {"R": "0", "B": "1"}
    tmp = [nums_to_chr_dict[num] for num in tmp]
    return np.array(tmp)


def make_player_pairs(num_cards_per_player: int = 3) -> tuple:
    """Generate possible pairs of player1 against player2"""

    # construct a pairing, while excluding duplicates
    card_combination = ["".join(p) for p in product("RB", repeat=num_cards_per_player)]
    possible_combinations = list(combinations(card_combination, 2))
    # save for later use by visualization
    possible_combinations = np.array(possible_combinations)
    np.save(PATH_DATA_CLEAN / 'possible_pairs', card_combination)
    return possible_combinations, card_combination


def calculate_probabilities(score: int, total_simulations: int) -> int:
    return round((score / total_simulations) * 100, None)


def update_scores(results_dict: dict, combo: list, player_overall:list, total_simulations: int, ron_ties: int, classic_ties: int) -> dict:
    """Update scores after each sequence-by-sequence total simulation

    Args:
        results_dict (dict): this will be written to file for heatmaps
        combo (list): player-vs-player sequence combinations
        player_overall (list): (classic wins, rons wins)
        total_simulations (int): total simulations 
        ron_ties (int): ties scored using ron's versioin
        classic_ties (int): ties scored using classic version

    Returns:
        dict: final output
    """
    results_dict["classic"].loc[combo[0], combo[1]] = calculate_probabilities(player_overall[0], total_simulations)
    results_dict["classic_ties"].loc[combo[0], combo[1]] = calculate_probabilities(classic_ties, total_simulations)
    results_dict["ron"].loc[combo[0], combo[1]] = calculate_probabilities(player_overall[1], total_simulations)
    results_dict["ron_ties"].loc[combo[0], combo[1]] = calculate_probabilities(ron_ties, total_simulations)
    return results_dict


def simulate_game(
    possible_combinations: np.ndarray, card_combination: list, additional_simulations: int = 0
) -> None:
    """Simulate game and store scores to file as numpy arrays
    Args:
        possible_combinations (list): a list of all possible player-vs-player
            combinations
        card_combinations (list): list of all possible 3-pair combinations of R & B
        additional_simulations (int): generate additional deck of cards
            if supplied by user
    """
    combo_size = len(card_combination)

    # lazily make a list of 4 dataframes
    bulk_results = {
        category: pd.DataFrame(
            np.zeros((combo_size, combo_size)),
            columns=card_combination,
            index=card_combination,
            dtype=int
        )
        for category in ["classic", "classic_ties", "ron", "ron_ties"]
    }

    if additional_simulations != 0:  # make more simulations
        print("Generating more data based on user input")
        deck_gen = datagen.DeckGenerator()
        deck_gen.make_decks(additional_simulations, 52)
        deck_gen.save_deck()
    data_paths, _ = read_raw_data(PATH_DATA_RAW_DECKS)
    data = concat_raw_data(data_paths)
    total_simulations = data.shape[0]
    print(total_simulations)

    # save total simulations to file
    np.save(PATH_DATA_CLEAN / 'total_sims.npy', total_simulations)

    converted_data = convert_numpy_str(data)

    # play game for every possible combination
    pbar = tqdm(
        possible_combinations,
        bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}]",
    )
    for combo in pbar:
        pbar.set_description(f"Playing {combo[0]} against {combo[1]}")
        player1_overall, player2_overall, h_n_ties, ron_ties = play_game(
            converted_data, combo[0], combo[1]
        )

        # update player a's results
        bulk_results = update_scores(bulk_results, combo, player1_overall, total_simulations, ron_ties, h_n_ties)

         # player_b's perspective 
        bulk_results = update_scores(bulk_results, combo[::-1], player2_overall, total_simulations, ron_ties, h_n_ties)

    # save each result to .np array
    for key in bulk_results:
        filename = PATH_DATA_CLEAN / f"_{key}"
        np.save(filename, bulk_results[key].to_numpy())
    return total_simulations


def play_game(
    data_stack: np.ndarray, player1: np.ndarray, player2: np.ndarray
) -> tuple:
    """Simulate game by playing and counting wins, ties
    Args:
        data_stack (np.ndarray): num_simulations x 52 shape data array
        player1 (np.ndarray): 3-card sequence for player 1. this is just a one-
            item array.
        player2 (np.ndarray): 3-card sequence for player 1. this is just a one-
            item array.
    Returns:
        np.ndarray: player1_overall [classic, ron's version],
            player2_overall [classic, ron's version],
            classic_ties, ron_ties
    """

    player1 = "".join(convert_chr_to_nums(player1))
    player2 = "".join(convert_chr_to_nums(player2))

    # (0, 0) --> original, ron's version
    player1_overall = [0, 0]
    player2_overall = [0, 0]
    h_n_ties = 0
    ron_ties = 0

    # loop through each array
    for _, simulation in enumerate(data_stack):

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

                # reset counter
                prev = 0
                continue

            elif play == player2:
                player2_tmp_result[0] += 1
                cards_won = len(simulation[: prev + 3])
                player2_tmp_result[1] += cards_won
                simulation = simulation[cards_won:]

                # reset counter
                prev = 0
                continue

            prev += 1

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

    return player1_overall, player2_overall, h_n_ties, ron_ties
