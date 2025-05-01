import pytest
from unittest.mock import MagicMock
from mail_client.gmail_client import GmailClient
from mail_client.factories import create_gmail_attachment

@pytest.fixture
def e2e_mail_client(monkeypatch):
    client = GmailClient()
    service = MagicMock()
    client.service = service
    return client

def test_full_email_flow(e2e_mail_client):
    
    e2e_mail_client.service.users.return_value.messages.return_value.send.return_value.execute.return_value = {}
    
    attachment = create_gmail_attachment("example.txt", b"Email body")
    sent = e2e_mail_client.send_message(
        to="receiver@example.com",
        subject="Full E2E Email",
        body="This is the body",
        attachments=[attachment]
    )
    assert sent is True

    
    e2e_mail_client.service.users.return_value.messages.return_value.list.return_value.execute.return_value = {
        "messages": [{"id": "id1"}]
    }
    e2e_mail_client.service.users.return_value.messages.return_value.get.return_value.execute.return_value = {
        "id": "id1", "payload": {"headers": []}
    }
    messages = list(e2e_mail_client.get_messages())
    assert len(messages) == 1

    
    e2e_mail_client.service.users.return_value.messages.return_value.trash.return_value.execute.return_value = {}
    deleted = e2e_mail_client.delete_message("id1")
    assert deleted is True
