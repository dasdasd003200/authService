import strawberry
from typing import TypeVar, Generic, Optional, Type, Callable
from uuid import UUID

from src.core.infrastructure.web.strawberry.decorators import (
    async_to_sync,
    safe_resolver,
)
from src.core.infrastructure.web.strawberry.base_query import BaseQuery
from src.core.infrastructure.web.strawberry.base_mutation import BaseMutation
from src.core.domain.repositories.base_repository import BaseRepository
from src.core.application.use_cases.base_crud_use_cases import (
    GetEntityByIdUseCase,
    GetEntityByIdQuery,
)

T = TypeVar("T")  # Entity type
U = TypeVar("U")  # GraphQL type
R = TypeVar("R")  # Repository type


class GenericEntityResolver(BaseQuery):
    """Generic resolver for entity operations"""

    def __init__(
        self,
        repository: BaseRepository[T],
        entity_to_graphql_converter: Callable[[T], U],
        entity_name: str = "Entity",
    ):
        self.repository = repository
        self.converter = entity_to_graphql_converter
        self.entity_name = entity_name

    @async_to_sync
    @safe_resolver(default_value=None)
    async def get_by_id(self, entity_id: str) -> Optional[U]:
        """Generic get by ID resolver"""
        use_case = GetEntityByIdUseCase(self.repository, self.entity_name)
        query = GetEntityByIdQuery(entity_id=UUID(entity_id))

        entity = await use_case.execute(query)
        return self.converter(entity) if entity else None
