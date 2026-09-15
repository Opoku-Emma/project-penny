import numpy as np
import json
from datetime import datetime as dt
from pathlib import Path

from src.paths import (
    PATH_LOGS,
    make_project_folders,
)

SEED_PATH = PATH_LOGS / "seed_log.json"


class SeedGenerator:
    """
    This class is generates seed numbers and stores them
    for later retrieval
    """

    def __init__(self) -> None:
        self.seed = 0

    def get_next_seed(self) -> int:
        """Generate next seed value"""

        if SEED_PATH.exists():
            with SEED_PATH.open("r") as inFile:
                seed_log = json.load(inFile)
            self.seed = seed_log["seed"] + 1
        else:
            print(f"Seed path doesn't exist. Starting with {self.seed}")

        return self.seed

    def save_seed_info(self) -> None:
        """Save seed info to file for late retrieval"""
        seed_log = {"seed": self.seed, "seed_time": str(dt.now()), "used": True}
        with SEED_PATH.open("w") as outFile:
            json.dump(seed_log, outFile)
        return


# def main():
#     make_project_folders()

#     seed_generator = SeedGenerator()
#     seed_generator.get_next_seed()

#     return


# if __name__ == "__main__":
#     main()
