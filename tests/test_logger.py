"""Unit tests for Logger module."""

from pathlib import Path

from src.logger import Logger

LOG_FILE = Path("operations.log")

def test_log() -> None:
    """Test logging functionality."""
    Logger.log("Test log entry")

    with LOG_FILE.open() as file:
        content = file.read()

    assert "Test log entry" in content
