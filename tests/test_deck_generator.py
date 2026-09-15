from src import generate_decks as generate_decks

deck_obj = generate_decks.DeckGenerator()

c_decks = deck_obj.make_decks(2, 52)
print(c_decks)

deck_obj.save_deck()