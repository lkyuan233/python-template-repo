import logging
from typing import cast
from mail_client.factories import get_gmail_client
from mail_client.interface import MailClient
from ai_conversation_client.gemini_api_client import GeminiAPIClient
from ai_conversation_client.client import AIConversationClient

from spam_detector import process_emails, save_results_to_csv

def main() -> None:
    # Step 0: Setup logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    print("🚀 Starting main.py...")

    # Step 1: Init Gmail + AI clients
    mail_client = cast(MailClient, get_gmail_client())
    print("✅ Gmail client initialized:", mail_client)

    gemini_backend = GeminiAPIClient()
    ai_client = AIConversationClient(api_client=gemini_backend)
    print("✅ AI client initialized.")

    # Step 2: Start AI session
    user_id = "integration_user"
    session_id = ai_client.start_new_session(user_id=user_id)
    logging.info(f"Started AI session: {session_id}")

    # Step 3: Process emails and get spam scores
    results = process_emails(mail_client, ai_client, session_id)
    print(f"📬 Raw results: {results}")
    logging.info(f"Processed {len(results)} emails.")

    # Step 4: Save to CSV
    save_results_to_csv(results)
    logging.info("Saved output to output.csv.")

    # Step 5: End session
    ai_client.end_session(session_id)
    logging.info("Ended AI session.")

    print("✅ Finished main.py execution.")

if __name__ == "__main__":
    main()
