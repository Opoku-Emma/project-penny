from src import datagen as generate_decks


def test_datagen(generate_data: bool = True, num_simulations: int =10):

    if generate_data:
        print('Making deck generator object')
        deck_obj = generate_decks.DeckGenerator()
        print('Making decks')
        # add option to add additional data
        for _ in range(num_simulations):
            deck_obj.make_decks(10_000, 52)
            print('Saving decks')
            deck_obj.save_deck()
    else:
        print('Using old data')
