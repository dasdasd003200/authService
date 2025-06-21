from abc import abstractmethod
from dataclasses import dataclass
from typing import TypeVar, Generic, Optional, List
from uuid import UUID

from src.core.domain.entities.base_entity import BaseEntity
from src.core.domain.repositories.base_repository import BaseRepository
from src.core.exceptions.base_exceptions import NotFoundError
from src.core.application.interfaces.base_use_case import BaseUseCase

T = TypeVar("T", bound=BaseEntity)
TRepository = TypeVar("TRepository", bound=BaseRepository)


@dataclass
class GetEntityByIdQuery:
    """Generic query for getting entity by ID"""

    entity_id: UUID


@dataclass
class DeleteEntityCommand:
    """Generic command for deleting entity"""

    entity_id: UUID


class GetEntityByIdUseCase(BaseUseCase[GetEntityByIdQuery, Optional[T]], Generic[T]):
    """Base use case for getting entity by ID"""

    def __init__(self, repository: BaseRepository[T], entity_name: str = "Entity"):
        self.repository = repository
        self.entity_name = entity_name

    async def execute(self, query: GetEntityByIdQuery) -> Optional[T]:
        """Execute get entity by ID"""
        entity = await self.repository.find_by_id(query.entity_id)

        if not entity:
            raise NotFoundError(
                f"{self.entity_name} with ID {query.entity_id} not found",
                error_code=f"{self.entity_name.upper()}_NOT_FOUND",
            )

        return entity


class DeleteEntityUseCase(BaseUseCase[DeleteEntityCommand, bool], Generic[T]):
    """Base use case for deleting entity"""

    def __init__(self, repository: BaseRepository[T], entity_name: str = "Entity"):
        self.repository = repository
        self.entity_name = entity_name

    async def execute(self, command: DeleteEntityCommand) -> bool:
        """Execute delete entity"""
        # Check if entity exists first
        entity = await self.repository.find_by_id(command.entity_id)
        if not entity:
            raise NotFoundError(
                f"{self.entity_name} with ID {command.entity_id} not found",
                error_code=f"{self.entity_name.upper()}_NOT_FOUND",
            )

        return await self.repository.delete(command.entity_id)
