from src.dataproc import make_player_pairs, simulate_game
import src.datavis as datavis
from datetime import datetime as dt


# We can either use argparse or just take user
# input on the fly
def main():
    additional_simulation = 1
    print("Hello from project-penny!\n")

    if additional_simulation != 0:
        print("Simulating data")
        possible_combinations, card_combination = make_player_pairs(3)
        simulate_game(possible_combinations, card_combination)
    else:
        print("No additional data specified! Using old data")

    print("Generating Charts")
    datavis.datavis()
    print("Done")

    return


if __name__ == "__main__":
    main()
