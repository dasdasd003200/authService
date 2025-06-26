import strawberry
from typing import Optional
from datetime import datetime
from ..enums.status import UserStatus


@strawberry.type
class UserGraphQLType:
    id: str = strawberry.field(description="Unique user identifier")
    email: str = strawberry.field(description="User email address")
    first_name: str = strawberry.field(description="User first name")
    last_name: str = strawberry.field(description="User last name")
    full_name: str = strawberry.field(description="User full name")
    status: UserStatus = strawberry.field(description="User status")
    email_verified: bool = strawberry.field(description="Email verification status")
    created_at: datetime = strawberry.field(description="Creation timestamp")
    updated_at: datetime = strawberry.field(description="Last update timestamp")
