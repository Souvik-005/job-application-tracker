from enum import Enum
from dataclasses import dataclass

class Status(Enum):
    WISHLIST = "wishlist"
    APPLIED = "applied"
    INTERVIEW = "interview"
    OFFER = "offer"
    REJECTED = "rejected"

@dataclass
class Application:
    company: str
    title: str
    status: Status = Status.APPLIED
    job_url: str | None = None
    contact: str | None = None
    notes: str | None = None
    follow_up_date: str | None = None
    id: int | None = None
    date_applied: str | None = None