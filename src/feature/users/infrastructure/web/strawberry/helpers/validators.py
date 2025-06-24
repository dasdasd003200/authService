import re
from src.core.exceptions.base_exceptions import ValidationException


def validate_user_name(name: str, field_name: str, min_length: int = 1, max_length: int = 50) -> str:
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
    from src.core.infrastructure.web.strawberry.helpers.validators import validate_email_format

    return validate_email_format(email, "User Email")


# Futuras validaciones específicas de users:
# def validate_user_role(role: str) -> str: ...
# def validate_user_permissions(permissions: List[str]) -> List[str]: ...
