import strawberry
from typing import Optional


@strawberry.input
class UserFindOneInput:
    user_id: Optional[str] = strawberry.field(default=None, description="Find by user ID")
    email: Optional[str] = strawberry.field(default=None, description="Find by email")
