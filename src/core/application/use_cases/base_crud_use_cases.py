# src/core/application/use_cases/base_crud_use_cases.py
from typing import List, Optional, Tuple, TypeVar, Generic
from uuid import UUID

from src.core.domain.entities.base_entity import BaseEntity
from src.core.domain.repositories.base_repository import BaseRepository
from src.core.exceptions.base_exceptions import NotFoundError
from src.shared.criteria.prepare import PrepareFind, PrepareFindOne
from src.shared.criteria.base_criteria import Criteria

T = TypeVar("T", bound=BaseEntity)


class BaseCrudUseCases(Generic[T]):
    def __init__(self, repository: BaseRepository[T], entity_name: str):
        self.repository = repository
        self.entity_name = entity_name

    async def find_with_criteria(self, prepare: PrepareFind) -> Tuple[List[T], int]:
        entities = await self.repository.find_with_criteria(prepare.criteria)

        count_criteria = Criteria(
            filters=prepare.criteria.filters,
            orders=prepare.criteria.orders,
            projection=prepare.criteria.projection,
            options=prepare.criteria.options,
        )
        total_count = await self.repository.count_with_criteria(count_criteria)
        return entities, total_count

    async def find_one_with_criteria(self, prepare: PrepareFindOne) -> Optional[T]:
        return await self.repository.find_one_with_criteria(prepare.criteria)

    async def delete_by_id(self, entity_id: UUID) -> bool:
        entity = await self.repository.find_by_id(entity_id)
        if not entity:
            raise NotFoundError(f"{self.entity_name} with ID {entity_id} not found")
        return await self.repository.delete(entity_id)
