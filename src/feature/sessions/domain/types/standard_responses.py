# src/feature/sessions/domain/types/standard_responses.py
import strawberry
from typing import Optional
from src.core.infrastructure.web.strawberry.responses import CreateResponse, UpdateResponse, DeleteResponse, FindResponse, FindOneResponse
from ..schemes.session import SessionGraphQLType, AuthResponse


# Standard CRUD responses for sessions
SessionCreateResponse = CreateResponse[SessionGraphQLType]
SessionUpdateResponse = UpdateResponse[SessionGraphQLType]
SessionDeleteResponse = DeleteResponse
SessionFindResponse = FindResponse[SessionGraphQLType]
SessionFindOneResponse = FindOneResponse[SessionGraphQLType]


# ===== AUTH-SPECIFIC RESPONSES =====


@strawberry.type
class LoginResponse:
    success: bool = strawberry.field(description="Operation success status")
    data: Optional[AuthResponse] = strawberry.field(default=None, description="Authentication data")
    message: Optional[str] = strawberry.field(default=None, description="Response message")
    error_code: Optional[str] = strawberry.field(default=None, description="Error code if failed")


@strawberry.type
class RefreshTokenResponse:
    success: bool = strawberry.field(description="Operation success status")
    data: Optional[AuthResponse] = strawberry.field(default=None, description="New authentication data")
    message: Optional[str] = strawberry.field(default=None, description="Response message")
    error_code: Optional[str] = strawberry.field(default=None, description="Error code if failed")


@strawberry.type
class LogoutResponse:
    success: bool = strawberry.field(description="Operation success status")
    message: Optional[str] = strawberry.field(default=None, description="Response message")
    error_code: Optional[str] = strawberry.field(default=None, description="Error code if failed")
    sessions_affected: Optional[int] = strawberry.field(default=None, description="Number of sessions that were logged out")
