"""Logger module for recording operations."""

from .logger import Logger

# Define module-level API
logger_api = Logger()

# Expose only necessary components
__all__ = ["Logger", "logger_api"]
