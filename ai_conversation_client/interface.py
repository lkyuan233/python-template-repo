from typing import Any
from abc import ABC, abstractmethod

# Interface that client.py will implement
class IAIConversationClient(ABC):
    @abstractmethod
    def send_message(self, session_id: str, message: str) -> dict[str, Any]: ...
    
    @abstractmethod
    def get_chat_history(self, session_id: str) -> list[dict[str, Any]]: ...
    
    @abstractmethod
    def set_user_preferences(self, user_id: str, preferences: dict[str, Any]) -> bool: ...
    
    @abstractmethod
    def start_new_session(self, user_id: str) -> str: ...
    
    @abstractmethod
    def end_session(self, session_id: str) -> bool: ...
