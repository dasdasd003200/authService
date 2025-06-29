# src/feature/sessions/domain/repositories/session_repository.py
from abc import abstractmethod
from typing import Optional, List
from uuid import UUID

from src.core.domain.repositories.base_repository import BaseRepository
from ..entities.session import Session
from ..value_objects.token_type import TokenType
from ..value_objects.session_status import SessionStatus


class SessionRepository(BaseRepository[Session]):
    @abstractmethod
    async def find_by_user_id(self, user_id: UUID) -> List[Session]:
        """Find all sessions for a user"""
        pass

    @abstractmethod
    async def find_active_sessions_by_user_id(self, user_id: UUID) -> List[Session]:
        """Find all active sessions for a user"""
        pass

    @abstractmethod
    async def find_by_user_and_token_type(self, user_id: UUID, token_type: TokenType) -> List[Session]:
        """Find sessions by user and token type"""
        pass

    @abstractmethod
    async def revoke_all_user_sessions(self, user_id: UUID) -> int:
        """Revoke all sessions for a user"""
        pass

    @abstractmethod
    async def revoke_user_sessions_by_type(self, user_id: UUID, token_type: TokenType) -> int:
        """Revoke sessions by user and token type"""
        pass

    @abstractmethod
    async def cleanup_expired_sessions(self) -> int:
        """Remove expired sessions"""
        pass

    @abstractmethod
    async def count_active_sessions_by_user(self, user_id: UUID) -> int:
        """Count active sessions for a user"""
        pass

