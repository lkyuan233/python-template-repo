"""Gmail implementation of mail_api interfaces."""

from typing import Optional
import base64
import mimetypes

from mail_client.interface import Message, Attachment, Client, create_attachment
from .gmail_client import GmailClient
from .gmail_message import GmailMessage
from .gmail_attachment import GmailAttachment


def get_gmail_client(credentials_file: Optional[str] = None, token_file: Optional[str] = None) -> Client:
    """Return a Gmail implementation of the Client interface.

    Args:
        credentials_file: Path to the credentials.json file. Defaults to 'credentials.json'.
        token_file: Path to the token.json file. Defaults to 'token.json'.

    Returns:
        A Gmail client that implements the Client interface
    """
    return GmailClient(credentials_file=credentials_file, token_file=token_file)


def create_gmail_attachment(
    filename: str,
    data: Optional[bytes],
    content_type: Optional[str] = None,
    service: Optional[object] = None,
    message_id: Optional[str] = None,
) -> Attachment:
    """Create a Gmail attachment.

    Args:
        filename: Name of the attachment file
        data: Binary content of the attachment
        content_type: MIME type of the content (will be guessed if not provided)
        service: Gmail API service client (required for large attachments)
        message_id: The ID of the message the attachment belongs to

    Returns:
        A GmailAttachment object
    """
    if data is not None:
        encoded_data = base64.urlsafe_b64encode(data).decode("ascii")
        body = {"data": encoded_data}
    else:
        body = {"attachmentId": "PLACEHOLDER"}

    attachment_part = {
        "filename": filename,
        "mimeType": content_type
        or mimetypes.guess_type(filename)[0]
        or "application/octet-stream",
        "body": body,
    }

    return GmailAttachment(attachment_part, service=service, message_id=message_id)


# Export public interface
__all__ = [
    "GmailClient",
    "GmailMessage",
    "GmailAttachment",
    "get_gmail_client",
    "create_gmail_attachment",
    "Message",
    "Attachment",
    "Client",
    "create_attachment",
]