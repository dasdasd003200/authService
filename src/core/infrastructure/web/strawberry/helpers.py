# src/core/infrastructure/web/strawberry/helpers.py - CORE HELPERS ESENCIALES
"""
Core helpers para Strawberry GraphQL - SOLO LO ESENCIAL
"""

from typing import Optional, Type, TypeVar, Callable, Any, Dict
from uuid import UUID
import strawberry

from src.core.exceptions.base_exceptions import BaseDomainException

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

    return response_class(success=False, message=str(error) if str(error) else default_message, error_code="INTERNAL_ERROR", data=None)


# ===== ASYNC EXECUTION WRAPPER =====


async def execute_use_case(use_case_func: Callable, response_class: Type[T], success_message: str = "Operation completed successfully", *args, **kwargs) -> T:
    """
    Standard pattern for executing use cases in GraphQL mutations/queries

    Usage:
        return await execute_use_case(
            lambda: use_case.execute(command),
            CreateUserResponse,
            "User created successfully"
        )
    """
    try:
        result = await use_case_func(*args, **kwargs)
        return create_success_response(response_class, success_message, result)
    except Exception as error:
        return create_error_response(response_class, error)


# ===== INPUT VALIDATION =====


def validate_uuid(uuid_str: str, field_name: str = "ID") -> UUID:
    """Validate and convert string to UUID"""
    try:
        return UUID(uuid_str)
    except (ValueError, TypeError):
        raise ValueError(f"Invalid {field_name}: {uuid_str}")


def validate_required(value: Any, field_name: str) -> Any:
    """Validate required field"""
    if value is None or (isinstance(value, str) and not value.strip()):
        raise ValueError(f"{field_name} is required")
    return value


def validate_email_format(email: str) -> str:
    """Basic email validation"""
    email = email.strip().lower()
    if "@" not in email or "." not in email.split("@")[1]:
        raise ValueError(f"Invalid email format: {email}")
    return email


# ===== GRAPHQL TYPE FACTORIES =====


def create_base_response_type(name: str, data_type: Optional[Type] = None):
    """
    Factory to create GraphQL response types

    Usage:
        CreateUserResponse = create_base_response_type("CreateUserResponse", UserType)
    """

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
        # Try to find matching value
        for enum_item in graphql_enum_class:
            if enum_item.value == domain_value:
                return enum_item

        # Fallback to first item if no match
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

