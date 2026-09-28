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
        """Store simulated decks as numpy arrays, split into chunks of MAX_SIMS."""
        if self.current_seed == self.previous_seed and self.previous_seed != 0:
            raise RuntimeError("Generate decks before saving!")

        self.PATH_DECKS.mkdir(parents=True, exist_ok=True)
        num_decks, num_cards = self.current_decks.shape[:2]
        MAX_SIMS = 100_000

        for part, start in enumerate(range(0, num_decks, MAX_SIMS)):
            filename = (
                self.PATH_DECKS
                / f"decks_{num_decks}x{num_cards}_part_{part:02d}_seed_{self.current_seed}.npy"
            )
            np.save(filename, self.current_decks[start : start + MAX_SIMS])

        self.seed_logger.save_seed_info()