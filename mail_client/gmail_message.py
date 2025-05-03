from mail_client.interface import Message
import html2text
import logging
import base64
import binascii
from typing import Dict, List, Any

# Set up logger
logger = logging.getLogger(__name__)


class GmailMessage(Message):
    """Implementation of the Message interface for Gmail."""

    def __init__(self, message_data: Dict[str, Any]) -> None:
        """Initialize a Gmail message.

        Args:
            message_data: A Gmail API message object
        """
        self._message_data = message_data
        self._body_cache: str | None = None
        self._html_converter = html2text.HTML2Text()
        self._html_converter.ignore_links = False
        self._headers = {
            header["name"].lower(): header["value"]
            for header in message_data.get("payload", {}).get("headers", [])
        }

    @property
    def id(self) -> str:
        """Return the id of the message."""
        return str(self._message_data.get("id", ""))

    @property
    def from_(self) -> str:
        """Return the sender of the message."""
        return str(self._headers.get("from", ""))

    @property
    def to(self) -> str:
        """Return the recipient of the message."""
        return str(self._headers.get("to", ""))

    @property
    def date(self) -> str:
        """Return the date of the message."""
        return str(self._headers.get("date", ""))

    @property
    def subject(self) -> str:
        """Return the subject of the message."""
        return str(self._headers.get("subject", ""))

    @property
    def body(self) -> str:
        """Return the body of the message."""
        if self._body_cache is not None:
            return self._body_cache

        body_text: str = ""
        parts = self._get_parts(self._message_data.get("payload", {}))

        for part in parts:
            mime_type = part.get("mimeType", "")
            if mime_type == "text/plain":
                body_text = self._decode_body(part)
                break
            elif mime_type == "text/html" and not body_text:
                html_body = self._decode_body(part)
                body_text = self._html_converter.handle(html_body)

        if not body_text:
            logger.warning(f"No body extracted from email ID: {self.id}")

        self._body_cache = body_text
        return body_text

    def _get_parts(self, payload: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Recursively get all parts from a message payload."""
        if not payload:
            return []

        parts: List[Dict[str, Any]] = []
        if "body" in payload:
            parts.append(payload)

        for part in payload.get("parts", []):
            parts.extend(self._get_parts(part))

        return parts

    def _decode_body(self, part: Dict[str, Any]) -> str:
        """Decode the body of a message part."""
        body_data = part.get("body", {}).get("data", "")
        if not body_data:
            return ""

        body_data = body_data.replace("-", "+").replace("_", "/")
        padding_needed = len(body_data) % 4
        if padding_needed:
            body_data += "=" * (4 - padding_needed)

        try:
            decoded_data = base64.b64decode(body_data).decode("utf-8")
            return decoded_data
        except (UnicodeDecodeError, binascii.Error) as e:
            logger.error(f"Error decoding message body for email ID {self.id}: {e}")
            return ""
        