# import asyncio
# from ai_conversation_client.cli import run_cli
# from ai_conversation_client.client import AIConversationClient
from ai_conversation_client.gemini_api_client import GeminiAPIClient

# def main() -> None:
#     gemini_backend = GeminiAPIClient()
#     client = AIConversationClient(api_client=gemini_backend)
#     asyncio.run(run_cli(client))

# if __name__ == "__main__":
#     main()

# import asyncio
# from ai_conversation_client.cli import run_cli
# from ai_conversation_client.client import AIConversationClient
# from ai_conversation_client.gemini_api_client import GeminiAPIClient

# def main() -> None:
#     gemini_backend = GeminiAPIClient()
#     client = AIConversationClient(api_client=gemini_backend)
#     asyncio.run(run_cli(client))

# if __name__ == "__main__":
#     main()

import csv
import logging

from mail_gmail_impl.src.mail_gmail_impl import get_gmail_client
from ai_conversation_client.client import AIConversationClient

def fetch_emails(mail_client):
    """Fetch emails using the mail client."""
    emails = []
    for message in mail_client.get_messages():
        emails.append({
            "id": message.id,         # each message has an id
            "subject": message.subject,
            "body": message.body
        })
    return emails

def analyze_email(ai_client, session_id, email_body):
    """Send email content to AI client and get spam probability."""
    # prompt = f"Analyze this email carefully and give me only a number between 0 and 100.\nWhat is the % probability that this email is spam?\n\nEmail Content:\n{email_body}"
    prompt = f"""
    Given the following parsed email content, rate how much it appears to be spam by giving it a score between 1 and 10 (it can be a decimal value), with 10 being the most likely that the content is spam. \nYour response should only contain the score with no additional text, this is very important.\n\nEmail Content:\n{email_body}
    """
    
    response = ai_client.send_message(session_id=session_id, message=prompt)
    print(response)
    # Expect response like {'content': '7', 'role': 'assistant', 'timestamp': '...', 'id': '...'}
    ai_message = response.get("content", "")
    
    try:
        spam_probability = float(ai_message.strip())
    except ValueError:
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
    # ai_client = AIConversationClient()
    gemini_backend = GeminiAPIClient()
    ai_client = AIConversationClient(api_client=gemini_backend)
    
    # Start a session for AI Conversation Client
    user_id = "integration_user"  # arbitrary
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
