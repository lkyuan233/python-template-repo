from abc import ABC, abstractmethod
from typing import Any, Protocol

# -----------------------------
# Main Interface
# -----------------------------
class IAIConversationClient(ABC):
    @abstractmethod
    def send_message(self, session_id: str, message: str) -> dict[str, Any]: pass

    @abstractmethod
    def get_chat_history(self, session_id: str) -> list[dict[str, Any]]: pass

    @abstractmethod
    def set_user_preferences(self, user_id: str, preferences: dict[str, Any]) -> bool: pass

    @abstractmethod
    def start_new_session(self, user_id: str) -> str: pass

    @abstractmethod
    def end_session(self, session_id: str) -> bool: pass

# -----------------------------
# Protocol for injected dependency
# -----------------------------
class APIClientProtocol(Protocol):
    def send(self, session_id: str, message: str) -> dict[str, Any]: ...
    def get_history(self, session_id: str) -> list[dict[str, Any]]: ...
    def set_preferences(self, user_id: str, preferences: dict[str, Any]) -> bool: ...
    def start_session(self, user_id: str) -> str: ...
    def end_session(self, session_id: str) -> bool: ...
