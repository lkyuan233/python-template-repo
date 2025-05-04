import csv
from pathlib import Path
from typing import List, Dict, Any

from spam_detector import process_emails, save_results_to_csv, SpamResult
from mail_client.interface import MailClient, Message
from ai_conversation_client.interface import IAIConversationClient


class FakeEmail:
    def __init__(self, email_id: str, body: str) -> None:
        self._id = email_id
        self._body = body

    @property
    def id(self) -> str:
        return self._id

    @property
    def from_(self) -> str:
        return "sender@example.com"

    @property
    def to(self) -> str:
        return "recipient@example.com"

    @property
    def date(self) -> str:
        return "2025-05-03"

    @property
    def subject(self) -> str:
        return "Sample Subject"

    @property
    def body(self) -> str:
        return self._body


class FakeMailClient:
    def get_messages(self) -> List[Message]:
        return [
            FakeEmail("123", "Hello! Claim your free vacation now."),
            FakeEmail("456", "Reminder: your invoice is ready."),
        ]

    def get_message(self, message_id: str) -> Message:
        return FakeEmail(message_id, "Generated content")

    def send_message(self, to: str, subject: str, body: str, attachments: Any = None) -> bool:
        return True

    def delete_message(self, message_id: str) -> bool:
        return True

    def mark_as_read(self, message_id: str) -> None:
        return None


class DummyAIClient(IAIConversationClient):
    def send_message(self, session_id: str, message: str) -> Dict[str, Any]:
        return {"content": "3.7"}  # 37%

    def get_chat_history(self, session_id: str) -> List[Dict[str, Any]]:
        return []

    def set_user_preferences(self, user_id: str, preferences: Dict[str, Any]) -> bool:
        return True

    def start_new_session(self, user_id: str) -> str:
        return "session_id"

    def end_session(self, session_id: str) -> bool:
        return True


def test_end_to_end_pipeline(tmp_path: Path) -> None:
    mail_client: MailClient = FakeMailClient()
    ai_client: IAIConversationClient = DummyAIClient()
    session_id = "test_session"

    results: List[SpamResult] = process_emails(mail_client, ai_client, session_id)
    assert len(results) == 2
    assert results[0]["Pct_spam"] == 37.0

    output_file = tmp_path / "result.csv"
    save_results_to_csv(results, filename=str(output_file))

    with open(output_file, newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert rows[0]["mail_id"] == "123"
        assert float(rows[0]["Pct_spam"]) == 37.0