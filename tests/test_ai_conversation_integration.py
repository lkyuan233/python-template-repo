import pytest
from ai_conversation_client.client import AIConversationClient
from tests.dummy_api_client import DummyAPIClient

@pytest.fixture
def client() -> AIConversationClient:
    api = DummyAPIClient()
    return AIConversationClient(api_client=api)

def test_send_message_adds_entries(client: AIConversationClient) -> None:
    session_id = client.start_new_session("user1")
    client.send_message(session_id, "Hello")
    history = client.get_chat_history(session_id)
    assert len(history) == 2  # User + Assistant

def test_user_preferences_persist(client: AIConversationClient) -> None:
    client.set_user_preferences("user2", {"system_prompt": "Welcome!"})
    session_id = client.start_new_session("user2")
    history = client.get_chat_history(session_id)
    assert any("Welcome!" in msg["content"] for msg in history)

def test_end_session_clears_history(client: AIConversationClient) -> None:
    session_id = client.start_new_session("user3")
    client.send_message(session_id, "Hi")
    client.end_session(session_id)
    history = client.get_chat_history(session_id)
    assert history == []

def test_multiple_sessions(client: AIConversationClient) -> None:
    s1 = client.start_new_session("userA")
    s2 = client.start_new_session("userB")
    assert s1 != s2
