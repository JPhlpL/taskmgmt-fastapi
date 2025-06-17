# src/core/logger.py
import logging
from datetime import datetime
import os


def setup_logger():
    logger = logging.getLogger("taskmgmt")
    if logger.handlers:
        return logger

    log_dir = os.path.join(os.path.dirname(__file__), "..", "logs")
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{datetime.now().strftime('%Y-%m-%d')}.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )
    return logger
