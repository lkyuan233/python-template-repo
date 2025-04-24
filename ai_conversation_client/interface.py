from abc import ABC, abstractmethod
from typing import Protocol, Any

class IAIConversationClient(ABC):
    """
    Abstract base class for an AI conversation client.

    This interface defines the standard methods required for managing
    AI chat sessions, sending messages, retrieving history, and handling
    user preferences.
    """

    @abstractmethod
    def send_message(self, session_id: str, message: str) -> dict[str, Any]:
        """
        Send a message to the AI conversation for the given session.

        Args:
            session_id (str): The identifier for the chat session.
            message (str): The user's message to send.

        Returns:
            dict[str, Any]: The AI's response message as a dictionary.
        """
        pass

    @abstractmethod
    def get_chat_history(self, session_id: str) -> list[dict[str, Any]]:
        """
        Retrieve the full chat history for a given session.

        Args:
            session_id (str): The identifier for the chat session.

        Returns:
            list[dict[str, Any]]: A list of message dictionaries representing the chat history.
        """
        pass

    @abstractmethod
    def set_user_preferences(self, user_id: str, preferences: dict[str, Any]) -> bool:
        """
        Set or update preferences for a user.

        Args:
            user_id (str): The user's identifier.
            preferences (dict[str, Any]): A dictionary of user preference settings.

        Returns:
            bool: True if preferences were successfully set.
        """
        pass

    @abstractmethod
    def start_new_session(self, user_id: str) -> str:
        """
        Start a new chat session for the specified user.

        Args:
            user_id (str): The user's identifier.

        Returns:
            str: The new session's unique identifier.
        """
        pass

    @abstractmethod
    def end_session(self, session_id: str) -> bool:
        """
        End and clean up the specified chat session.

        Args:
            session_id (str): The identifier for the chat session.

        Returns:
            bool: True if the session was successfully ended.
        """
        pass

class APIClientProtocol(Protocol):
    """
    Protocol for API client implementations.

    Any concrete API client (e.g., Gemini, OpenAI) must implement these methods
    to be compatible with the AIConversationClient.
    """

    def send(self, session_id: str, message: str) -> dict[str, Any]:
        """
        Send a message to the API for the given session.

        Args:
            session_id (str): The identifier for the chat session.
            message (str): The user's message to send.

        Returns:
            dict[str, Any]: The API's response message as a dictionary.
        """
        ...

    def get_history(self, session_id: str) -> list[dict[str, Any]]:
        """
        Retrieve the full chat history for a given session.

        Args:
            session_id (str): The identifier for the chat session.

        Returns:
            list[dict[str, Any]]: A list of message dictionaries representing the chat history.
        """
        ...

    def set_preferences(self, user_id: str, preferences: dict[str, Any]) -> bool:
        """
        Set or update preferences for a user.

        Args:
            user_id (str): The user's identifier.
            preferences (dict[str, Any]): A dictionary of user preference settings.

        Returns:
            bool: True if preferences were successfully set.
        """
        ...

    def start_session(self, user_id: str) -> str:
        """
        Start a new chat session for the specified user.

        Args:
            user_id (str): The user's identifier.

        Returns:
            str: The new session's unique identifier.
        """
        ...

    def end_session(self, session_id: str) -> bool:
        """
        End and clean up the specified chat session.

        Args:
            session_id (str): The identifier for the chat session.

        Returns:
            bool: True if the session was successfully ended.
        """
        ...
