from src import datagen as generate_decks

print('Making deck generator object')
deck_obj = generate_decks.DeckGenerator()
print('Making decks')
c_decks = deck_obj.make_decks(2, 52)

print('Saving decks')
deck_obj.save_deck()