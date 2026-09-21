import numpy as np

from src.paths import PATH_DATA_RAW_DECKS
import src.generate_seed as g_seed


class DeckGenerator:
    """Utility class to create and save deck of cards"""

    def __init__(self) -> None:
        self.seed_logger = g_seed.SeedGenerator()
        self.PATH_DECKS = PATH_DATA_RAW_DECKS
        self.current_seed = self.seed_logger.seed
        # this will be used to check if a deck has been
        # generated. if previous and current are the same,
        # an error will pop up to first make a deck
        self.previous_seed = self.current_seed

    def make_decks(self, num_sims: int, num_cards: int) -> np.ndarray:
        """Generate a deck of cards with size (num_decks, num_cards).
        Args:
            num_sims (int): number of simulations (or decks)
            num_cards (int): number of cards per deck
        Returns:
            np.ndarray: (num_sims x num_cards) shaped array"""

        # set seed
        self.current_seed = self.seed_logger.get_next_seed()
        rng = np.random.default_rng(self.current_seed)

        tmp_deck = [1] * (num_cards // 2) + [0] * (num_cards // 2)
        tmp_deck = tmp_deck * num_sims
        tmp_deck = np.array(tmp_deck).reshape((num_sims, num_cards))

        self.current_decks = rng.permuted(tmp_deck, axis=1)

        return self.current_decks

    def save_deck(self) -> None:
        """Store simulated deck as numpy arrays for later retrieval"""
        if self.current_seed == self.previous_seed and (self.previous_seed != 0):
            # print("Generate decks before saving!")
            raise RuntimeError("Generate decks before saving!")

        self.PATH_DECKS.mkdir(parents=True, exist_ok=True)
        num_decks = self.current_decks.shape[0]
        num_cards = self.current_decks.shape[1]

        # i am going to determine how many simulations are saved per file
        MAX_SIMS = 1000000

        whole, decimal = divmod(self.current_decks.shape[0], MAX_SIMS)
        print(whole, decimal)

        #put this here so that no errors are triggered
        part = 0
        for part in range(whole):

            filename = (
                self.PATH_DECKS
                / f"decks_{num_decks}x{num_cards}_part{part}_seed_{self.current_seed}"
            )
            np.save(filename, self.current_decks[part*MAX_SIMS: part*MAX_SIMS+MAX_SIMS])

        if decimal != 0:
            print(decimal)
            filename = (
                self.PATH_DECKS
                / f"decks_{num_decks}x{num_cards}_part_{part+1}_seed_{self.current_seed}"
            )
            np.save(filename, self.current_decks[part*MAX_SIMS: part*MAX_SIMS+decimal])

        print()
        self.seed_logger.save_seed_info()
        return
