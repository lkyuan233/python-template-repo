import os
import uuid
import requests
from typing import Any
from dotenv import load_dotenv
import importlib

from ai_conversation_client.interface import APIClientProtocol
from ai_conversation_client.conversations import Conversation, Message, MessageRole

load_dotenv()

class GeminiAPIClient(APIClientProtocol):
    """
    Gemini API client implementing the APIClientProtocol interface.
    Manages chat sessions and communicates with the Gemini API.
    """

    def __init__(self) -> None:
        """
        Initialize the GeminiAPIClient and load the API key.
        """
        self._api_key = os.getenv("GEMINI_API_KEY")
        if not self._api_key:
            raise ValueError("Missing GEMINI_API_KEY in .env file")

        genai = importlib.import_module("google.generativeai")
        genai.configure(api_key=self._api_key)
        self._model = genai.GenerativeModel("gemini-pro")

        self._model_url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"gemini-2.0-flash:generateContent?key={self._api_key}"
        )

        self._sessions: dict[str, Conversation] = {}
        self._chat_sessions: dict[str, Any] = {}
        self._user_preferences: dict[str, dict[str, Any]] = {}

    def send(self, session_id: str, message: str) -> dict[str, Any]:
        """
        Send a message to the Gemini API for a given session.

        Args:
            session_id: The session identifier.
            message: The user's message.

        Returns:
            dict: The assistant's response.
        """
        if session_id not in self._sessions:
            raise ValueError("Session not found")

        convo = self._sessions[session_id]
        convo.add_message(Message(message, MessageRole.USER))

        history = "\n".join(
            f"{msg.role.value.capitalize()}: {msg.content}"
            for msg in convo.messages
        )

        payload = {
            'contents': [
                {'parts': [{'text': history}]}
            ]
        }
        headers = {'Content-Type': 'application/json'}

        try:
            response = requests.post(self._model_url, headers=headers, json=payload)
            response.raise_for_status()
            parsed = response.json()
            text = parsed['candidates'][0]['content']['parts'][0]['text'].strip()
            assistant_msg = Message(text, MessageRole.ASSISTANT)
            convo.add_message(assistant_msg)

            return {
                "message_id": assistant_msg.id,
                "role": assistant_msg.role.value,
                "content": assistant_msg.content,
                "timestamp": assistant_msg.timestamp.isoformat()
            }
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {e}")

    def get_history(self, session_id: str) -> list[dict[str, Any]]:
        """
        Get the chat history for a session.

        Args:
            session_id: The session identifier.

        Returns:
            list: List of message dictionaries.
        """
        if session_id not in self._sessions:
            return []
        return [
            {
                "message_id": m.id,
                "role": m.role.value,
                "content": m.content,
                "timestamp": m.timestamp.isoformat()
            }
            for m in self._sessions[session_id].messages
        ]

    def set_preferences(self, user_id: str, preferences: dict[str, Any]) -> bool:
        """
        Set user preferences.

        Args:
            user_id: The user's identifier.
            preferences: A dictionary of preferences.

        Returns:
            bool: True if successful.
        """
        self._user_preferences[user_id] = preferences
        return True

    def start_session(self, user_id: str) -> str:
        """
        Start a new chat session.

        Args:
            user_id: The user's identifier.

        Returns:
            str: The new session's ID.
        """
        session_id = f"sess_{uuid.uuid4().hex[:8]}"
        prompt = self._user_preferences.get(user_id, {}).get("system_prompt")
        convo = Conversation(conversation_id=session_id, system_prompt=prompt)
        self._sessions[session_id] = convo
        self._chat_sessions[session_id] = self._model.start_chat(history=[])
        return session_id

    def end_session(self, session_id: str) -> bool:
        """
        End a chat session.

        Args:
            session_id: The session identifier.

        Returns:
            bool: True if successful.
        """
        self._sessions.pop(session_id, None)
        self._chat_sessions.pop(session_id, None)
        return True
