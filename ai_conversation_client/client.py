from ai_conversation_client.interface import IAIConversationClient, APIClientProtocol
from typing import Any

class AIConversationClient(IAIConversationClient):
    """
    Main client class handling conversation sessions through an API provider.
    Implements IAIConversationClient interface.
    """

    def __init__(self, api_client: APIClientProtocol) -> None:
        """
        Initialize with a concrete API provider.

        Args:
            api_client: Implementation of APIClientProtocol.
        """
        self.api_client = api_client

    def send_message(self, session_id: str, message: str) -> dict[str, Any]:
        """
        Send a message to the specified session.

        Args:
            session_id: The session identifier.
            message: The user's message.

        Returns:
            dict: The assistant's response.
        """
        return self.api_client.send(session_id, message)

    def get_chat_history(self, session_id: str) -> list[dict[str, Any]]:
        """
        Retrieve the chat history for a session.

        Args:
            session_id: The session identifier.

        Returns:
            list: List of message dictionaries.
        """
        return self.api_client.get_history(session_id)

    def set_user_preferences(self, user_id: str, preferences: dict[str, Any]) -> bool:
        """
        Set user preferences.

        Args:
            user_id: The user's identifier.
            preferences: A dictionary of preferences.

        Returns:
            bool: True if successful.
        """
        return self.api_client.set_preferences(user_id, preferences)

    def start_new_session(self, user_id: str) -> str:
        """
        Start a new session for the user.

        Args:
            user_id: The user's identifier.

        Returns:
            str: The new session's ID.
        """
        return self.api_client.start_session(user_id)

    def end_session(self, session_id: str) -> bool:
        """
        End a chat session.

        Args:
            session_id: The session identifier.

        Returns:
            bool: True if successful.
        """
        return self.api_client.end_session(session_id)
