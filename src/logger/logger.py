"""Logger module for logging operations performed."""

import logging
from pathlib import Path

LOG_FILE = Path("operations.log")

# Configure logging only if not already configured
logger = logging.getLogger(__name__)  # Uses dynamic module name
if not logger.hasHandlers():
    handler = logging.FileHandler(LOG_FILE, mode="a")  # Append mode (does not overwrite logs)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    handler.setLevel(logging.INFO)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

class Logger:
    """Logger class to log operations performed."""

    def __init__(self):
        self.log_file = LOG_FILE

    def set_log_file(self, log_file: Path) -> None:
        """Set a custom log file."""
        self.log_file = log_file
        # Reconfigure logger to use this custom log file
        self._reconfigure_logger()

    def _reconfigure_logger(self) -> None:
        """Reconfigure the logger to use the specified log file."""
        for handler in logger.handlers:
            logger.removeHandler(handler)
        handler = logging.FileHandler(self.log_file, mode="a")
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        handler.setLevel(logging.INFO)
        logger.addHandler(handler)
        logger.setLevel(logging.DEBUG)

    @staticmethod
    def log(message: str) -> None:
        """Log a message to the operations log file."""
        logger.info(message)
        for handler in logger.handlers:
            handler.flush()  # Force flush to disk
