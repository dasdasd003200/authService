# src/core/infrastructure/web/strawberry/base_mutation.py - SIMPLIFIED
import asyncio
from typing import TypeVar, Type, Callable, Any

from src.core.exceptions.base_exceptions import BaseDomainException

T = TypeVar("T")


def handle_async_execution(async_func: Callable, *args, **kwargs) -> Any:
    """Helper to run async functions in sync context"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(async_func(*args, **kwargs))


def create_success_response(
    response_class: Type[T], message: str, data: Any = None
) -> T:
    """Create success response - FIXED"""
    return response_class(success=True, message=message, error_code=None, data=data)


def create_error_response(response_class: Type[T], error: Exception) -> T:
    """Create error response from exception - FIXED"""
    if isinstance(error, BaseDomainException):
        return response_class(
            success=False,
            message=error.message,
            error_code=error.error_code,
            data=None,
        )
    else:
        return response_class(
            success=False,
            message=f"An unexpected error occurred: {str(error)}",
            error_code="INTERNAL_ERROR",
            data=None,
        )


# FIXED: Simple response types directly
import strawberry
from typing import Optional


@strawberry.type
class BaseResponse:
    """Base response type for all mutations"""

    success: bool
    message: Optional[str] = None
    error_code: Optional[str] = None


@strawberry.type
class CreateUserResponse(BaseResponse):
    """Response for creating user"""

    data: Optional[Any] = None  # Will be UserType

