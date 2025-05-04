from mail_client.interface import Client, Message, Attachment
from typing import Iterator, Optional
import os.path
import base64
import json
import logging
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build, Resource
from googleapiclient.errors import HttpError

from .gmail_message import GmailMessage

# Set up logger
logger = logging.getLogger(__name__)


class GmailClient(Client):
    """Implementation of the Client interface for Gmail."""

    SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]
    TOKEN_FILE = "token.json"
    CREDENTIALS_FILE = "credentials.json"

    def __init__(self, credentials_file: Optional[str] = None, token_file: Optional[str] = None) -> None:
        self.credentials_file = credentials_file or self.CREDENTIALS_FILE
        self.token_file = token_file or self.TOKEN_FILE
        self.service: Resource = self._get_gmail_service()

    def _get_gmail_service(self) -> Resource:
        creds: Optional[Credentials] = None

        if os.path.exists(self.token_file):
            try:
                with open(self.token_file, "r") as token_file:
                    creds_info = json.load(token_file)
                    creds = Credentials.from_authorized_user_info(creds_info)  # type: ignore[no-untyped-call]
            except (json.JSONDecodeError, ValueError) as e:
                logger.error(f"Error loading token file: {e}")

        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())  # type: ignore[no-untyped-call]
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, self.SCOPES
                )
                creds = flow.run_local_server(port=0)

            if creds is not None:
                with open(self.token_file, "w") as token:
                    token.write(creds.to_json())  # type: ignore[no-untyped-call]

        return build("gmail", "v1", credentials=creds)

    def get_messages(self) -> Iterator[Message]:
        try:
            results = (
                self.service.users()
                .messages()
                .list(userId="me", maxResults=10, labelIds=["INBOX"])
                .execute()
            )
            messages = results.get("messages", [])

            for message in messages:
                msg_id = message["id"]
                msg = self._get_message_by_id(msg_id)
                if msg:
                    yield msg

        except HttpError as error:
            logger.error(f"An error occurred while fetching messages: {error}")

    def get_message(self, message_id: str) -> Optional[Message]:
        return self._get_message_by_id(message_id)

    def _get_message_by_id(self, message_id: str) -> Optional[Message]:
        try:
            message = (
                self.service.users()
                .messages()
                .get(userId="me", id=message_id, format="full")
                .execute()
            )
            return GmailMessage(message)
        except HttpError as error:
            logger.error(f"Error fetching message {message_id}: {error}")
            return None

    def send_message(
        self,
        to: str,
        subject: str,
        body: str,
        attachments: Optional[list[Attachment]] = None,
    ) -> bool:
        try:
            message = MIMEMultipart()
            message["to"] = to
            message["subject"] = subject
            message.attach(MIMEText(body, "plain"))

            if attachments:
                for attachment in attachments:
                    mime_attachment = (
                        MIMEBase(*attachment.content_type.split("/", 1))
                        if "/" in attachment.content_type
                        else MIMEBase("application", "octet-stream")
                    )
                    mime_attachment.set_payload(attachment.data)
                    encoders.encode_base64(mime_attachment)
                    mime_attachment.add_header(
                        "Content-Disposition",
                        f"attachment; filename={attachment.filename}",
                    )
                    message.attach(mime_attachment)

            encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            create_message = {"raw": encoded_message}

            self.service.users().messages().send(
                userId="me", body=create_message
            ).execute()
            return True
        except Exception as error:
            logger.error(f"An error occurred while sending message: {error}")
            return False

    def delete_message(self, message_id: str) -> bool:
        try:
            self.service.users().messages().trash(userId="me", id=message_id).execute()
            return True
        except HttpError as error:
            logger.error(f"Error deleting message {message_id}: {error}")
            return False

    def get_message_by_id(self, message_id: str) -> Optional[Message]:
        """Public method to fetch message by ID."""
        return self._get_message_by_id(message_id)

    def mark_as_read(self, message_id: str) -> bool:
        """Mark an email as read (remove 'UNREAD' label)."""
        try:
            self.service.users().messages().modify(
                userId="me",
                id=message_id,
                body={"removeLabelIds": ["UNREAD"]}
            ).execute()
            return True
        except Exception as error:
            logger.error(f"Failed to mark message {message_id} as read: {error}")
            return False