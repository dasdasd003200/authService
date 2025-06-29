# src/feature/sessions/infrastructure/services/auth_service.py
from uuid import UUID
from typing import Dict, Any, Optional

from src.core.infrastructure.web.strawberry.services.base_service import BaseService
from src.core.infrastructure.web.strawberry.responses import FindData, FindOneData
from src.shared.criteria.service_helper import CriteriaServiceHelper
from src.feature.users.domain.repositories.user_repository import UserRepository
from ...application.use_cases.session_use_cases import SessionUseCases
from ...domain.inputs.login import LoginInput
from ...domain.inputs.refresh import RefreshTokenInput
from ...domain.inputs.logout import LogoutInput
from ...domain.inputs.find import SessionFindInput
from ...domain.inputs.find_one import SessionFindOneInput
from ...domain.types.standard_responses import LoginResponse, RefreshTokenResponse, LogoutResponse, SessionFindResponse, SessionFindOneResponse
from ...domain.schemes.session import SessionGraphQLType, AuthResponse
from ...domain.schemes.session_fields import SessionFields
from src.core.exceptions.base_exceptions import BaseDomainException
from src.core.infrastructure.web.strawberry.helpers.validators import validate_uuid
from .jwt_service import JWTService


class AuthService(BaseService):
    def __init__(self, session_use_cases: SessionUseCases, user_repository: UserRepository):
        super().__init__("Session")
        self.session_use_cases = session_use_cases
        self.user_repository = user_repository
        self.jwt_service = JWTService()
        self.criteria_helper = CriteriaServiceHelper(feature_name="session", search_fields=["user_agent", "device_info"], boolean_fields=["is_active", "is_expired"], string_fields=["status", "token_type", "ip_address"])

    # ===== AUTH OPERATIONS =====

    async def login(self, input: LoginInput, request_info: Dict[str, Any] = None) -> LoginResponse:
        """Handle user login"""
        try:
            # Extract request info
            ip_address = request_info.get("ip_address") if request_info else None
            user_agent = request_info.get("user_agent") if request_info else None

            # Convert input to use case args
            login_args = SessionFields.login_args(input)
            login_args.update({"ip_address": ip_address, "user_agent": user_agent})

            # Authenticate and create sessions
            access_session, refresh_session = await self.session_use_cases.authenticate_user(**login_args)

            # Get user for email (needed for JWT)
            user = await self.user_repository.find_by_id(access_session.user_id)
            if not user:
                return LoginResponse(success=False, message="Authentication failed", error_code="USER_NOT_FOUND")

            # Generate JWT tokens
            token_data = self.jwt_service.generate_token_pair(access_session, refresh_session, str(user.email))

            # Build response
            auth_response = AuthResponse(access_token=token_data["access_token"], refresh_token=token_data["refresh_token"], expires_in=token_data["expires_in"], token_type=token_data["token_type"], user_id=token_data["user_id"], user_email=token_data["user_email"], session_id=token_data["session_id"])

            return LoginResponse(success=True, data=auth_response, message="Login successful")

        except BaseDomainException as e:
            return LoginResponse(success=False, message=e.message, error_code=e.error_code)

    async def refresh_token(self, input: RefreshTokenInput) -> RefreshTokenResponse:
        """Handle token refresh"""
        try:
            # Extract session ID from refresh token
            refresh_token = input.refresh_token
            session_id = self.jwt_service.extract_session_id(refresh_token)

            # Validate refresh token type
            if not self.jwt_service.validate_token_type(refresh_token, "refresh"):
                return RefreshTokenResponse(success=False, message="Invalid token type", error_code="INVALID_TOKEN_TYPE")

            # Create new access token
            new_access_session = await self.session_use_cases.refresh_access_token(session_id)

            # Get user for email
            user = await self.user_repository.find_by_id(new_access_session.user_id)
            if not user:
                return RefreshTokenResponse(success=False, message="User not found", error_code="USER_NOT_FOUND")

            # Generate new access token
            token_data = self.jwt_service.generate_access_token(new_access_session, str(user.email))

            # Build response (keep same refresh token)
            auth_response = AuthResponse(
                access_token=token_data["access_token"],
                refresh_token=refresh_token,  # Keep original refresh token
                expires_in=token_data["expires_in"],
                token_type=token_data["token_type"],
                user_id=token_data["user_id"],
                user_email=token_data["user_email"],
                session_id=token_data["session_id"],
            )

            return RefreshTokenResponse(success=True, data=auth_response, message="Token refreshed successfully")

        except BaseDomainException as e:
            return RefreshTokenResponse(success=False, message=e.message, error_code=e.error_code)

    async def logout(self, input: LogoutInput, user_context: Dict[str, Any]) -> LogoutResponse:
        """Handle user logout"""
        try:
            logout_args = SessionFields.logout_args(input)

            if logout_args["logout_all"]:
                # Logout all sessions for user
                user_id = user_context.get("user_id")
                if not user_id:
                    return LogoutResponse(success=False, message="User context required for logout all", error_code="USER_CONTEXT_REQUIRED")

                affected_count = await self.session_use_cases.logout_all_user_sessions(UUID(user_id))
                return LogoutResponse(success=True, message=f"Logged out from {affected_count} sessions", sessions_affected=affected_count)

            elif logout_args["session_id"]:
                # Logout specific session
                session_uuid = validate_uuid(logout_args["session_id"], "Session ID")
                await self.session_use_cases.logout_session(session_uuid)
                return LogoutResponse(success=True, message="Logged out successfully", sessions_affected=1)

            else:
                return LogoutResponse(success=False, message="Either session_id or logout_all must be specified", error_code="INVALID_LOGOUT_REQUEST")

        except BaseDomainException as e:
            return LogoutResponse(success=False, message=e.message, error_code=e.error_code)

    # ===== CRUD OPERATIONS =====

    async def find(self, input: SessionFindInput) -> SessionFindResponse:
        """Find sessions with criteria"""
        try:
            prepare = self.criteria_helper.build_find_prepare(input)
            sessions, total_count = await self.session_use_cases.find_with_criteria(prepare)

            session_graphql_list = SessionGraphQLType.from_entities(sessions)
            response_data = self.handle_success_find(session_graphql_list, total_count)

            return SessionFindResponse(success=response_data["success"], data=FindData(items=response_data["data"]), total_count=response_data["total_count"], message=response_data["message"])
        except BaseDomainException as e:
            error_data = self.handle_exception(e, [])
            return SessionFindResponse(success=error_data["success"], data=FindData(items=error_data["data"]), total_count=0, message=error_data["message"], error_code=error_data["error_code"])

    async def find_one(self, input: SessionFindOneInput) -> SessionFindOneResponse:
        """Find one session with criteria"""
        try:
            prepare = self.criteria_helper.build_find_one_prepare(input)
            session = await self.session_use_cases.find_one_with_criteria(prepare)

            session_graphql = SessionGraphQLType.from_entity(session) if session else None
            response_data = self.handle_success_find_one(session_graphql)

            return SessionFindOneResponse(success=response_data["success"], data=FindOneData(item=response_data["data"]), message=response_data["message"])
        except BaseDomainException as e:
            error_data = self.handle_exception(e, None)
            return SessionFindOneResponse(success=error_data["success"], data=FindOneData(item=error_data["data"]), message=error_data["message"], error_code=error_data["error_code"])
