from ai_conversation_client.interface import IAIConversationClient, APIClientProtocol
from typing import Any

class AIConversationClient(IAIConversationClient):
    def __init__(self, api_client: APIClientProtocol) -> None:
        self.api_client = api_client

    def send_message(self, session_id: str, message: str) -> dict[str, Any]:
        return self.api_client.send(session_id, message)

    def get_chat_history(self, session_id: str) -> list[dict[str, Any]]:
        return self.api_client.get_history(session_id)

    def set_user_preferences(self, user_id: str, preferences: dict[str, Any]) -> bool:
        return self.api_client.set_preferences(user_id, preferences)

    def start_new_session(self, user_id: str) -> str:
        return self.api_client.start_session(user_id)

    def end_session(self, session_id: str) -> bool:
        return self.api_client.end_session(session_id)
