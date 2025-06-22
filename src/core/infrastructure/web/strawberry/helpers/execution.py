# src/core/infrastructure/web/strawberry/helpers/execution.py
"""
Use case execution wrapper and response creation utilities
"""

from typing import Type, TypeVar, Callable, Any

from src.core.exceptions.base_exceptions import BaseDomainException

T = TypeVar("T")


def create_success_response(response_class: Type[T], message: str = "Operation successful", data: Any = None) -> T:
    """Create standardized success response"""
    return response_class(success=True, message=message, error_code=None, data=data)


def create_error_response(response_class: Type[T], error: Exception, default_message: str = "An error occurred") -> T:
    """Create standardized error response"""
    if isinstance(error, BaseDomainException):
        return response_class(success=False, message=error.message, error_code=error.error_code, data=None)

    return response_class(success=False, message=str(error) if str(error) else default_message, error_code="VALIDATION_ERROR", data=None)


async def execute_use_case(use_case_func: Callable, response_class: Type[T], success_message: str = "Operation completed successfully", *args, **kwargs) -> T:
    """
    Standard pattern for executing use cases in GraphQL mutations/queries
    """
    try:
        result = await use_case_func(*args, **kwargs)
        return create_success_response(response_class, success_message, result)
    except Exception as error:
        return create_error_response(response_class, error)
