import pytest
from tests.dummy_client import DummyAIClient

@pytest.fixture
def client():
    return DummyAIClient()

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
