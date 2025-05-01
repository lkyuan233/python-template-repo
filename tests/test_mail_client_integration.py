import pytest
from unittest.mock import MagicMock
from mail_client.gmail_client import GmailClient
from mail_client.factories import create_gmail_attachment

@pytest.fixture
def mock_gmail_client(monkeypatch):
    client = GmailClient()
    service = MagicMock()
    client.service = service
    return client

def test_send_email_with_attachment(mock_gmail_client):
    attachment = create_gmail_attachment("test.txt", b"Hello World")
    result = mock_gmail_client.send_message(
        to="receiver@example.com",
        subject="Test Email",
        body="Test Body",
        attachments=[attachment],
    )
    assert result is True

def test_fetch_messages(mock_gmail_client):
    mock_gmail_client.service.users.return_value.messages.return_value.list.return_value.execute.return_value = {
        "messages": [{"id": "12345"}]
    }
    mock_gmail_client.service.users.return_value.messages.return_value.get.return_value.execute.return_value = {
        "id": "12345", "payload": {"headers": []}
    }
    messages = list(mock_gmail_client.get_messages())
    assert len(messages) == 1

def test_delete_message(mock_gmail_client):
    mock_gmail_client.service.users.return_value.messages.return_value.trash.return_value.execute.return_value = {}
    result = mock_gmail_client.delete_message("12345")
    assert result is True
