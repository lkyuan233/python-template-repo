import re
import pytest
from spam_detector import (
    sanitize_email_content,
    analyze_email,
    build_prompt,
    detect_spam_score  # ✅ NEW IMPORT
)

class DummyAIClient:
    def send_message(self, session_id, message):
        return {"content": "7.2"}  # Expected to give score 72.0

def test_sanitize_email_content_masks_sensitive_data():
    content = "Contact me at john@example.com or 1234567890. Also my bank: 123456789012"
    result = sanitize_email_content(content)
    assert "[EMAIL]" in result
    assert "[PHONE]" in result
    assert "[SENSITIVE]" in result

def test_build_prompt_format():
    email = "hello world this is a test email with words " * 10
    prompt = build_prompt(email)
    assert "Email Content:" in prompt
    assert len(prompt.split()) <= 70  # Assuming content is truncated

def test_analyze_email_parses_number_correctly():
    ai_client = DummyAIClient()
    score = analyze_email(ai_client, "test_session", "Buy cheap stuff now!")
    assert score == pytest.approx(72.0)

# ✅ NEW TEST
def test_detect_spam_score_utility():
    class DummyAIClient:
        def send_message(self, session_id, message):
            return {"content": "4.5"}  # Should return 45.0

    ai_client = DummyAIClient()
    email_body = "You have won a lottery. Click to claim your prize!"
    score = detect_spam_score(email_body, ai_client, session_id="dummy_session")
    assert score == pytest.approx(45.0)
