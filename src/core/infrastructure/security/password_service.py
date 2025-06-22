# src/core/infrastructure/security/password_service.py - SIMPLIFICADO
"""
Password service using ONLY Django's built-in facilities.
No custom classes, just simple functions.
"""

from django.contrib.auth.hashers import make_password, check_password


def hash_password(plain_password: str) -> str:
    """
    Hash a plain password using Django's system.

    Args:
        plain_password: The plain text password

    Returns:
        The hashed password string

    Raises:
        ValueError: If password is too short or invalid
    """
    # Basic validation
    if not plain_password or len(plain_password.strip()) < 8:
        raise ValueError("Password must be at least 8 characters")

    # Use Django's make_password (handles salt automatically)
    return make_password(plain_password.strip())


def verify_password(plain_password: str, password_hash: str) -> bool:
    """
    Verify a plain password against a hash using Django's system.

    Args:
        plain_password: The plain text password to verify
        password_hash: The stored hash to check against

    Returns:
        True if password matches, False otherwise
    """
    if not plain_password or not password_hash:
        return False

    return check_password(plain_password, password_hash)


# Optional: Password strength validation
def validate_password_strength(password: str) -> list[str]:
    """
    Validate password strength and return list of issues.

    Returns:
        Empty list if valid, list of error messages if invalid
    """
    errors = []

    if len(password) < 8:
        errors.append("Password must be at least 8 characters")

    if password.isdigit():
        errors.append("Password cannot be only numbers")

    if password.lower() in ["password", "12345678", "qwerty"]:
        errors.append("Password is too common")

    return errors

