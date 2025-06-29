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
        pass

    @abstractmethod
    async def find_active_sessions_by_user_id(self, user_id: UUID) -> List[Session]:
        pass

    @abstractmethod
    async def find_by_user_and_token_type(self, user_id: UUID, token_type: TokenType) -> List[Session]:
        pass

    @abstractmethod
    async def revoke_all_user_sessions(self, user_id: UUID) -> int:
        pass

    @abstractmethod
    async def revoke_user_sessions_by_type(self, user_id: UUID, token_type: TokenType) -> int:
        pass

    @abstractmethod
    async def cleanup_expired_sessions(self) -> int:
        pass

    @abstractmethod
    async def count_active_sessions_by_user(self, user_id: UUID) -> int:
        pass
