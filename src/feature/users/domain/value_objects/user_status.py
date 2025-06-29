# src/feature/users/domain/value_objects/user_status.py
import strawberry
from enum import Enum


@strawberry.enum
class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_string(cls, value: str) -> "UserStatus":
        for status in cls:
            if status.value == value.lower():
                return status
        raise ValueError(f"Status inválido: {value}")

