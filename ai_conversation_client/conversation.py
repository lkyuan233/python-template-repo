from enum import Enum
from datetime import datetime
from typing import List, Dict, Optional, Any
import uuid

class MessageRole(Enum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    FUNCTION = "function"

class Message:
    def __init__(self, content: str, role: MessageRole = MessageRole.USER,
                 message_id: Optional[str] = None, timestamp: Optional[datetime] = None):
        self._content = content
        self._role = role
        self._id = message_id or f"msg_{uuid.uuid4().hex[:8]}"
        self._timestamp = timestamp or datetime.now()

    @property
    def id(self) -> str:
        return self._id

    @property
    def content(self) -> str:
        return self._content

    @property
    def role(self) -> MessageRole:
        return self._role

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    def to_dict(self) -> Dict[str, Any]:
        return {
            "role": self._role.value,
            "content": self._content
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Message':
        role = MessageRole(data.get("role", "user"))
        content = data.get("content", "")
        message_id = data.get("id")
        timestamp_str = data.get("timestamp")

        timestamp = None
        if timestamp_str:
            try:
                timestamp = datetime.fromisoformat(timestamp_str)
            except ValueError:
                timestamp = datetime.now()

        return cls(content, role, message_id, timestamp)

class Conversation:
    def __init__(self, conversation_id: Optional[str] = None,
                 title: Optional[str] = None,
                 system_prompt: Optional[str] = None):
        self._id = conversation_id or f"conv_{uuid.uuid4().hex[:8]}"
        self._title = title or f"Conversation {self._id}"
        self._messages: List[Message] = []

        if system_prompt:
            self.add_message(Message(system_prompt, MessageRole.SYSTEM))

    @property
    def id(self) -> str:
        return self._id

    @property
    def title(self) -> str:
        return self._title

    @property
    def messages(self) -> List[Message]:
        return self._messages.copy()

    def add_message(self, message: Message) -> None:
        self._messages.append(message)

    def get_latest_messages(self, count: int = 5) -> List[Message]:
        return self._messages[-count:] if self._messages else []

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self._id,
            "title": self._title,
            "messages": [
                {
                    "id": msg.id,
                    "content": msg.content,
                    "role": msg.role.value,
                    "timestamp": msg.timestamp.isoformat()
                }
                for msg in self._messages
            ]
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Conversation':
        conversation_id = data.get("id")
        title = data.get("title")
        conversation = cls(conversation_id, title)

        for msg_data in data.get("messages", []):
            role = MessageRole(msg_data.get("role", "user"))
            content = msg_data.get("content", "")
            message_id = msg_data.get("id")

            timestamp = None
            timestamp_str = msg_data.get("timestamp")
            if timestamp_str:
                try:
                    timestamp = datetime.fromisoformat(timestamp_str)
                except ValueError:
                    timestamp = datetime.now()

            message = Message(content, role, message_id, timestamp)
            conversation.add_message(message)

        return conversation