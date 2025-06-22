# src/core/infrastructure/web/strawberry/response_factory.py - FACTORY PARA RESPONSES
"""
Factory para crear tipos de respuesta GraphQL de forma consistente
"""

import strawberry
from typing import Type, Optional, List, TypeVar, Generic

T = TypeVar("T")


# ===== BASE RESPONSE TYPE =====


@strawberry.type
class BaseResponse:
    """Base response para todas las operaciones"""

    success: bool = strawberry.field(description="Indicates if operation was successful")
    message: Optional[str] = strawberry.field(description="Human-readable message")
    error_code: Optional[str] = strawberry.field(description="Machine-readable error code")


# ===== FACTORY FUNCTIONS =====


def create_mutation_response(data_type: Type[T], type_name: str) -> Type:
    """
    Create a mutation response type with data field

    Usage:
        CreateUserResponse = create_mutation_response(UserType, "CreateUserResponse")
    """

    @strawberry.type(name=type_name)
    class MutationResponse(BaseResponse):
        data: Optional[data_type] = strawberry.field(description="The operation result data", default=None)

    return MutationResponse


def create_simple_response(type_name: str) -> Type:
    """
    Create a simple response without data field

    Usage:
        DeleteUserResponse = create_simple_response("DeleteUserResponse")
    """

    @strawberry.type(name=type_name)
    class SimpleResponse(BaseResponse):
        pass

    return SimpleResponse


def create_list_response(item_type: Type[T], type_name: str) -> Type:
    """
    Create a response for list operations

    Usage:
        SearchUsersResponse = create_list_response(UserType, "SearchUsersResponse")
    """

    @strawberry.type(name=type_name)
    class ListResponse(BaseResponse):
        data: Optional[List[item_type]] = strawberry.field(description="List of items", default=None)
        total_count: Optional[int] = strawberry.field(description="Total number of items", default=None)

    return ListResponse


def create_paginated_response(item_type: Type[T], type_name: str) -> Type:
    """
    Create a paginated response

    Usage:
        UsersPaginatedResponse = create_paginated_response(UserType, "UsersPaginatedResponse")
    """

    @strawberry.type
    class PaginationInfo:
        current_page: int
        page_size: int
        total_items: int
        total_pages: int
        has_next: bool
        has_previous: bool

    @strawberry.type(name=type_name)
    class PaginatedResponse:
        items: List[item_type] = strawberry.field(description="List of items")
        pagination: PaginationInfo = strawberry.field(description="Pagination information")

    return PaginatedResponse


# ===== COMMON RESPONSES =====

# Response simple para operaciones sin datos
SimpleOperationResponse = create_simple_response("SimpleOperationResponse")


# Response genérico con mensaje
@strawberry.type
class MessageResponse(BaseResponse):
    """Generic response with just success/message/error_code"""

    pass


# ===== HELPER PARA CREAR RESPONSES RÁPIDAMENTE =====


class ResponseFactory:
    """Utility class para crear responses comunes"""

    @staticmethod
    def success(message: str = "Operation successful", data=None) -> dict:
        """Create success response data"""
        return {"success": True, "message": message, "error_code": None, "data": data}

    @staticmethod
    def error(message: str, error_code: str = "ERROR") -> dict:
        """Create error response data"""
        return {"success": False, "message": message, "error_code": error_code, "data": None}

    @staticmethod
    def from_exception(exception: Exception) -> dict:
        """Create error response from exception"""
        from src.core.exceptions.base_exceptions import BaseDomainException

        if isinstance(exception, BaseDomainException):
            return ResponseFactory.error(exception.message, exception.error_code)

        return ResponseFactory.error(str(exception), "INTERNAL_ERROR")
