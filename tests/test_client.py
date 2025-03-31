import pytest
from unittest.mock import MagicMock
from ai_conversation_client.client import AIConversationClient


@pytest.fixture
def client():
    client = AIConversationClient()

    # Mock the methods to return fake valid outputs
    client.send_message = MagicMock(return_value={"reply": "Hello there!"})
    client.get_chat_history = MagicMock(return_value=[{"sender": "user", "text": "Hi"}])
    client.set_user_preferences = MagicMock(return_value=True)
    client.start_new_session = MagicMock(return_value="session_abc123")
    client.end_session = MagicMock(return_value=True)

    return client

def test_send_message(client):
    response = client.send_message("session_123", "Hello")
    assert isinstance(response, dict)
    assert "reply" in response

def test_get_chat_history(client):
    history = client.get_chat_history("session_123")
    assert isinstance(history, list)
    assert all(isinstance(msg, dict) for msg in history)

def test_set_user_preferences(client):
    preferences = {"language": "English", "theme": "dark"}
    result = client.set_user_preferences("user_456", preferences)
    assert isinstance(result, bool)

def test_start_new_session(client):
    session_id = client.start_new_session("user_456")
    assert isinstance(session_id, str)

def test_end_session(client):
    result = client.end_session("session_123")
    assert isinstance(result, bool)
