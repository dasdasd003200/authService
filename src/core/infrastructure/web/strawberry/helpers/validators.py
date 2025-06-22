# src/core/infrastructure/web/strawberry/helpers/validators.py
"""
Input validation utilities for GraphQL mutations and queries
"""

import re
from typing import Any
from uuid import UUID

from src.core.exceptions.base_exceptions import ValidationException


def validate_uuid(uuid_str: str, field_name: str = "ID") -> UUID:
    """Validate and convert string to UUID with enhanced error messages"""
    if not uuid_str or not isinstance(uuid_str, str):
        raise ValidationException(f"{field_name} is required", error_code="FIELD_REQUIRED")

    uuid_str = uuid_str.strip()
    if not uuid_str:
        raise ValidationException(f"{field_name} cannot be empty", error_code="FIELD_EMPTY")

    try:
        return UUID(uuid_str)
    except (ValueError, TypeError):
        raise ValidationException(f"Invalid {field_name} format: {uuid_str}", error_code="INVALID_UUID")


def validate_required(value: Any, field_name: str) -> Any:
    """Validate required field with better error handling"""
    if value is None:
        raise ValidationException(f"{field_name} is required", error_code="FIELD_REQUIRED")

    if isinstance(value, str):
        value = value.strip()
        if not value:
            raise ValidationException(f"{field_name} cannot be empty", error_code="FIELD_EMPTY")

    return value


def validate_email_format(email: str, field_name: str = "Email") -> str:
    """Enhanced email validation with comprehensive checks"""
    if not email or not isinstance(email, str):
        raise ValidationException(f"{field_name} is required", error_code="FIELD_REQUIRED")

    email = email.strip().lower()

    if not email:
        raise ValidationException(f"{field_name} cannot be empty", error_code="FIELD_EMPTY")

    # Length validation first
    if len(email) > 254:
        raise ValidationException(f"{field_name} is too long (max 254 characters)", error_code="EMAIL_TOO_LONG")

    # Basic format validation
    if "@" not in email:
        raise ValidationException(f"{field_name} must contain @ symbol", error_code="INVALID_EMAIL_FORMAT")

    parts = email.split("@")
    if len(parts) != 2:
        raise ValidationException(f"{field_name} format is invalid", error_code="INVALID_EMAIL_FORMAT")

    local, domain = parts
    if not local or not domain:
        raise ValidationException(f"{field_name} format is invalid", error_code="INVALID_EMAIL_FORMAT")

    # Local part validation
    if len(local) > 64:
        raise ValidationException(f"{field_name} local part is too long (max 64 characters)", error_code="EMAIL_LOCAL_TOO_LONG")

    # Domain validation
    if "." not in domain:
        raise ValidationException(f"{field_name} domain must contain a dot", error_code="INVALID_EMAIL_DOMAIN")

    # More comprehensive regex validation
    email_pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if not re.match(email_pattern, email):
        raise ValidationException(f"{field_name} format is invalid", error_code="INVALID_EMAIL_FORMAT")

    return email


def validate_name(name: str, field_name: str, min_length: int = 1, max_length: int = 50) -> str:
    """Validate user names (first_name, last_name)"""
    if not name or not isinstance(name, str):
        raise ValidationException(f"{field_name} is required", error_code="FIELD_REQUIRED")

    name = name.strip()

    if not name:
        raise ValidationException(f"{field_name} cannot be empty", error_code="FIELD_EMPTY")

    if len(name) < min_length:
        raise ValidationException(f"{field_name} must be at least {min_length} characters", error_code="NAME_TOO_SHORT")

    if len(name) > max_length:
        raise ValidationException(f"{field_name} must be at most {max_length} characters", error_code="NAME_TOO_LONG")

    # Only allow letters, spaces, hyphens, apostrophes
    name_pattern = r"^[a-zA-ZÀ-ÿ\s\-']+$"
    if not re.match(name_pattern, name):
        raise ValidationException(f"{field_name} contains invalid characters", error_code="INVALID_NAME_CHARACTERS")

    return name


def validate_password_strength(password: str, field_name: str = "Password") -> str:
    """Basic password validation (Django will do full validation)"""
    if not password or not isinstance(password, str):
        raise ValidationException(f"{field_name} is required", error_code="FIELD_REQUIRED")

    if len(password.strip()) != len(password):
        raise ValidationException(f"{field_name} cannot start or end with spaces", error_code="INVALID_PASSWORD_WHITESPACE")

    if len(password) < 8:
        raise ValidationException(f"{field_name} must be at least 8 characters", error_code="PASSWORD_TOO_SHORT")

    if len(password) > 128:
        raise ValidationException(f"{field_name} is too long (max 128 characters)", error_code="PASSWORD_TOO_LONG")

    return password
