"""Unit tests for Logger module."""

import logging
from pathlib import Path

from .logger import Logger

LOG_FILE = "operations.log"
TEST_MESSAGE = "Test message"

def test_logger_log_message() -> None:
    """Test that Logger.log writes a message to the log file."""
    logging.basicConfig(filename=LOG_FILE, level=logging.INFO, format="%(message)s")

    logger = Logger()

    logger.log(TEST_MESSAGE)

    with Path(LOG_FILE).open("r") as f:
        content = f.read()
    assert TEST_MESSAGE in content