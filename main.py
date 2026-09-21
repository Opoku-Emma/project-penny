
from src.dataproc import make_player_pairs, simulate_game
import src.datavis as datavis
from datetime import datetime as dt

def get_simulation_count(prompt: str) -> int:
    """Prompt the user for a positive number of simulations."""

    while True:
        try:
            number = int(input(prompt))

            if number > 0 and number < 1000001:
                return number
            print(f"{number} isn't valid for this")
            print("Please enter a number greater than 0 and less than 1,000,001")


        except ValueError:
            print("Please enter a whole number.")


def main() -> None:
    """Run the Penny's Game simulation pipeline."""

    print("\nPenny's Game Simulation")
    print("-----------------------")
    print("1 - Add simulations to existing data")
    print("2 - Generate charts from existing data")
    print("3 - Exit")

    choice = input("\nEnter your choice: ").strip()

    # Add simulations to the existing results
    if choice == "1":

        additional_simulations = get_simulation_count(
            "How many additional simulations would you like to run? "
        )

        print(
            f"\nAdding {additional_simulations:,} simulations "
            f"to the existing data..."
        )

        possible_combinations, card_combination = make_player_pairs(3)

        # Record the time immediately before starting the simulation.
        start_time = dt.now()
        print(f"Start time: {start_time:%Y-%m-%d %H:%M:%S}\n")

        simulate_game(
            possible_combinations,
            card_combination,
            additional_simulations
        )

        # Stop the simulation timer before generating/displaying figures.
        end_time = dt.now()
        elapsed_time = end_time - start_time

        print("\nSimulation completed")
        print(f"End time:     {end_time:%Y-%m-%d %H:%M:%S}")
        print(f"Runtime:      {elapsed_time}")

    # Generate charts only
    if choice == "2":

        print("\nUsing existing simulation data.")

    # Exit
    if choice == "3":
        print("\nExiting.")
        return

    # Check for invalid input
    if choice not in ["1", "2", "3"]:
        print("\nInvalid selection.")
        return

    # Generate charts for choices 1, or 2
    datavis.datavis()

    print("Done, thank you.")


if __name__ == "__main__":
    main()