import pytest
from ai_conversation_client.client import AIConversationClient
from tests.dummy_api_client import DummyAPIClient

@pytest.fixture
def e2e_client() -> AIConversationClient:
    return AIConversationClient(api_client=DummyAPIClient())

def test_full_chat_flow(e2e_client: AIConversationClient) -> None:
    session_id = e2e_client.start_new_session("userE2E")
    e2e_client.send_message(session_id, "Hello")
    e2e_client.send_message(session_id, "How are you?")
    history = e2e_client.get_chat_history(session_id)
    assert len(history) == 4  
    e2e_client.end_session(session_id)
    history_after = e2e_client.get_chat_history(session_id)
    assert history_after == []
