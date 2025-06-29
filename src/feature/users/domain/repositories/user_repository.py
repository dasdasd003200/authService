from abc import abstractmethod
from typing import Optional
from uuid import UUID

from src.core.domain.value_objects.email import Email
from src.core.domain.repositories.base_repository import BaseRepository
from ..entities.user import User


class UserRepository(BaseRepository[User]):
    @abstractmethod
    async def save_with_password(self, user: User, password: str) -> User:
        pass

    @abstractmethod
    async def find_by_email(self, email: Email) -> Optional[User]:
        pass

    @abstractmethod
    async def exists_by_email(self, email: Email) -> bool:
        pass

    @abstractmethod
    async def delete_by_id(self, user_id: UUID) -> bool:
        pass

