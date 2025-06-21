# src/feature/users/infrastructure/web/strawberry/types.py
"""
Strawberry GraphQL types for User feature.
"""

import strawberry
from typing import Optional, List
from datetime import datetime

from src.core.infrastructure.web.strawberry.types import UserStatusEnumStrawberry


@strawberry.type
class UserType:
    """GraphQL type for User"""

    id: str = strawberry.field(description="Unique user ID")
    email: str = strawberry.field(description="User email")
    first_name: str = strawberry.field(description="User first name")
    last_name: str = strawberry.field(description="User last name")
    full_name: str = strawberry.field(description="User full name")
    status: UserStatusEnumStrawberry = strawberry.field(description="User status")
    email_verified: bool = strawberry.field(description="Email verified")
    last_login: Optional[datetime] = strawberry.field(description="Last login")
    failed_login_attempts: int = strawberry.field(description="Failed login attempts")
    created_at: Optional[datetime] = strawberry.field(description="Creation date")
    updated_at: Optional[datetime] = strawberry.field(description="Update date")


@strawberry.input
class CreateUserInput:
    """Input for creating user"""

    email: str = strawberry.field(description="User email")
    password: str = strawberry.field(description="User password")
    first_name: str = strawberry.field(description="User first name")
    last_name: str = strawberry.field(description="User last name")
    email_verified: bool = strawberry.field(default=False, description="Email verified")


# Create response types manually instead of using factory
@strawberry.type
class CreateUserResponse:
    """Response for creating user"""

    success: bool = strawberry.field(
        description="Indicates if the operation was successful"
    )
    message: Optional[str] = strawberry.field(
        description="Human-readable message about the operation result"
    )
    error_code: Optional[str] = strawberry.field(
        description="Machine-readable error code if operation failed"
    )
    data: Optional[UserType] = strawberry.field(description="The operation result data")


@strawberry.type
class UserPaginatedResponse:
    """Paginated response for users"""

    items: List[UserType] = strawberry.field(description="List of users")
    pagination: "PaginationInfo" = strawberry.field(
        description="Pagination information"
    )


# Import PaginationInfo for forward reference
from src.core.infrastructure.web.strawberry.types import PaginationInfo

