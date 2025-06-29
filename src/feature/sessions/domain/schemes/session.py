import strawberry
from datetime import datetime
from typing import Optional
from ..value_objects.token_type import TokenType
from ..value_objects.session_status import SessionStatus


@strawberry.type
class SessionGraphQLType:
    id: str = strawberry.field(description="Unique session identifier")
    user_id: str = strawberry.field(name="userId", description="User identifier")

    token_type: TokenType = strawberry.field(name="tokenType", description="Token type (access/refresh)")
    status: SessionStatus = strawberry.field(description="Session status")

    expires_at: datetime = strawberry.field(name="expiresAt", description="Session expiration time")
    is_active: bool = strawberry.field(name="isActive", description="Whether session is currently active")
    is_expired: bool = strawberry.field(name="isExpired", description="Whether session has expired")

    ip_address: Optional[str] = strawberry.field(name="ipAddress", default=None, description="IP address")
    user_agent: Optional[str] = strawberry.field(name="userAgent", default=None, description="User agent string")
    device_info: Optional[str] = strawberry.field(name="deviceInfo", default=None, description="Device information")

    created_at: datetime = strawberry.field(name="createdAt", description="Creation timestamp")
    updated_at: datetime = strawberry.field(name="updatedAt", description="Last update timestamp")

    @classmethod
    def from_entity(cls, session) -> "SessionGraphQLType":
        return cls(
            id=str(session.id),
            user_id=str(session.user_id),
            token_type=session.token_type,
            status=session.status,
            expires_at=session.expires_at,
            is_active=session.is_active,
            is_expired=session.is_expired,
            ip_address=session.ip_address,
            user_agent=session.user_agent,
            device_info=session.device_info,
            created_at=session.created_at,
            updated_at=session.updated_at,
        )

    @classmethod
    def from_entities(cls, sessions) -> list["SessionGraphQLType"]:
        return [cls.from_entity(session) for session in sessions]


@strawberry.type
class AuthResponse:
    access_token: str = strawberry.field(name="accessToken", description="JWT access token")
    refresh_token: str = strawberry.field(name="refreshToken", description="JWT refresh token")
    expires_in: int = strawberry.field(name="expiresIn", description="Access token expiration in seconds")
    token_type: str = strawberry.field(name="tokenType", default="Bearer", description="Token type")

    user_id: str = strawberry.field(name="userId", description="Authenticated user ID")
    user_email: str = strawberry.field(name="userEmail", description="Authenticated user email")
    session_id: str = strawberry.field(name="sessionId", description="Session identifier")
