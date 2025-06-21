# src/core/infrastructure/web/strawberry/types.py
"""
Base Strawberry types for consistent responses across all features.
"""

import strawberry
from enum import Enum
from typing import Optional, TypeVar, List

T = TypeVar("T")


@strawberry.type
class BaseResponse:
    """Base response type for all mutations"""

    success: bool = strawberry.field(
        description="Indicates if the operation was successful"
    )
    message: Optional[str] = strawberry.field(
        description="Human-readable message about the operation result"
    )
    error_code: Optional[str] = strawberry.field(
        description="Machine-readable error code if operation failed"
    )


@strawberry.type
class PaginationInfo:
    """Pagination information for list queries"""

    current_page: int = strawberry.field(description="Current page number")
    page_size: int = strawberry.field(description="Number of items per page")
    total_items: int = strawberry.field(description="Total number of items")
    total_pages: int = strawberry.field(description="Total number of pages")
    has_next: bool = strawberry.field(description="Whether there is a next page")
    has_previous: bool = strawberry.field(
        description="Whether there is a previous page"
    )


@strawberry.input
class PaginationInput:
    """Input type for pagination"""

    page: int = strawberry.field(default=1, description="Page number (starts from 1)")
    page_size: int = strawberry.field(
        default=10, description="Number of items per page"
    )


def create_response_type(data_type, type_name: str):
    """
    Factory function to create response types with data field.

    Usage:
        CreateUserResponse = create_response_type(UserType, "CreateUserResponse")
    """

    @strawberry.type(name=type_name)
    class Response(BaseResponse):
        data: Optional[data_type] = strawberry.field(
            description="The operation result data"
        )

    return Response


def create_paginated_type(item_type, type_name: str):
    """
    Factory function to create paginated response types.

    Usage:
        UserPaginatedResponse = create_paginated_type(UserType, "UserPaginatedResponse")
    """

    @strawberry.type(name=type_name)
    class PaginatedResponse:
        items: List[item_type] = strawberry.field(description="List of items")
        pagination: PaginationInfo = strawberry.field(
            description="Pagination information"
        )

    return PaginatedResponse


# Define the Strawberry enum directly
@strawberry.enum
class UserStatusEnumStrawberry(Enum):
    """Strawberry GraphQL enum for user statuses"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"

