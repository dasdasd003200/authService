# src/core/domain/repositories/base_repository.py - MÉTODOS COMPLETOS
from abc import ABC, abstractmethod
from typing import Optional, List, TypeVar, Generic, Dict, Any
from uuid import UUID

from src.core.domain.entities.base_entity import BaseEntity
from src.core.domain.repositories.criteria.base_criteria import BaseCriteria

T = TypeVar("T", bound=BaseEntity)


class BaseRepository(ABC, Generic[T]):
    """Base repository interface - OPERACIONES CRUD COMPLETAS"""

    # ===== CREATE OPERATIONS =====
    @abstractmethod
    async def save(self, entity: T) -> T:
        """Save (create or update) single entity"""
        pass

    @abstractmethod
    async def save_many(self, entities: List[T]) -> List[T]:
        """Bulk save multiple entities"""
        pass

    # ===== READ OPERATIONS =====
    @abstractmethod
    async def find_by_id(self, entity_id: UUID) -> Optional[T]:
        """Find single entity by ID"""
        pass

    @abstractmethod
    async def find_by_criteria(self, criteria: List[BaseCriteria]) -> List[T]:
        """Find multiple entities by criteria"""
        pass

    @abstractmethod
    async def find_first(self, criteria: List[BaseCriteria]) -> Optional[T]:
        """Find first entity matching criteria"""
        pass

    @abstractmethod
    async def find_all(self) -> List[T]:
        """Find all entities (use with pagination for large datasets)"""
        pass

    # ===== UPDATE OPERATIONS =====
    @abstractmethod
    async def update_by_id(self, entity_id: UUID, updates: Dict[str, Any]) -> Optional[T]:
        """Update specific fields by ID without loading full entity"""
        pass

    @abstractmethod
    async def update_many(self, entity_ids: List[UUID], updates: Dict[str, Any]) -> int:
        """Bulk update multiple entities, returns count of updated"""
        pass

    # ===== DELETE OPERATIONS =====
    @abstractmethod
    async def delete_by_id(self, entity_id: UUID) -> bool:
        """Delete single entity by ID"""
        pass

    @abstractmethod
    async def delete_many(self, entity_ids: List[UUID]) -> int:
        """Bulk delete multiple entities, returns count of deleted"""
        pass

    @abstractmethod
    async def delete_by_criteria(self, criteria: List[BaseCriteria]) -> int:
        """Delete multiple entities by criteria, returns count of deleted"""
        pass

    # ===== QUERY OPERATIONS =====
    @abstractmethod
    async def count_by_criteria(self, criteria: List[BaseCriteria]) -> int:
        """Count entities matching criteria"""
        pass

    @abstractmethod
    async def exists_by_id(self, entity_id: UUID) -> bool:
        """Check if entity exists by ID"""
        pass

    @abstractmethod
    async def exists_by_criteria(self, criteria: List[BaseCriteria]) -> bool:
        """Check if any entity exists matching criteria"""
        pass

    # ===== LEGACY METHODS (mantener compatibilidad) =====
    async def delete(self, entity_id: UUID) -> bool:
        """Legacy delete method - delegates to delete_by_id"""
        return await self.delete_by_id(entity_id)
