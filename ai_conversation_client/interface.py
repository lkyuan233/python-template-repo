from abc import ABC, abstractmethod
from typing import Any, Protocol

# -----------------------------
# Main Interface
# -----------------------------
class IAIConversationClient(ABC):
    """Interface for an AI conversation client."""

    @abstractmethod
    def send_message(self, session_id: str, message: str) -> dict[str, Any]:
        """Send a message in a session."""
        pass

    @abstractmethod
    def get_chat_history(self, session_id: str) -> list[dict[str, Any]]:
        """Get chat history for a session."""
        pass

    @abstractmethod
    def set_user_preferences(self, user_id: str, preferences: dict[str, Any]) -> bool:
        """Set preferences for a user."""
        pass

    @abstractmethod
    def start_new_session(self, user_id: str) -> str:
        """Start a new session for a user."""
        pass

    @abstractmethod
    def end_session(self, session_id: str) -> bool:
        """End an existing session."""
        pass

# -----------------------------
# Protocol for injected dependency
# -----------------------------
class APIClientProtocol(Protocol):
    """Protocol for the API client dependency."""

    def send(self, session_id: str, message: str) -> dict[str, Any]:
        """Send a message in a session."""
        ...

    def get_history(self, session_id: str) -> list[dict[str, Any]]:
        """Get history for a session."""
        ...

    def set_preferences(self, user_id: str, preferences: dict[str, Any]) -> bool:
        """Set user preferences."""
        ...

    def start_session(self, user_id: str) -> str:
        """Start a new session for a user."""
        ...

    def end_session(self, session_id: str) -> bool:
        """End a session."""
        ...
