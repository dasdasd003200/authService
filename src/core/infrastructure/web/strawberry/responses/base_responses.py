import strawberry
from typing import Optional, TypeVar, Generic, List
from abc import ABC

T = TypeVar("T")


@strawberry.type
class BaseResponse(ABC):
    success: bool = strawberry.field(description="Operation success status")
    message: Optional[str] = strawberry.field(default=None, description="Response message")
    error_code: Optional[str] = strawberry.field(default=None, description="Error code if failed")


@strawberry.type
class DataResponse(BaseResponse, Generic[T]):
    data: Optional[T] = strawberry.field(default=None, description="Response data")


@strawberry.type
class ListDataResponse(BaseResponse, Generic[T]):
    data: List[T] = strawberry.field(description="List of items")
    total_count: int = strawberry.field(description="Total count of items")


@strawberry.type
class OperationResponse(BaseResponse):
    affected_count: Optional[int] = strawberry.field(default=None, description="Number of affected records")
