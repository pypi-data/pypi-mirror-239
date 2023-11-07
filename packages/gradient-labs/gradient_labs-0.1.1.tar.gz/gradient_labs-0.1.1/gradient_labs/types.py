import iso8601
from enum import Enum


class ParticipantType(str, Enum):
    CUSTOMER: str = "Customer"
    AGENT: str = "Agent"


class Conversation:
    def __init__(self, *, id, customer_id, created, updated, metadata, status):
        self.id = id
        self.customer_id = customer_id
        self.created = iso8601.parse_date(created)
        self.updated = iso8601.parse_date(updated)
        self.metadata = metadata
        self.status = status
