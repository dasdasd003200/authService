import strawberry
from typing import Optional
from ..schemes.user import UserGraphQLType  # ✅ CAMBIAR IMPORT


@strawberry.type
class UserCreateResponse:
    success: bool = strawberry.field(description="Operation success status")
    data: Optional[UserGraphQLType] = strawberry.field(default=None, description="Created user data")  # ✅ CAMBIAR TIPO
    message: Optional[str] = strawberry.field(default=None, description="Response message")
    error_code: Optional[str] = strawberry.field(default=None, description="Error code if failed")

