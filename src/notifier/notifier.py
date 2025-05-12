"""Notifier module for sending alerts when a threshold is exceeded."""

import logging

logger = logging.getLogger(__name__)  #  Uses dynamic module name

class Notifier:
    """Notifier class to send alerts if a calculated value exceeds a threshold."""

    def __init__(self, threshold: float) -> None:
        """Initialize Notifier with a given threshold."""
        self.threshold = threshold

    def send_alert(self, value: float) -> str:
        """Send an alert if the value exceeds the threshold."""
        if value > self.threshold:
            message = f"Alert! Value {value} exceeds threshold {self.threshold}"
            logger.warning(message)  #  Log the alert
            return message
        return "Value is within the limit."
