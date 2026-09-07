import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from app.config import LOG_DIR


LOG_FILE = LOG_DIR / "app.log"


def setup_logging():

    logger = logging.getLogger()

    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers
    if logger.handlers:
        return

    # ========================================================
    # FORMAT
    # ========================================================

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | "
        "%(name)s | %(message)s"
    )

    # ========================================================
    # FILE HANDLER
    # ========================================================

    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )

    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    # ========================================================
    # CONSOLE HANDLER
    # ========================================================

    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # ========================================================
    # ADD HANDLERS
    # ========================================================

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)