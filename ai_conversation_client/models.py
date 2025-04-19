from dataclasses import dataclass
from typing import Any

@dataclass
class Message:
    session_id: str
    message: str

@dataclass
class UserPreferences:
    user_id: str
    preferences: dict[str, Any]
