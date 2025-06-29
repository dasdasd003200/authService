# src/feature/sessions/domain/value_objects/session_status.py
import strawberry
from enum import Enum


@strawberry.enum
class SessionStatus(Enum):
    ACTIVE = "active"
    EXPIRED = "expired"
    REVOKED = "revoked"
    LOGGED_OUT = "logged_out"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_string(cls, value: str) -> "SessionStatus":
        for status in cls:
            if status.value == value.lower():
                return status
        raise ValueError(f"Invalid session status: {value}")
