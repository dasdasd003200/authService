import strawberry
from typing import List, Optional
from ..schemes.user import UserGraphQLType  # ✅ CAMBIAR IMPORT


@strawberry.type
class UserFindData:
    users: List[UserGraphQLType] = strawberry.field(description="List of users")  # ✅ CAMBIAR TIPO


@strawberry.type
class UserFindResponse:
    success: bool = strawberry.field(description="Operation success status")
    data: UserFindData = strawberry.field(description="Response data")
    total_count: int = strawberry.field(description="Total count of users")
    message: Optional[str] = strawberry.field(default=None, description="Response message")
    error_code: Optional[str] = strawberry.field(default=None, description="Error code if failed")

