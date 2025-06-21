# src/core/application/services/password_service.py
"""
Password service that bridges domain password validation with Django's password hashing system.

This service provides a consistent way to handle passwords across all features while
maintaining domain validation rules and leveraging Django's proven hashing mechanisms.
"""

from django.contrib.auth.hashers import make_password, check_password
from src.feature.users.domain.value_objects.password import Password


class DjangoPasswordAdapter(Password):
    """
    Adapter that makes Django's password system work with domain Password validation.

    This adapter:
    - Uses domain Password validation rules
    - Leverages Django's secure hashing system
    - Provides consistent interface across features
    - Maintains compatibility with Django admin and auth system
    """

    def __init__(self, django_password_hash: str):
        """
        Initialize with Django password hash.

        Args:
            django_password_hash: The hashed password from Django's system
        """
        # Store Django hash
        self._django_hash = django_password_hash

        # Set dummy values for the parent class requirements
        # We override the behavior but need to satisfy the dataclass
        object.__setattr__(self, "hashed_value", django_password_hash)
        object.__setattr__(self, "salt", "")

    @classmethod
    def create_django(cls, plain_password: str) -> "DjangoPasswordAdapter":
        """
        Create password using Django's hashing system with domain validation.

        Args:
            plain_password: The plain text password

        Returns:
            DjangoPasswordAdapter instance

        Raises:
            ValueError: If password doesn't meet domain requirements
        """
        # Use domain validation rules first
        cls._validate_password(plain_password)

        # Hash using Django's system
        django_hash = make_password(plain_password)

        return cls(django_hash)

    @classmethod
    def from_django_hash(cls, django_hash: str) -> "DjangoPasswordAdapter":
        """
        Create adapter from existing Django hash (for loading from DB).

        Args:
            django_hash: Existing Django password hash

        Returns:
            DjangoPasswordAdapter instance
        """
        return cls(django_hash)

    def verify(self, plain_password: str) -> bool:
        """
        Verify password using Django's system.

        Args:
            plain_password: Password to verify

        Returns:
            True if password matches, False otherwise
        """
        return check_password(plain_password, self._django_hash)

    @property
    def django_hash(self) -> str:
        """Get the Django password hash."""
        return self._django_hash

    def __str__(self) -> str:
        return "[PROTECTED_DJANGO_PASSWORD]"

    def __repr__(self) -> str:
        return "DjangoPasswordAdapter([PROTECTED])"


def create_password_from_plain(plain_password: str) -> DjangoPasswordAdapter:
    """
    Factory function to create password from plain text.

    This is the main entry point for creating passwords in the application.

    Args:
        plain_password: The plain text password

    Returns:
        DjangoPasswordAdapter instance

    Raises:
        ValueError: If password validation fails
    """
    return DjangoPasswordAdapter.create_django(plain_password)


def create_password_from_hash(django_hash: str) -> DjangoPasswordAdapter:
    """
    Factory function to create password from Django hash.

    Used when loading users from database.

    Args:
        django_hash: Existing Django password hash

    Returns:
        DjangoPasswordAdapter instance
    """
    return DjangoPasswordAdapter.from_django_hash(django_hash)


def verify_password(
    plain_password: str, hashed_password: DjangoPasswordAdapter
) -> bool:
    """
    Utility function to verify passwords.

    Args:
        plain_password: Plain text password to verify
        hashed_password: DjangoPasswordAdapter instance

    Returns:
        True if password matches, False otherwise
    """
    return hashed_password.verify(plain_password)
