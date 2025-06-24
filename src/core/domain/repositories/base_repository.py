from abc import ABC, abstractmethod
from typing import Optional, List, TypeVar, Generic
from uuid import UUID

from src.core.domain.entities.base_entity import BaseEntity
from src.shared.criteria.base_criteria import BaseCriteria

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
    async def find_by_criteria(self, criteria: List[BaseCriteria]) -> List[T]:
        """Find entities by criteria"""
        pass

    @abstractmethod
    async def count_by_criteria(self, criteria: List[BaseCriteria]) -> int:
        """Count entities by criteria"""
        pass

    @abstractmethod
    async def delete(self, entity_id: UUID) -> bool:
        """Delete an entity (soft delete recommended)"""
        pass

    @abstractmethod
    async def exists_by_id(self, entity_id: UUID) -> bool:
        """Check if entity exists by ID"""
        pass
