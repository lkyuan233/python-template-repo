"""Logger module for recording operations."""

from abc import ABC, abstractmethod
from pathlib import Path

from .logger import Logger


# Step 1: Define the interface for Logger
class ILogger(ABC):
    """Interface for a logger component."""

    @abstractmethod
    def log(self, message: str) -> None:
        """Log a message to the log file."""
        pass

    @abstractmethod
    def set_log_file(self, log_file: Path) -> None:
        """Set a custom log file."""
        pass


# Step 2: Provide a default instance implementing the interface
logger_api: ILogger = Logger()

# Step 3: Explicit module exports
__all__ = ["ILogger", "Logger", "logger_api"]
