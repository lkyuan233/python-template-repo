from dataclasses import dataclass

@dataclass
class Message:
    session_id: str
    message: str

@dataclass
class UserPreferences:
    user_id: str
    preferences: dict
