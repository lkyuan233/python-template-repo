from typing import Iterator, Protocol, Optional, runtime_checkable, List


@runtime_checkable
class Message(Protocol):
    """A Mail Message."""

    @property
    def id(self) -> str:
        raise NotImplementedError()

    @property
    def from_(self) -> str:
        raise NotImplementedError()

    @property
    def to(self) -> str:
        raise NotImplementedError()

    @property
    def date(self) -> str:
        raise NotImplementedError()

    @property
    def subject(self) -> str:
        raise NotImplementedError()

    @property
    def body(self) -> str:
        raise NotImplementedError()


@runtime_checkable
class Attachment(Protocol):
    """An email attachment."""

    @property
    def filename(self) -> str:
        raise NotImplementedError()

    @property
    def content_type(self) -> str:
        raise NotImplementedError()

    @property
    def data(self) -> bytes:
        raise NotImplementedError()


@runtime_checkable
class Client(Protocol):
    """A Mail Client used to interact with email services."""

    def get_messages(self) -> Iterator[Message]:
        raise NotImplementedError()

    def get_message(self, message_id: str) -> Optional[Message]:
        raise NotImplementedError()

    def send_message(
        self,
        to: str,
        subject: str,
        body: str,
        attachments: Optional[list[Attachment]] = None
    ) -> bool:
        raise NotImplementedError()

    def delete_message(self, message_id: str) -> bool:
        raise NotImplementedError()


def get_client() -> Client:
    raise NotImplementedError()


def create_attachment(
    filename: str, data: bytes, content_type: Optional[str] = None
) -> Attachment:
    raise NotImplementedError()


# ✅ NEWLY ADDED: MailClient Protocol used in spam_detector
class MailClient(Protocol):
    """Extended Client interface for spam detection."""

    def get_messages(self) -> List[Message]:
        ...

    def get_message(self, message_id: str) -> Optional[Message]:
        ...

    def send_message(
        self,
        to: str,
        subject: str,
        body: str,
        attachments: Optional[List[Attachment]] = None
    ) -> bool:
        ...

    def delete_message(self, message_id: str) -> bool:
        ...

    def mark_as_read(self, message_id: str) -> None:
        ...