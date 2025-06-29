import strawberry
from typing import Optional, TypeVar, Generic, List
from abc import ABC

T = TypeVar("T")


@strawberry.type
class BaseResponse(ABC):
    """Base response for all operations"""

    success: bool = strawberry.field(description="Operation success status")
    message: Optional[str] = strawberry.field(default=None, description="Response message")
    error_code: Optional[str] = strawberry.field(default=None, description="Error code if failed")


@strawberry.type
class DataResponse(BaseResponse, Generic[T]):
    """Response with single data item"""

    data: Optional[T] = strawberry.field(default=None, description="Response data")


@strawberry.type
class ListDataResponse(BaseResponse, Generic[T]):
    """Response with list of data items"""

    data: List[T] = strawberry.field(description="List of items")
    total_count: int = strawberry.field(description="Total count of items")


@strawberry.type
class OperationResponse(BaseResponse):
    """Response for operations without data return (like delete)"""

    affected_count: Optional[int] = strawberry.field(default=None, description="Number of affected records")

