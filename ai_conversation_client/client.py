from typing import Dict, List, Optional
import uuid
import os
import json
import requests
from dotenv import load_dotenv
import google.generativeai as genai
from .conversation import Conversation, Message, MessageRole

load_dotenv()

class AIConversationClient:
    def __init__(self):
        """Initializes the AI conversation client."""
        self._sessions: Dict[str, Conversation] = {}
        self._chat_sessions: Dict[str, genai.ChatSession] = {}
        self._user_preferences: Dict[str, dict] = {}

        self._api_key = os.getenv("GEMINI_API_KEY")
        if not self._api_key:
            raise ValueError("Missing GEMINI_API_KEY in .env file")

        genai.configure(api_key=self._api_key)
        self._model = genai.GenerativeModel("gemini-pro")
        self._model_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={self._api_key}"

    async def send_message(self, session_id: str, message: str) -> dict:
        """
        Sends a message to the AI and receives a response.
        """
        if session_id not in self._sessions or session_id not in self._chat_sessions:
            raise ValueError(f"No session found with ID: {session_id}")

        conversation = self._sessions[session_id]
        conversation.add_message(Message(message, MessageRole.USER))
        
        history = "\n".join(
            f"{msg.role.value.capitalize()}: {msg.content}" for msg in conversation.messages
        )
        
        payload = {
            'contents': [
                {
                    'parts': [
                        {
                            'text': history
                        }
                    ]
                }
            ]
        }
        
        headers = {
            'Content-Type': 'application/json',
        }

        try:
            # chat = self._chat_sessions[session_id]
            # response = chat.send_message(message)
            # reply = response.text.strip()
            
            response = requests.post(self._model_url, headers=headers, json=payload)
            response.raise_for_status()

            parsed = response.json()
            text = parsed['candidates'][0]['content']['parts'][0]['text'].strip()
            
            assistant_msg = Message(text, MessageRole.ASSISTANT)
            conversation.add_message(assistant_msg)

            # assistant_msg = Message(reply, MessageRole.ASSISTANT)
            # conversation.add_message(assistant_msg)

            return {
                "message_id": assistant_msg.id,
                "role": assistant_msg.role.value,
                "content": assistant_msg.content,
                "timestamp": assistant_msg.timestamp.isoformat()
            }
        except Exception as e:
            raise RuntimeError(f"Gemini API error: {e}")

    def get_chat_history(self, session_id: str) -> List[dict]:
        if session_id not in self._sessions:
            raise ValueError(f"No session found with ID: {session_id}")

        return [
            {
                "message_id": msg.id,
                "role": msg.role.value,
                "content": msg.content,
                "timestamp": msg.timestamp.isoformat()
            }
            for msg in self._sessions[session_id].messages
        ]

    def set_user_preferences(self, user_id: str, preferences: dict) -> bool:
        self._user_preferences[user_id] = preferences
        return True

    def start_new_session(self, user_id: str) -> str:
        session_id = f"sess_{uuid.uuid4().hex[:8]}"
        system_prompt = self._user_preferences.get(user_id, {}).get("system_prompt")

        # Create both a local conversation and a Gemini chat session
        conversation = Conversation(conversation_id=session_id, system_prompt=system_prompt)
        chat = self._model.start_chat(history=[])

        self._sessions[session_id] = conversation
        self._chat_sessions[session_id] = chat
        return session_id

    def end_session(self, session_id: str) -> bool:
        self._sessions.pop(session_id, None)
        self._chat_sessions.pop(session_id, None)
        return True