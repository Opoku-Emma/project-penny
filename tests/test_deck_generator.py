from src import datagen as generate_decks


def test_datagen(generate_data: bool = False, num_simulations: int = 0):

    if generate_data:
        print('Making deck generator object')
        deck_obj = generate_decks.DeckGenerator()
        print('Making decks')
        # add option to add additional data
        deck_obj.make_decks(100, 52)

        print('Saving decks')
        deck_obj.save_deck()
    else:
        print('Using old data')
