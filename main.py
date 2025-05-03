# mail_client/gmail_message.py

import base64
import logging
from typing import List, Dict, Any
from googleapiclient.discovery import Resource
from googleapiclient.errors import HttpError


class GmailMessageClient:
    def __init__(self, service: Resource, user_id: str = "me") -> None:
        self.service = service
        self.user_id = user_id

    def _get_parts(self, parts: List[Dict[str, Any]]) -> str:
        """Recursively search through MIME parts to extract email body."""
        for part in parts:
            if part.get("mimeType") == "text/plain" and "data" in part.get("body", {}):
                return self._decode_body(part["body"]["data"])
            if "parts" in part:
                result = self._get_parts(part["parts"])
                if result:
                    return result
        return ""

    def _decode_body(self, body: str) -> str:
        """Decode base64 URL-safe encoded email body."""
        try:
            decoded_bytes = base64.urlsafe_b64decode(body.encode("ASCII"))
            return decoded_bytes.decode("utf-8")
        except Exception as e:
            logging.warning(f"Failed to decode body: {e}")
            return ""

    def get_body_from_message(self, message: Dict[str, Any]) -> str:
        """Extract body text from message payload."""
        payload = message.get("payload", {})
        if payload.get("mimeType") == "text/plain":
            body = payload.get("body", {}).get("data")
            return self._decode_body(body) if body else ""
        if payload.get("mimeType") == "multipart/alternative":
            return self._get_parts(payload.get("parts", []))
        return ""

    def get_messages(self) -> List[Dict[str, str]]:
        """Get list of unread messages and extract their content."""
        results: List[Dict[str, str]] = []
        try:
            response = self.service.users().messages().list(userId=self.user_id, labelIds=["INBOX"], q="is:unread").execute()
            messages = response.get("messages", [])
            for msg in messages:
                msg_id = msg["id"]
                message = self.service.users().messages().get(userId=self.user_id, id=msg_id, format="full").execute()
                body = self.get_body_from_message(message)
                results.append({"id": msg_id, "body": body})
        except HttpError as error:
            logging.error(f"An error occurred: {error}")
        return results

    def mark_as_read(self, msg_id: str) -> None:
        """Mark a message as read by removing UNREAD label."""
        try:
            self.service.users().messages().modify(
                userId=self.user_id,
                id=msg_id,
                body={"removeLabelIds": ["UNREAD"]}
            ).execute()
        except HttpError as error:
            logging.error(f"An error occurred while marking as read: {error}")
