import strawberry
from typing import Optional


@strawberry.input
class LoginInput:
    email: str = strawberry.field(description="User email address")
    password: str = strawberry.field(description="User password")
    remember_me: bool = strawberry.field(default=False, description="Extended session duration")
    device_info: Optional[str] = strawberry.field(default=None, description="Device information")
