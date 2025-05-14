"""Notifier module for sending alerts when a threshold is exceeded."""

from abc import ABC, abstractmethod
from .notifier import Notifier

# Step 1: Define the interface for Notifier
class INotifier(ABC):
    """Interface for a notifier component."""

    @abstractmethod
    def send_alert(self, value: float) -> str:
        """Send an alert if the value exceeds a threshold."""
        pass

# Step 2: Provide a default API instance (threshold = 10 used in tests)
notifier_api: INotifier = Notifier(threshold=10)

# Step 3: Explicit module exports
__all__ = ["INotifier", "Notifier", "notifier_api"]
