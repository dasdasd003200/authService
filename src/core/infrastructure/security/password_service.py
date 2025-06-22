# src/core/application/services/password_service.py - SIMPLIFIED FINAL
"""
Simple password service - SOLO LO NECESARIO
"""

from django.contrib.auth.hashers import make_password, check_password


class DomainPassword:
    """Simple domain password that works with Django"""

    def __init__(self, hashed_value: str):
        self.hashed_value = hashed_value

    @classmethod
    def create_from_plain(cls, plain_password: str) -> "DomainPassword":
        """Create password from plain text with validation"""
        # Simple validation
        if len(plain_password) < 8:
            raise ValueError("Password must be at least 8 characters")

        # Hash with Django
        hashed = make_password(plain_password)
        return cls(hashed)

    @classmethod
    def from_hash(cls, hashed_value: str) -> "DomainPassword":
        """Create from existing hash"""
        return cls(hashed_value)

    def verify(self, plain_password: str) -> bool:
        """Verify password"""
        return check_password(plain_password, self.hashed_value)

    @property
    def hash(self) -> str:
        """Get hash for storage"""
        return self.hashed_value

    def __str__(self) -> str:
        return "[PROTECTED]"


# Factory functions
def create_password(plain_password: str) -> DomainPassword:
    return DomainPassword.create_from_plain(plain_password)


def load_password(hashed_value: str) -> DomainPassword:
    return DomainPassword.from_hash(hashed_value)

