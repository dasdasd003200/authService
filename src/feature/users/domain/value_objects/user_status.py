# src/feature/users/domain/value_objects/user_status.py
from enum import Enum


class UserStatus(Enum):
    """Estados posibles de un usuario"""

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

    @property
    def is_active(self) -> bool:
        """Verifica si el status es activo"""
        return self == UserStatus.ACTIVE

    @property
    def can_login(self) -> bool:
        """Verifica si el usuario puede hacer login"""
        return self in [UserStatus.ACTIVE]
