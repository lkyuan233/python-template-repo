from dataclasses import dataclass
from typing import Any

@dataclass
class Message:
    """Represents a message in a conversation session."""
    session_id: str
    message: str

@dataclass
class UserPreferences:
    """Holds preferences associated with a user."""
    user_id: str
    preferences: dict[str, Any]
