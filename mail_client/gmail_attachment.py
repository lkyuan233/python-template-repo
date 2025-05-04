from mail_client.interface import Attachment
import base64
import binascii
import mimetypes
import logging
from typing import Optional, Dict, Any

# Set up logger
logger = logging.getLogger(__name__)


class GmailAttachment(Attachment):
    """Implementation of the Attachment interface for Gmail."""

    def __init__(
        self,
        attachment_part: Dict[str, Any],
        service: Optional[Any] = None,
        message_id: Optional[str] = None
    ) -> None:
        """Initialize a Gmail attachment.

        Args:
            attachment_part: A Gmail API message part representing an attachment
            service: Gmail API service client (required for large attachments)
            message_id: The ID of the message the attachment belongs to
        """
        self._attachment_part = attachment_part
        self._filename: str = attachment_part.get("filename", "")
        self._mime_type: str = attachment_part.get("mimeType", "")
        self._data_cache: Optional[bytes] = None
        self._service = service
        self._message_id = message_id

    @property
    def filename(self) -> str:
        """Return the filename of the attachment."""
        return self._filename

    @property
    def content_type(self) -> str:
        """Return the MIME content type of the attachment."""
        if not self._mime_type and self._filename:
            guessed_type, _ = mimetypes.guess_type(self._filename)
            if guessed_type:
                return guessed_type
        return self._mime_type or "application/octet-stream"

    @property
    def data(self) -> bytes:
        """Return the binary data of the attachment."""
        if self._data_cache is not None:
            return self._data_cache

        body_data: str = self._attachment_part.get("body", {}).get("data", "")
        if not body_data:
            attachment_id: str = self._attachment_part.get("body", {}).get("attachmentId", "")
            if attachment_id and self._service and self._message_id:
                try:
                    attachment = (
                        self._service.users()
                        .messages()
                        .attachments()
                        .get(userId="me", messageId=self._message_id, id=attachment_id)
                        .execute()
                    )
                    body_data = attachment.get("data", "")
                except Exception as e:
                    logger.error(f"Error occurred while fetching large attachments: {e}")
                    return b""
            else:
                return b""

        try:
            body_data = body_data.replace("-", "+").replace("_", "/")
            padding_needed = len(body_data) % 4
            if padding_needed:
                body_data += "=" * (4 - padding_needed)

            self._data_cache = base64.b64decode(body_data)
            return self._data_cache
        except binascii.Error as e:
            logger.error(f"Error decoding attachment data: {e}")
            return b""
        