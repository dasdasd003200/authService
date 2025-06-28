import strawberry
from typing import Optional
from ..schemes.user import UserGraphQLType


@strawberry.type
class UserFindOneData:
    user: Optional[UserGraphQLType] = strawberry.field(default=None, description="Found user")


@strawberry.type
class UserFindOneResponse:
    success: bool = strawberry.field(description="Operation success status")
    data: UserFindOneData = strawberry.field(description="Response data")
    message: Optional[str] = strawberry.field(default=None, description="Response message")
    error_code: Optional[str] = strawberry.field(default=None, description="Error code if failed")
