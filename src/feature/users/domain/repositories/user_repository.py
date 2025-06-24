from abc import abstractmethod
from typing import Optional
from uuid import UUID

from src.core.domain.value_objects.email import Email
from src.core.domain.repositories.base_repository import BaseRepository
from src.feature.users.domain.entities.user import User


class UserRepository(BaseRepository[User]):
    """User repository interface - with password management methods"""

    @abstractmethod
    async def find_by_email(self, email: Email) -> Optional[User]:
        """Find user by email"""
        pass

    @abstractmethod
    async def exists_by_email(self, email: Email) -> bool:
        """Check if user exists by email"""
        pass

    @abstractmethod
    async def save_with_password(self, entity: User, plain_password: str) -> User:
        """Save user entity with password using Django's hashing"""
        pass

    @abstractmethod
    async def verify_password(self, user_id: UUID, plain_password: str) -> bool:
        """Verify user password using Django's verification"""
        pass

    @abstractmethod
    async def change_password(self, user_id: UUID, new_plain_password: str) -> bool:
        """Change user password using Django's hashing"""
        pass
