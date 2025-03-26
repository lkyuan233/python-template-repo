"""Unit tests for Logger module."""

import pytest
import logging
from src.logger import logger_api  # ✅ Importing the Logger API

@pytest.fixture
def logger_instance() -> None:
    """Fixture to use the shared Logger API instance."""
    return logger_api  #  Uses the API from `__init__.py`

def test_log_message(logger_instance, caplog) -> None:
    """Test if a message is logged correctly."""
    test_message = "This is a test log entry"

    with caplog.at_level(logging.INFO):  #  Capture logs at INFO level
        logger_instance.log(test_message)

    #  Check if the message appears in the captured logs
    assert test_message in caplog.text
