from abc import ABC, abstractmethod
from typing import Optional, List, TypeVar, Generic
from uuid import UUID

from src.core.domain.entities.base_entity import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class BaseRepository(ABC, Generic[T]):
    """Base repository interface for all entities"""

    @abstractmethod
    async def save(self, entity: T) -> T:
        """Save or update an entity"""
        pass

    @abstractmethod
    async def find_by_id(self, entity_id: UUID) -> Optional[T]:
        """Find entity by ID"""
        pass

    @abstractmethod
    async def delete(self, entity_id: UUID) -> bool:
        """Delete an entity (soft delete recommended)"""
        pass

    @abstractmethod
    async def exists_by_id(self, entity_id: UUID) -> bool:
        """Check if entity exists by ID"""
        pass

    # ===== NEW METHODS FOR GENERIC CRITERIA =====
    @abstractmethod
    async def find_with_criteria(self, criteria) -> List[T]:
        """Find entities using generic Criteria"""
        pass

    @abstractmethod
    async def find_one_with_criteria(self, criteria) -> Optional[T]:
        """Find one entity using generic Criteria"""
        pass

    @abstractmethod
    async def count_with_criteria(self, criteria) -> int:
        """Count entities using generic Criteria"""
        pass
