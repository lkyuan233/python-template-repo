"""Logger module for logging operations performed."""

import logging

LOG_FILE = "operations.log"

# Configure logging to write to a file
logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    filemode="a",
)

logger = logging.getLogger('logger')
logger.setLevel(logging.DEBUG)
fh = logging.FileHandler('operations.log')
fh.setLevel(logging.DEBUG)
logger.addHandler(fh)

class Logger:
    """Logger class to log operations performed by the calculator."""

    @staticmethod
    def log(message: str) -> None:
        """Log a message to the operations log file and force flush."""
        logger.info(message)

        # Flush logging handlers to ensure the message is written immediately
        for handler in logging.getLogger().handlers:
            handler.flush()
