# src/feature/users/infrastructure/web/strawberry/helpers/validators.py
"""
Validadores específicos del feature USERS
"""

import re
from src.core.exceptions.base_exceptions import ValidationException


def validate_user_name(name: str, field_name: str, min_length: int = 1, max_length: int = 50) -> str:
    """
    Validate user names (first_name, last_name) - ESPECÍFICO DE USERS

    Reglas de negocio específicas para nombres de usuario:
    - Solo letras, espacios, guiones y apostrofes
    - Longitud entre 1 y 50 caracteres
    """
    if not name or not isinstance(name, str):
        raise ValidationException(f"{field_name} is required", error_code="FIELD_REQUIRED")

    name = name.strip()

    if not name:
        raise ValidationException(f"{field_name} cannot be empty", error_code="FIELD_EMPTY")

    if len(name) < min_length:
        raise ValidationException(f"{field_name} must be at least {min_length} characters", error_code="NAME_TOO_SHORT")

    if len(name) > max_length:
        raise ValidationException(f"{field_name} must be at most {max_length} characters", error_code="NAME_TOO_LONG")

    # REGLA ESPECÍFICA DE USERS: Solo letras, espacios, hyphens, apostrophes
    name_pattern = r"^[a-zA-ZÀ-ÿ\s\-']+$"
    if not re.match(name_pattern, name):
        raise ValidationException(f"{field_name} contains invalid characters", error_code="INVALID_NAME_CHARACTERS")

    return name


def validate_user_password(password: str, field_name: str = "Password") -> str:
    """
    Basic password validation for USERS feature

    Nota: Django hará la validación completa, esto es solo validación básica
    """
    if not password or not isinstance(password, str):
        raise ValidationException(f"{field_name} is required", error_code="FIELD_REQUIRED")

    if len(password.strip()) != len(password):
        raise ValidationException(f"{field_name} cannot start or end with spaces", error_code="INVALID_PASSWORD_WHITESPACE")

    if len(password) < 8:
        raise ValidationException(f"{field_name} must be at least 8 characters", error_code="PASSWORD_TOO_SHORT")

    if len(password) > 128:
        raise ValidationException(f"{field_name} is too long (max 128 characters)", error_code="PASSWORD_TOO_LONG")

    return password


def validate_user_email_uniqueness(email: str) -> str:
    """
    Validate email format for USERS feature

    Podría tener reglas específicas de users como:
    - Dominios bloqueados
    - Formatos específicos de empresa
    """
    # Por ahora solo usa la validación genérica
    from src.core.infrastructure.web.strawberry.helpers.validators import validate_email_format

    return validate_email_format(email, "User Email")


# Futuras validaciones específicas de users:
# def validate_user_role(role: str) -> str: ...
# def validate_user_permissions(permissions: List[str]) -> List[str]: ...
