import csv
from pathlib import Path
from typing import List, Dict, Any

from spam_detector import process_emails, save_results_to_csv


class FakeEmail:
    def __init__(self, id: str, body: str) -> None:
        self.id = id
        self.body = body


class FakeMailClient:
    def get_messages(self) -> List[FakeEmail]:
        return [
            FakeEmail("123", "Hello! Claim your free vacation now."),
            FakeEmail("456", "Reminder: your invoice is ready.")
        ]

    def mark_as_read(self, msg_id: str) -> bool:
        return True


class DummyAIClient:
    def send_message(self, session_id: str, message: str) -> Dict[str, Any]:
        return {"content": "3.7"}  # 37%


def test_end_to_end_pipeline(tmp_path: Path) -> None:
    mail_client = FakeMailClient()
    ai_client = DummyAIClient()
    session_id = "test_session"

    results: List[Dict[str, Any]] = process_emails(mail_client, ai_client, session_id)
    assert len(results) == 2
    assert results[0]["Pct_spam"] == 37.0

    output_file = tmp_path / "result.csv"
    save_results_to_csv(results, filename=str(output_file))

    with open(output_file, newline='') as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert rows[0]["mail_id"] == "123"
        assert float(rows[0]["Pct_spam"]) == 37.0
