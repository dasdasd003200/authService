from abc import ABC, abstractmethod
from typing import Optional, List, TypeVar, Generic
from uuid import UUID

from src.core.domain.entities.base_entity import BaseEntity

T = TypeVar("T", bound=BaseEntity)


class BaseRepository(ABC, Generic[T]):
    @abstractmethod
    async def save(self, entity: T) -> T:
        pass

    @abstractmethod
    async def find_by_id(self, entity_id: UUID) -> Optional[T]:
        pass

    @abstractmethod
    async def delete(self, entity_id: UUID) -> bool:
        pass

    @abstractmethod
    async def exists_by_id(self, entity_id: UUID) -> bool:
        pass

    @abstractmethod
    async def find_with_criteria(self, criteria) -> List[T]:
        pass

    @abstractmethod
    async def find_one_with_criteria(self, criteria) -> Optional[T]:
        pass

    @abstractmethod
    async def count_with_criteria(self, criteria) -> int:
        pass
