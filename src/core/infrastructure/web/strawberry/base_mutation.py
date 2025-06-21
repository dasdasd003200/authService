# src/core/infrastructure/web/strawberry/base_mutation.py
import strawberry
import asyncio
from typing import TypeVar, Generic, Type, Callable, Any
from abc import ABC, abstractmethod

from src.core.exceptions.base_exceptions import BaseDomainException
from src.core.infrastructure.web.strawberry.types import BaseResponse

T = TypeVar("T")
TInput = TypeVar("TInput")
TOutput = TypeVar("TOutput")


class BaseMutation(ABC):
    """Base class for all mutations with common error handling"""

    @staticmethod
    def handle_async_execution(async_func: Callable, *args, **kwargs) -> Any:
        """Helper to run async functions in sync context"""
        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(async_func(*args, **kwargs))

    @staticmethod
    def create_success_response(
        response_class: Type[T], message: str, data: Any = None
    ) -> T:
        """Create success response"""
        return response_class(success=True, message=message, error_code=None, data=data)

    @staticmethod
    def create_error_response(response_class: Type[T], error: Exception) -> T:
        """Create error response from exception"""
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
