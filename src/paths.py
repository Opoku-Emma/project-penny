from pathlib import Path

PROJECT_ROOT = Path(__file__).absolute().parents[1]

PATH_DATA = PROJECT_ROOT / 'data'
PATH_DATA_RAW = PATH_DATA / 'raw'
PATH_DATA_RAW_DECKS = PATH_DATA_RAW / 'decks'
PATH_DATA_CLEAN = PATH_DATA / 'clean'
PATH_LOGS = PROJECT_ROOT / 'logs'

PATH_FIGURES = PROJECT_ROOT / 'figures'
PATH_FIGURES_ARCHIVE = PATH_FIGURES / 'archive'

def make_project_folders():
    '''
    Create the folders used by this project if they do not already exist.
    '''
    PATH_DATA.mkdir(parents=True, exist_ok=True)
    PATH_DATA_RAW.mkdir(parents=True, exist_ok=True)
    PATH_DATA_CLEAN.mkdir(parents=True, exist_ok=True)
    PATH_DATA_RAW_DECKS.mkdir(parents=True, exist_ok=True)
    PATH_LOGS.mkdir(parents=True, exist_ok=True)
    PATH_FIGURES.mkdir(parents=True, exist_ok=True)
    PATH_FIGURES_ARCHIVE.mkdir(parents=True, exist_ok=True)
