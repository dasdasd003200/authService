import strawberry
from typing import TypeVar, Generic, Optional


T = TypeVar("T")


@strawberry.type
class CreateResponse(Generic[T]):
    """Standard create operation response"""

    success: bool = strawberry.field(description="Operation success status")
    data: Optional[T] = strawberry.field(default=None, description="Created item data")
    message: Optional[str] = strawberry.field(default=None, description="Response message")
    error_code: Optional[str] = strawberry.field(default=None, description="Error code if failed")


@strawberry.type
class UpdateResponse(Generic[T]):
    """Standard update operation response"""

    success: bool = strawberry.field(description="Operation success status")
    data: Optional[T] = strawberry.field(default=None, description="Updated item data")
    message: Optional[str] = strawberry.field(default=None, description="Response message")
    error_code: Optional[str] = strawberry.field(default=None, description="Error code if failed")


@strawberry.type
class DeleteResponse:
    """Standard delete operation response"""

    success: bool = strawberry.field(description="Operation success status")
    message: Optional[str] = strawberry.field(default=None, description="Response message")
    error_code: Optional[str] = strawberry.field(default=None, description="Error code if failed")
    affected_count: Optional[int] = strawberry.field(default=None, description="Number of deleted records")


@strawberry.type
class FindData(Generic[T]):
    """Standard find data container"""

    items: list[T] = strawberry.field(description="List of found items")


@strawberry.type
class FindResponse(Generic[T]):
    """Standard find operation response"""

    success: bool = strawberry.field(description="Operation success status")
    data: FindData[T] = strawberry.field(description="Response data")
    total_count: int = strawberry.field(description="Total count of items")
    message: Optional[str] = strawberry.field(default=None, description="Response message")
    error_code: Optional[str] = strawberry.field(default=None, description="Error code if failed")


@strawberry.type
class FindOneData(Generic[T]):
    """Standard find one data container"""

    item: Optional[T] = strawberry.field(default=None, description="Found item")


@strawberry.type
class FindOneResponse(Generic[T]):
    """Standard find one operation response"""

    success: bool = strawberry.field(description="Operation success status")
    data: FindOneData[T] = strawberry.field(description="Response data")
    message: Optional[str] = strawberry.field(default=None, description="Response message")
    error_code: Optional[str] = strawberry.field(default=None, description="Error code if failed")

