import strawberry
from typing import Optional, List
from datetime import datetime

from src.core.infrastructure.web.strawberry.types import (
    PaginationInfo,
    BaseResponse,
    AuditFields,
)
from src.core.infrastructure.web.strawberry.response_factory import (
    create_mutation_response,
    create_simple_response,
    create_paginated_response,
)
from .enums import UserStatus


@strawberry.type
class UserType:
    id: str = strawberry.field(description="Unique user ID")
    email: str = strawberry.field(description="User email")
    first_name: str = strawberry.field(description="User first name")
    last_name: str = strawberry.field(description="User last name")
    full_name: str = strawberry.field(description="User full name")
    status: UserStatus = strawberry.field(description="User status")
    email_verified: bool = strawberry.field(description="Email verified")
    last_login: Optional[datetime] = strawberry.field(description="Last login")
    failed_login_attempts: int = strawberry.field(description="Failed login attempts")
    created_at: Optional[datetime] = strawberry.field(description="Creation date")
    updated_at: Optional[datetime] = strawberry.field(description="Update date")


@strawberry.input
class CreateUserInput:
    email: str = strawberry.field(description="User email")
    password: str = strawberry.field(description="User password (will be hashed by Django)")
    first_name: str = strawberry.field(description="User first name")
    last_name: str = strawberry.field(description="User last name")
    email_verified: bool = strawberry.field(default=False, description="Email verified")


@strawberry.input
class UpdateUserInput:
    user_id: str = strawberry.field(description="User ID to update")
    first_name: Optional[str] = strawberry.field(default=None, description="New first name")
    last_name: Optional[str] = strawberry.field(default=None, description="New last name")


@strawberry.input
class ChangePasswordInput:
    user_id: str = strawberry.field(description="User ID")
    new_password: str = strawberry.field(description="New password (will be hashed by Django)")


# ===== MUTATION RESPONSES (YA EXISTÍAN) =====
CreateUserResponse = create_mutation_response(UserType, "CreateUserResponse")
UpdateUserResponse = create_mutation_response(UserType, "UpdateUserResponse")
DeleteUserResponse = create_simple_response("DeleteUserResponse")
UsersPaginatedResponse = create_paginated_response(UserType, "UsersPaginatedResponse")

# ===== NUEVOS: QUERY RESPONSES =====
GetUserResponse = create_mutation_response(UserType, "GetUserResponse")
GetUserByEmailResponse = create_mutation_response(UserType, "GetUserByEmailResponse")
