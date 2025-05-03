from spam_detector import analyze_email

class FakeEmail:
    def __init__(self, id, body):  # ✅ Fixed constructor
        self.id = id
        self.body = body

class FakeMailClient:
    def get_messages(self):
        return [FakeEmail("1", "Win a FREE iPhone by clicking here!")]
    def mark_as_read(self, msg_id):
        return True

class DummyAIClient:
    def send_message(self, session_id, message):
        return {"content": "6.5"}

def test_integration_fetch_and_score_email():
    mail_client = FakeMailClient()
    ai_client = DummyAIClient()
    session_id = "fake_session"

    emails = mail_client.get_messages()
    assert emails[0].id == "1"

    score = analyze_email(ai_client, session_id, emails[0].body)
    assert score == 65.0
