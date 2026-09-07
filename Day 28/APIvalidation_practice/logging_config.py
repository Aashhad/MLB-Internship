import logging
from pathlib import Path


# BASE DIRECTORY

BASE_DIR = Path(__file__).resolve().parent


# LOG DIRECTORY

LOG_DIR = BASE_DIR / "logs"

LOG_DIR.mkdir(
    parents=True,
    exist_ok=True
)


# LOG FILE

LOG_FILE = LOG_DIR / "app.log"


# LOGGING SETUP

def setup_logging():

    logging.basicConfig(
        level=logging.INFO,

        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),

        handlers=[
            logging.FileHandler(
                LOG_FILE,
                encoding="utf-8"
            ),

            logging.StreamHandler()
        ]
    )