import strawberry
from typing import TypeVar, Type, Optional, List

from src.core.infrastructure.web.strawberry.types import BaseResponse, PaginationInfo

T = TypeVar("T")


def create_entity_response_type(entity_type: Type[T], name: str):
    """Factory to create response types for entities"""

    @strawberry.type(name=name)
    class EntityResponse(BaseResponse):
        data: Optional[entity_type] = strawberry.field(
            description="The operation result data"
        )

    return EntityResponse


def create_paginated_response_type(entity_type: Type[T], name: str):
    """Factory to create paginated response types"""

    @strawberry.type(name=name)
    class PaginatedResponse:
        items: List[entity_type] = strawberry.field(description="List of items")
        pagination: PaginationInfo = strawberry.field(
            description="Pagination information"
        )

    return PaginatedResponse


def create_simple_response_type(name: str):
    """Factory to create simple boolean response types"""

    @strawberry.type(name=name)
    class SimpleResponse(BaseResponse):
        pass

    return SimpleResponse
