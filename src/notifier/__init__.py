"""Notifier module initialization."""

from .notifier import Notifier

# Define module-level API
notifier_api = Notifier(threshold=10)  #  Default threshold

# Expose only necessary components
__all__ = ["Notifier", "notifier_api"]
