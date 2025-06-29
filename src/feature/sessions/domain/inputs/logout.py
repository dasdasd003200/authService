import strawberry
from typing import Optional


@strawberry.input
class LogoutInput:
    session_id: Optional[str] = strawberry.field(default=None, description="Specific session ID to logout (optional)")
    logout_all: bool = strawberry.field(default=False, description="Logout from all sessions")
