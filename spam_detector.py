# spam_detector/spam_detector.py

import re
import logging
import csv

def sanitize_email_content(email_body):
    email_body = re.sub(r'\b[\w\.-]+@[\w\.-]+\.\w+\b', '[EMAIL]', email_body)
    email_body = re.sub(r'\b\d{10}\b', '[PHONE]', email_body)
    email_body = re.sub(r'\b\d{12,}\b', '[SENSITIVE]', email_body)
    words = email_body.split()
    return " ".join(words[:50]) + " ..." if len(words) > 50 else " ".join(words)

def build_prompt(email_body):
    sanitized = sanitize_email_content(email_body)
    return f"""
    Given the following parsed email content, rate how much it appears to be spam by giving it a score between 1 and 10 (decimal allowed), with 10 being most spammy.
    Your response should only contain the score.

    Email Content:
    {sanitized}
    """

def analyze_email(ai_client, session_id, email_body):
    prompt = build_prompt(email_body)
    response = ai_client.send_message(session_id=session_id, message=prompt)
    ai_message = response.get("content", "")
    match = re.search(r'\d+(\.\d+)?', ai_message)
    if match:
        return float(match.group()) * 10
    logging.warning(f"Could not parse spam probability from response: {ai_message}")
    return 0.0

def process_emails(mail_client, ai_client, session_id):
    results = []
    emails = mail_client.get_messages()
    for email in emails:
        if email.id and email.body:
            pct_spam = analyze_email(ai_client, session_id, email.body)
            results.append({"mail_id": email.id, "Pct_spam": pct_spam})
            mail_client.mark_as_read(email.id)
    return results

def save_results_to_csv(results, filename="output.csv"):
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["mail_id", "Pct_spam"])
        writer.writeheader()
        writer.writerows(results)

# ✅ New utility function for third-party usage
def detect_spam_score(email_body, ai_client, session_id):
    """
    Public utility to return a spam score given an email body.
    Handles prompt construction and parsing internally.
    """
    return analyze_email(ai_client, session_id, email_body)
