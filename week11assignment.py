from dataclasses import dataclass, field
from contextlib import contextmanager

class EmailError(Exception):
    pass
@dataclass
class Email:
    subject: str
    category: str
    size: int
    _status: str = field(init=False, default="UNREAD")

    def __post_init__(self):
        if self.size <= 0:
            raise EmailError(f"Invalid size for {self.subject}")


    @property
    def is_large(self) -> bool:
        return self.size > 100

    def __str__(self) -> str:
        return f"{self.subject} ({self.category}, {self.size}KB) [{self._status}]"

    def __gt__(self, other) -> bool:
        if isinstance(other, Email):
            return self.size > other.size
        return NotImplemented

class InboxFilter:
    def __init__(self, emails, allowed):
        self.emails = emails
        self.allowed = allowed
        self.index = 0


    def __iter__(self):
        return self

    def __next__(self):

        if self.index >= len(self.emails):
            raise StopIteration


        email = self.emails[self.index]
        self.index += 1

        if email.category in self.allowed:
            email._status = "KEPT"
        else:
            email._status = "DELETED"

        return email

def inbox_report(filt):
    kept = 0
    deleted = 0

    for email in filt:
        if email._status == "KEPT":
            kept += 1
        else:
            deleted += 1

        yield str(email)

    yield f"Result: {kept} kept, {deleted} deleted"


@contextmanager
def inbox_session(name):

    print(f"[OPEN] {name}")
    emails = []
    try:

        yield emails
    except EmailError as e:
        print(f"!!! Error: {e}")
    finally:
        print(f"[CLOSE] {name} ({len(emails)} emails)")