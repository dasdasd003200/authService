from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from src.core.domain.value_objects.email import Email
from ..entities.user import User


class UserRepository(ABC):
    """User repository interface - Simplified and clean"""

    @abstractmethod
    async def save(self, user: User) -> User:
        """Save or update user"""
        pass

    @abstractmethod
    async def save_with_password(self, user: User, password: str) -> User:
        """Save user with password (for creation)"""
        pass

    @abstractmethod
    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Find user by ID"""
        pass

    @abstractmethod
    async def find_by_email(self, email: Email) -> Optional[User]:
        """Find user by email"""
        pass

    @abstractmethod
    async def find_by_criteria(self, criteria: List) -> List[User]:
        """Find users by criteria"""
        pass

    @abstractmethod
    async def count_by_criteria(self, criteria: List) -> int:
        """Count users by criteria"""
        pass

    @abstractmethod
    async def delete_by_id(self, user_id: UUID) -> bool:
        """Delete user by ID"""
        pass

    @abstractmethod
    async def exists_by_email(self, email: Email) -> bool:
        """Check if user exists by email"""
        pass

