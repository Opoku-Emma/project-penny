import numpy as np

from src.paths import PATH_DATA_RAW
import src.generate_seed as g_seed


class DeckGenerator:

    def __init__(self) -> None:
        self.seed_logger = g_seed.SeedGenerator()
        self.PATH_DECKS = PATH_DATA_RAW / "decks"
        self.current_seed = None

    def make_decks(self, num_decks: int, num_cards: int) -> np.ndarray:
        '''Generate a deck of cards with size (num_decks, num_cards)'''

        # set seed
        self.current_seed = self.seed_logger.get_next_seed()
        rng = np.random.default_rng(self.current_seed)

        self.current_decks = rng.integers(low=0, high=2, size=(num_decks, num_cards))

        return self.current_decks

    def save_deck(self) -> None:

        if self.current_seed == None:
            print("Generate decks before saving!")

        self.PATH_DECKS.mkdir(parents=True, exist_ok=True)
        n_decks = self.current_decks.shape[0]
        n_cards = self.current_decks.shape[1]

        filename = (
            self.PATH_DECKS / f"decks_{n_decks}x{n_cards}_seed_{self.current_seed}"
        )
        np.save(filename, self.current_decks)
        print()
        self.seed_logger.save_seed_info()
        return
