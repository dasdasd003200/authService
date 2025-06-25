import strawberry
from typing import Optional


@strawberry.input
class UserUpdateInput:
    user_id: str = strawberry.field(description="User ID to update")
    first_name: Optional[str] = strawberry.field(default=None, description="New first name")
    last_name: Optional[str] = strawberry.field(default=None, description="New last name")
