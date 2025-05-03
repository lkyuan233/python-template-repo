import os
import csv
from spam_detector import process_emails, save_results_to_csv

class FakeEmail:
    def __init__(self, id, body):  # ✅ Fixed constructor
        self.id = id
        self.body = body

class FakeMailClient:
    def get_messages(self):
        return [
            FakeEmail("123", "Hello! Claim your free vacation now."),
            FakeEmail("456", "Reminder: your invoice is ready.")
        ]
    def mark_as_read(self, msg_id):
        return True

class DummyAIClient:
    def send_message(self, session_id, message):
        return {"content": "3.7"}  # 37%

def test_end_to_end_pipeline(tmp_path):
    mail_client = FakeMailClient()
    ai_client = DummyAIClient()
    session_id = "test_session"

    results = process_emails(mail_client, ai_client, session_id)
    assert len(results) == 2
    assert results[0]["Pct_spam"] == 37.0

    output_file = tmp_path / "result.csv"
    save_results_to_csv(results, filename=str(output_file))

    with open(output_file) as f:
        reader = csv.DictReader(f)
        rows = list(reader)
        assert rows[0]["mail_id"] == "123"
        assert float(rows[0]["Pct_spam"]) == 37.0
