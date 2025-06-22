# src/core/infrastructure/web/strawberry/helpers.py - VALIDACIÓN CENTRALIZADA
"""
Core helpers para Strawberry GraphQL - Validación centralizada y robusta
"""

from typing import Optional, Type, TypeVar, Callable, Any, Dict
from uuid import UUID
import strawberry
import re

from src.core.exceptions.base_exceptions import BaseDomainException, ValidationException

T = TypeVar("T")


# ===== CONVERSION UTILITIES =====


def safe_uuid_str(uuid_obj: Optional[UUID]) -> str:
    """Convert UUID to string safely"""
    return str(uuid_obj) if uuid_obj else ""


def safe_str(obj: Any) -> str:
    """Convert any object to string safely"""
    return str(obj) if obj is not None else ""


def safe_int(value: Any, default: int = 0) -> int:
    """Convert to int safely"""
    try:
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default


# ===== GRAPHQL RESPONSE FACTORIES =====


def create_success_response(response_class: Type[T], message: str = "Operation successful", data: Any = None) -> T:
    """Create standardized success response"""
    return response_class(success=True, message=message, error_code=None, data=data)


def create_error_response(response_class: Type[T], error: Exception, default_message: str = "An error occurred") -> T:
    """Create standardized error response"""
    if isinstance(error, BaseDomainException):
        return response_class(success=False, message=error.message, error_code=error.error_code, data=None)

    return response_class(success=False, message=str(error) if str(error) else default_message, error_code="VALIDATION_ERROR", data=None)


# ===== ASYNC EXECUTION WRAPPER =====


async def execute_use_case(use_case_func: Callable, response_class: Type[T], success_message: str = "Operation completed successfully", *args, **kwargs) -> T:
    """
    Standard pattern for executing use cases in GraphQL mutations/queries
    """
    try:
        result = await use_case_func(*args, **kwargs)
        return create_success_response(response_class, success_message, result)
    except Exception as error:
        return create_error_response(response_class, error)


# ===== ENHANCED INPUT VALIDATION =====


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


# ===== INPUT PROCESSORS (Para usar en mutations) =====


def process_create_user_input(input_data) -> Dict[str, Any]:
    """Process and validate CreateUserInput centrally"""
    return {
        "email": validate_email_format(input_data.email),
        "password": validate_password_strength(input_data.password),
        "first_name": validate_name(input_data.first_name, "First name"),
        "last_name": validate_name(input_data.last_name, "Last name"),
        "email_verified": bool(input_data.email_verified),
    }


def process_update_user_input(input_data) -> Dict[str, Any]:
    """Process and validate UpdateUserInput centrally"""
    result = {
        "user_id": validate_uuid(input_data.user_id, "User ID"),
    }

    # Optional fields
    if input_data.first_name is not None:
        result["first_name"] = validate_name(input_data.first_name, "First name")

    if input_data.last_name is not None:
        result["last_name"] = validate_name(input_data.last_name, "Last name")

    return result


def process_change_password_input(input_data) -> Dict[str, Any]:
    """Process and validate ChangePasswordInput centrally"""
    return {
        "user_id": validate_uuid(input_data.user_id, "User ID"),
        "new_password": validate_password_strength(input_data.new_password, "New password"),
    }


# ===== GRAPHQL TYPE FACTORIES =====


def create_base_response_type(name: str, data_type: Optional[Type] = None):
    """Factory to create GraphQL response types"""

    @strawberry.type(name=name)
    class BaseResponse:
        success: bool = strawberry.field(description="Operation success status")
        message: Optional[str] = strawberry.field(description="Human readable message")
        error_code: Optional[str] = strawberry.field(description="Error code for client handling")

        if data_type:
            data: Optional[data_type] = strawberry.field(description="Operation result data")
        else:
            data: Optional[str] = strawberry.field(description="Operation result", default=None)

    return BaseResponse


# ===== ENUM CONVERSION =====


def convert_domain_enum_to_graphql(domain_value: str, graphql_enum_class) -> Any:
    """Convert domain enum value to GraphQL enum"""
    try:
        for enum_item in graphql_enum_class:
            if enum_item.value == domain_value:
                return enum_item
        return list(graphql_enum_class)[0]
    except (AttributeError, IndexError):
        return None


# ===== PAGINATION HELPERS =====


def create_pagination_response(items: list, total_count: int, page: int, page_size: int) -> Dict[str, Any]:
    """Create standardized pagination response"""
    total_pages = (total_count + page_size - 1) // page_size

    return {"items": items, "pagination": {"current_page": page, "page_size": page_size, "total_items": total_count, "total_pages": total_pages, "has_next": page < total_pages, "has_previous": page > 1}}


# ===== FIELD CONVERTERS =====


def convert_datetime_to_iso(dt) -> Optional[str]:
    """Convert datetime to ISO string safely"""
    return dt.isoformat() if dt else None


def extract_domain_errors(errors: list) -> Dict[str, str]:
    """Extract domain validation errors into field-specific format"""
    error_dict = {}
    for error in errors:
        if hasattr(error, "field") and hasattr(error, "message"):
            error_dict[error.field] = error.message
        else:
            error_dict["general"] = str(error)
    return error_dict

