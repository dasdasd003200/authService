# src/core/infrastructure/web/strawberry/helpers/validators.py
"""
Input validation utilities for GraphQL mutations and queries
SOLO VALIDACIONES VERDADERAMENTE GENÉRICAS Y REUTILIZABLES
"""

import re
from typing import Any
from uuid import UUID

from src.core.exceptions.base_exceptions import ValidationException


def validate_uuid(uuid_str: str, field_name: str = "ID") -> UUID:
    """
    Validate and convert string to UUID - GENÉRICO
    Cualquier feature puede usar UUIDs para identificadores
    """
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
    """
    Validate required field - GENÉRICO
    Cualquier feature puede usar esta validación básica
    """
    if value is None:
        raise ValidationException(f"{field_name} is required", error_code="FIELD_REQUIRED")

    if isinstance(value, str):
        value = value.strip()
        if not value:
            raise ValidationException(f"{field_name} cannot be empty", error_code="FIELD_EMPTY")

    return value


def validate_email_format(email: str, field_name: str = "Email") -> str:
    """
    Enhanced email validation - GENÉRICO
    Múltiples features podrían necesitar validar emails (users, contacts, notifications, etc.)
    """
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


def validate_positive_integer(value: Any, field_name: str, min_value: int = 1) -> int:
    """
    Validate positive integer - GENÉRICO
    Útil para IDs, cantidades, páginas, etc.
    """
    try:
        int_value = int(value)
        if int_value < min_value:
            raise ValidationException(f"{field_name} must be at least {min_value}", error_code="VALUE_TOO_SMALL")
        return int_value
    except (ValueError, TypeError):
        raise ValidationException(f"{field_name} must be a valid integer", error_code="INVALID_INTEGER")


def validate_string_length(value: str, field_name: str, min_length: int = 0, max_length: int = 255) -> str:
    """
    Generic string length validation - GENÉRICO
    Útil para cualquier campo de texto con restricciones de longitud
    """
    if not isinstance(value, str):
        raise ValidationException(f"{field_name} must be a string", error_code="INVALID_TYPE")

    value = value.strip()

    if len(value) < min_length:
        raise ValidationException(f"{field_name} must be at least {min_length} characters", error_code="STRING_TOO_SHORT")

    if len(value) > max_length:
        raise ValidationException(f"{field_name} must be at most {max_length} characters", error_code="STRING_TOO_LONG")

    return value


# ELIMINADOS: validate_name() y validate_password_strength()
# → Movidos a src/feature/users/infrastructure/web/strawberry/helpers/validators.py

