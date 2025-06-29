# src/feature/sessions/application/use_cases/session_use_cases.py
from typing import Optional, Tuple
from uuid import UUID

from src.core.application.use_cases.base_crud_use_cases import BaseCrudUseCases
from src.core.domain.value_objects.email import Email
from src.core.exceptions.base_exceptions import ValidationException, NotFoundError, UnauthorizedError
from src.feature.users.domain.repositories.user_repository import UserRepository
from ...domain.entities.session import Session
from ...domain.repositories.session_repository import SessionRepository
from ...domain.value_objects.token_type import TokenType


class SessionUseCases(BaseCrudUseCases[Session]):
    def __init__(self, session_repository: SessionRepository, user_repository: UserRepository):
        super().__init__(session_repository, "Session")
        self.session_repository = session_repository
        self.user_repository = user_repository

    async def authenticate_user(self, email: str, password: str, remember_me: bool = False, ip_address: Optional[str] = None, user_agent: Optional[str] = None, device_info: Optional[str] = None) -> Tuple[Session, Session]:  # (access_session, refresh_session)
        """
        Authenticate user and create sessions
        Returns tuple of (access_session, refresh_session)
        """
        if not email or not password:
            raise ValidationException("Email and password are required")

        # Find user by email
        email_vo = Email(email)
        user = await self.user_repository.find_by_email(email_vo)
        if not user:
            raise UnauthorizedError("Invalid email or password")

        # Validate user status
        if not user.is_active:
            raise UnauthorizedError("Account is not active")

        # TODO: Add password verification here
        # For now, assuming password is valid
        # In real implementation: check password hash

        # Create sessions
        access_duration = 60 if not remember_me else 720  # 1 hour vs 12 hours
        refresh_duration = 7 if not remember_me else 30  # 7 days vs 30 days

        access_session = Session.create_access_token_session(user_id=user.id, duration_minutes=access_duration, ip_address=ip_address, user_agent=user_agent)
        access_session.device_info = device_info

        refresh_session = Session.create_refresh_token_session(user_id=user.id, duration_days=refresh_duration, ip_address=ip_address, user_agent=user_agent)
        refresh_session.device_info = device_info

        # Save sessions
        access_session = await self.session_repository.save(access_session)
        refresh_session = await self.session_repository.save(refresh_session)

        return access_session, refresh_session

    async def refresh_access_token(self, refresh_token_id: UUID) -> Session:
        """
        Create new access token using refresh token
        """
        refresh_session = await self.session_repository.find_by_id(refresh_token_id)
        if not refresh_session:
            raise NotFoundError("Refresh token not found")

        if not refresh_session.is_active:
            raise UnauthorizedError("Refresh token is invalid or expired")

        if refresh_session.token_type != TokenType.REFRESH:
            raise ValidationException("Invalid token type for refresh operation")

        # Create new access token
        access_session = Session.create_access_token_session(user_id=refresh_session.user_id, ip_address=refresh_session.ip_address, user_agent=refresh_session.user_agent)
        access_session.device_info = refresh_session.device_info

        return await self.session_repository.save(access_session)

    async def logout_session(self, session_id: UUID) -> bool:
        """
        Logout specific session
        """
        session = await self.session_repository.find_by_id(session_id)
        if not session:
            raise NotFoundError(f"Session with ID {session_id} not found")

        session.logout()
        await self.session_repository.save(session)
        return True

    async def logout_all_user_sessions(self, user_id: UUID) -> int:
        """
        Logout all sessions for a user
        """
        return await self.session_repository.revoke_all_user_sessions(user_id)

    async def validate_session(self, session_id: UUID) -> Session:
        """
        Validate and return session if active
        """
        session = await self.session_repository.find_by_id(session_id)
        if not session:
            raise NotFoundError("Session not found")

        if not session.is_active:
            raise UnauthorizedError("Session is invalid or expired")

        return session

    async def get_user_active_sessions(self, user_id: UUID) -> list[Session]:
        """
        Get all active sessions for a user
        """
        return await self.session_repository.find_active_sessions_by_user_id(user_id)

    async def cleanup_expired_sessions(self) -> int:
        """
        Remove expired sessions (maintenance task)
        """
        return await self.session_repository.cleanup_expired_sessions()

