# src/core/application/use_cases/base/delete_entity.py
"""
Base use case for deleting entities
"""

from typing import TypeVar, Generic

from src.core.domain.entities.base_entity import BaseEntity
from src.core.domain.repositories.base_repository import BaseRepository
from src.core.exceptions.base_exceptions import NotFoundError
from src.core.application.interfaces.base_use_case import BaseUseCase

from .commands import DeleteEntityCommand

T = TypeVar("T", bound=BaseEntity)


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
