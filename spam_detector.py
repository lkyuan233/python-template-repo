import re
import logging
import csv
from typing import List, Dict, TypedDict, Protocol
from mail_client.interface import MailClient


# AI Client protocol for interacting with LLMs
class AIClient(Protocol):
    def send_message(self, session_id: str, message: str) -> Dict[str, str]: ...


# Final output structure per email
class SpamResult(TypedDict):
    mail_id: str
    Pct_spam: float


def sanitize_email_content(email_body: str) -> str:
    """Mask email addresses, phone numbers, and sensitive numeric data."""
    email_body = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[EMAIL]', email_body)
    email_body = re.sub(r'\b\d{10}\b', '[PHONE]', email_body)
    email_body = re.sub(r'\b\d{12,}\b', '[SENSITIVE]', email_body)
    words = email_body.split()
    return " ".join(words[:50]) + " ..." if len(words) > 50 else " ".join(words)


def build_prompt(email_body: str) -> str:
    """Construct the prompt to send to the AI model."""
    sanitized = sanitize_email_content(email_body)
    return f"""
    Given the following parsed email content, rate how much it appears to be spam by giving it a score between 1 and 10 (decimal allowed), with 10 being most spammy.
    Your response should only contain the score.

    Email Content:
    {sanitized}
    """


def analyze_email(ai_client: AIClient, session_id: str, email_body: str) -> float:
    """Send email to AI client and extract spam score (scaled to 100)."""
    prompt = build_prompt(email_body)
    response = ai_client.send_message(session_id=session_id, message=prompt)
    ai_message = response.get("content", "")
    match = re.search(r'\d+(\.\d+)?', ai_message)
    if match:
        return float(match.group()) * 10  # Convert score out of 10 to percentage
    logging.warning(f"Could not parse spam probability from response: {ai_message}")
    return 0.0


def process_emails(mail_client: MailClient, ai_client: AIClient, session_id: str) -> List[SpamResult]:
    """Process all unread emails and return spam scores."""
    results: List[SpamResult] = []
    emails = mail_client.get_messages()
    for email in emails:
        if email.id and email.body:
            pct_spam = analyze_email(ai_client, session_id, email.body)
            results.append({"mail_id": email.id, "Pct_spam": pct_spam})
            mail_client.mark_as_read(email.id)
        else:
            logging.warning(f"Skipped email with missing id/body: {email}")
    return results


def save_results_to_csv(results: List[SpamResult], filename: str = "output.csv") -> None:
    """Save results to a CSV file."""
    with open(filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=["mail_id", "Pct_spam"])
        writer.writeheader()
        writer.writerows(results)


def detect_spam_score(email_body: str, ai_client: AIClient, session_id: str) -> float:
    """Wrapper for analyze_email to expose a more intuitive name."""
    return analyze_email(ai_client, session_id, email_body)