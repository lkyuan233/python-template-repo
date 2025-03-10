"""Logger module for logging operations performed."""

import logging
from pathlib import Path

LOG_FILE = Path("operations.log")

# Configure logging only if not already configured
logger = logging.getLogger(__name__)  # ✅ Uses dynamic module name
if not logger.hasHandlers():
    handler = logging.FileHandler(LOG_FILE, mode="a")  # ✅ Append mode (does not overwrite logs)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

class Logger:
    """Logger class to log operations performed."""

    @staticmethod
    def log(message: str) -> None:
        """Log a message to the operations log file."""
        logger.info(message)  # ✅ No need to manually flush logs

