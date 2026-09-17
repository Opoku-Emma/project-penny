from src.dataproc import make_player_pairs, simulate_game


# We can either use argparse or just take user
# input on the fly
def main():
    print("Hello from project-penny!\n")

    print("Simulating game")
    possible_combinations, card_combination = make_player_pairs(3)
    simulate_game(possible_combinations, card_combination)

    return


if __name__ == "__main__":
    main()
