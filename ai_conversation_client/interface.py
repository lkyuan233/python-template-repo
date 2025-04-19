from abc import ABC, abstractmethod

class IAIConversationClient(ABC):
    @abstractmethod
    def send_message(self, session_id: str, message: str) -> dict: pass

    @abstractmethod
    def get_chat_history(self, session_id: str) -> list: pass

    @abstractmethod
    def set_user_preferences(self, user_id: str, preferences: dict) -> bool: pass

    @abstractmethod
    def start_new_session(self, user_id: str) -> str: pass

    @abstractmethod
    def end_session(self, session_id: str) -> bool: pass
