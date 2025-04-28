import csv
import logging
import re  # 🆕 import regex module

from mail_client.factories import get_gmail_client  # ✅ Fixed import
from ai_conversation_client.client import AIConversationClient
from ai_conversation_client.gemini_api_client import GeminiAPIClient

def fetch_emails(mail_client):
    """Fetch emails using the mail client."""
    emails = []
    for message in mail_client.get_messages():
        emails.append({
            "id": message.id,
            "subject": message.subject,
            "body": message.body,
        })
    return emails

def sanitize_email_content(email_body):
    """Sanitize email body to protect user privacy."""
    # Return a placeholder instead of real email content
    return "[Email body hidden for privacy]"

def analyze_email(ai_client, session_id, email_body):
    """Send sanitized email content to AI client and get spam probability."""
    sanitized_body = sanitize_email_content(email_body)  # 🛡️ Sanitize before sending to AI

    prompt = f"""
    Given the following parsed email content, rate how much it appears to be spam by giving it a score between 1 and 10 (it can be a decimal value), with 10 being the most likely that the content is spam.
    Your response should only contain the score with no additional text, this is very important.

    Email Content:
    {sanitized_body}
    """
    
    response = ai_client.send_message(session_id=session_id, message=prompt)
    print(response)

    ai_message = response.get("content", "")

    # 🆕 New: Try extracting the first number found in the AI message using regex
    match = re.search(r'\d+(\.\d+)?', ai_message)
    if match:
        spam_probability = float(match.group())
    else:
        logging.warning(f"Could not parse spam probability from response: {ai_message}")
        spam_probability = 0.0  # Default to 0 if parsing fails

    return spam_probability * 10

def save_results_to_csv(results, filename="output.csv"):
    """Save results to a CSV file."""
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["mail_id", "Pct_spam"])
        writer.writeheader()
        for row in results:
            writer.writerow(row)

def main():
    # Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Initialize Gmail client
    gmail_client = get_gmail_client()

    # Initialize AI conversation client
    gemini_backend = GeminiAPIClient()
    ai_client = AIConversationClient(api_client=gemini_backend)
    
    # Start a session for AI Conversation Client
    user_id = "integration_user"  # arbitrary user ID
    session_id = ai_client.start_new_session(user_id=user_id)
    
    logging.info(f"Started AI conversation session: {session_id}")

    # Step 1: Fetch emails
    emails = fetch_emails(gmail_client)
    logging.info(f"Fetched {len(emails)} emails from inbox.")

    # Step 2: Analyze each email
    final_results = []
    for email in emails:
        mail_id = email.get("id")
        body = email.get("body")
        
        if mail_id and body:
            pct_spam = analyze_email(ai_client, session_id, body)
            final_results.append({
                "mail_id": mail_id,
                "Pct_spam": pct_spam
            })
        else:
            logging.warning(f"Skipping email with missing body or ID: {email}")

    # Step 3: Save results to CSV
    save_results_to_csv(final_results)
    logging.info(f"Results saved to output.csv.")

    # Step 4: End the session
    ai_client.end_session(session_id)
    logging.info(f"Ended AI conversation session: {session_id}")

if __name__ == "__main__":
    main()
