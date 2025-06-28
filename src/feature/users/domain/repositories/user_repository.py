from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from src.core.domain.value_objects.email import Email
from src.core.domain.repositories.base_repository import BaseRepository
from ..entities.user import User


class UserRepository(BaseRepository[User]):
    """User repository interface - extends base repository with user-specific methods"""

    # ===== USER-SPECIFIC METHODS =====
    @abstractmethod
    async def save_with_password(self, user: User, password: str) -> User:
        """Save user with password (Django-specific)"""
        pass

    @abstractmethod
    async def find_by_email(self, email: Email) -> Optional[User]:
        """Find user by email"""
        pass

    @abstractmethod
    async def exists_by_email(self, email: Email) -> bool:
        """Check if user exists by email"""
        pass

    @abstractmethod
    async def delete_by_id(self, user_id: UUID) -> bool:
        """Delete user by ID"""
        pass
