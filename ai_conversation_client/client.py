from ai_conversation_client.interface import IAIConversationClient, APIClientProtocol
from typing import Any

class AIConversationClient(IAIConversationClient):
    """
    Client for managing AI conversation sessions.
    """

    def __init__(self, api_client: APIClientProtocol) -> None:
        """
        Initializes the client with an API client.
        """
        self.api_client = api_client

    def send_message(self, session_id: str, message: str) -> dict[str, Any]:
        """
        Sends a message in the session.
        """
        return self.api_client.send(session_id, message)

    def get_chat_history(self, session_id: str) -> list[dict[str, Any]]:
        """
        Retrieves the chat history of a session.
        """
        return self.api_client.get_history(session_id)

    def set_user_preferences(self, user_id: str, preferences: dict[str, Any]) -> bool:
        """
        Sets user preferences.
        """
        return self.api_client.set_preferences(user_id, preferences)

    def start_new_session(self, user_id: str) -> str:
        """
        Starts a new session for the user.
        """
        return self.api_client.start_session(user_id)

    def end_session(self, session_id: str) -> bool:
        """
        Ends a conversation session.
        """
        return self.api_client.end_session(session_id)
