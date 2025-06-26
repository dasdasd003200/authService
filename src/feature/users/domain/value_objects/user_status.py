from enum import Enum


class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_string(cls, value: str) -> "UserStatus":
        """Crea UserStatus desde string"""
        for status in cls:
            if status.value == value.lower():
                return status
        raise ValueError(f"Status inválido: {value}")
