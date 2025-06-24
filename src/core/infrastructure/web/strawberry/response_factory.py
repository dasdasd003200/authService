import strawberry
from typing import Type, Optional, List, TypeVar, Generic

T = TypeVar("T")


@strawberry.type
class BaseResponse:
    """Base response para todas las operaciones"""

    success: bool = strawberry.field(description="Indicates if operation was successful")
    message: Optional[str] = strawberry.field(description="Human-readable message")
    error_code: Optional[str] = strawberry.field(description="Machine-readable error code")


def create_mutation_response(data_type: Type[T], type_name: str) -> Type:
    @strawberry.type(name=type_name)
    class MutationResponse(BaseResponse):
        data: Optional[data_type] = strawberry.field(description="The operation result data", default=None)

    return MutationResponse


def create_simple_response(type_name: str) -> Type:
    @strawberry.type(name=type_name)
    class SimpleResponse(BaseResponse):
        pass

    return SimpleResponse


def create_list_response(item_type: Type[T], type_name: str) -> Type:
    @strawberry.type(name=type_name)
    class ListResponse(BaseResponse):
        data: Optional[List[item_type]] = strawberry.field(description="List of items", default=None)
        total_count: Optional[int] = strawberry.field(description="Total number of items", default=None)

    return ListResponse


def create_paginated_response(item_type: Type[T], type_name: str) -> Type:
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


SimpleOperationResponse = create_simple_response("SimpleOperationResponse")


@strawberry.type
class MessageResponse(BaseResponse):
    pass


class ResponseFactory:
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
