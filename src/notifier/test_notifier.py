"""Unit tests for Notifier module."""

import pytest
import logging
from src.notifier import notifier_api  #  Importing Notifier API

THRESHOLD = 10
HIGH_VALUE = 15
LOW_VALUE = 5

@pytest.fixture
def notifier_instance() -> None:
    """Fixture to use the shared Notifier API instance."""
    return notifier_api  #  Uses API from `__init__.py`

def test_send_alert(notifier_instance, caplog) -> None:
    """Test that Notifier sends an alert when the threshold is exceeded."""
    with caplog.at_level(logging.WARNING):  #  Capture logs at WARNING level
        assert notifier_instance.send_alert(HIGH_VALUE) == (
            f"Alert! Value {HIGH_VALUE} exceeds threshold {THRESHOLD}"
        )
    
    assert notifier_instance.send_alert(LOW_VALUE) == "Value is within the limit."

    #  Check if the message appears in the captured logs
    assert f"Alert! Value {HIGH_VALUE} exceeds threshold {THRESHOLD}" in caplog.text
