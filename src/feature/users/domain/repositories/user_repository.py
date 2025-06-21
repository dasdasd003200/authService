# src/feature/users/domain/repositories/user_repository.py - SIMPLIFIED
from abc import abstractmethod
from typing import Optional

from src.core.domain.value_objects.email import Email
from src.core.domain.repositories.base_repository import BaseRepository
from src.feature.users.domain.entities.user import User


class UserRepository(BaseRepository[User]):
    """User repository interface - now inherits common CRUD operations"""

    # Only need to define user-specific methods
    @abstractmethod
    async def find_by_email(self, email: Email) -> Optional[User]:
        """Find user by email"""
        pass

    @abstractmethod
    async def exists_by_email(self, email: Email) -> bool:
        """Check if user exists by email"""
        pass
