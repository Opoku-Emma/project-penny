#
# Potential Issues:
#
# Too much logic in main function?
#
# Doesn't match suggested structure of:
# - datagen
# - dataproc
# - datavis
# 
# Option "1 - Start a new simulation" doesn't work
# because simulate_game always picks up 
# existing data.
# 
# Need to limit the number of simulations
# to prevent large file sizes?


from src.dataproc import make_player_pairs, simulate_game
import src.datavis as datavis
from datetime import datetime as dt

def get_simulation_count(prompt: str) -> int:
    """Prompt the user for a positive number of simulations."""

    while True:
        try:
            number = int(input(prompt))

            if number > 0:
                return number

            print("Please enter a number greater than 0.")

        except ValueError:
            print("Please enter a whole number.")


def main() -> None:
    """Run the Penny's Game simulation pipeline."""

    print("\nPenny's Game Simulation")
    print("-----------------------")
    print("1 - Start a new simulation")
    print("2 - Add simulations to existing data")
    print("3 - Generate charts from existing data")
    print("4 - Exit")

    choice = input("\nEnter your choice: ").strip()

    # Start a completely new simulation
    if choice == "1":

        number_simulations = get_simulation_count(
            "How many simulations would you like to run? "
        )

        print(
            f"\nStarting a new simulation with "
            f"{number_simulations:,} decks..."
        )

        possible_combinations, card_combination = make_player_pairs(3)

        simulate_game(
            possible_combinations,
            card_combination,
            number_simulations
        )

    # Add simulations to the existing results
    if choice == "2":

        additional_simulations = get_simulation_count(
            "How many additional simulations would you like to run? "
        )

        print(
            f"\nAdding {additional_simulations:,} simulations "
            f"to the existing data..."
        )

        possible_combinations, card_combination = make_player_pairs(3)

        simulate_game(
            possible_combinations,
            card_combination,
            additional_simulations
        )

    # Generate charts only
    if choice == "3":

        print("\nUsing existing simulation data.")

    # Exit
    if choice == "4":

        print("\nExiting.")
        return

    # Check for invalid input
    if choice not in ["1", "2", "3", "4"]:

        print("\nInvalid selection.")
        return

    # Generate charts for choices 1, 2, or 3
    print("\nGenerating charts...")

    datavis.datavis()

    print("Done.")


if __name__ == "__main__":
    main()