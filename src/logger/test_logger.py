"""Unit tests for Logger module."""

import logging
import pytest
from _pytest.logging import LogCaptureFixture

from src.logger import logger_api, ILogger


@pytest.fixture
def logger_instance() -> ILogger:
    """Fixture to use the shared Logger API instance."""
    return logger_api  # Uses the API from `__init__.py`


def test_log_message(
    logger_instance: ILogger, caplog: LogCaptureFixture
) -> None:
    """Test if a message is logged correctly."""
    test_message = "This is a test log entry"

    with caplog.at_level(logging.INFO):  # Capture logs at INFO level
        logger_instance.log(test_message)

    assert test_message in caplog.text
