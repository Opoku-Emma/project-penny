from src import datavis
from src.dataproc import make_player_pairs, simulate_game
import src.datavis as datavis
from datetime import datetime as dt


def main():

    # Number of new shuffled decks to generate.
    additional_simulation = 1_000_000

    print("Hello from project-penny!\n")

    if additional_simulation != 0:

        print(f"Simulating {additional_simulation:,} decks")

        # Record the time immediately before starting the simulation.
        start_time = dt.now()
        print(f"Start time: {start_time:%Y-%m-%d %H:%M:%S}\n")

        # Generate all possible player-vs-player color combinations.
        possible_combinations, card_combination = make_player_pairs(3)

        # Generate the requested number of additional decks and
        # simulate every player combination against the decks.
        simulate_game(
            possible_combinations,
            card_combination,
            additional_simulation
        )

        # Stop the simulation timer before generating/displaying figures.
        end_time = dt.now()
        elapsed_time = end_time - start_time

        print("\nSimulation completed")
        print(f"End time:     {end_time:%Y-%m-%d %H:%M:%S}")
        print(f"Runtime:      {elapsed_time}")

    else:
        print("No additional data specified! Using old data")

    # Figure generation occurs after simulation timing is complete.
    # plt.show() may block execution until the figure window is closed,
    # but this will no longer affect the reported simulation runtime.
    print("\nGenerating Charts")
    datavis.datavis()

    print("Done")



if __name__ == "__main__":
    main()