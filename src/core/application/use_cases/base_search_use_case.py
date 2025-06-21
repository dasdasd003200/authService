# src/core/application/use_cases/base_search_use_case.py - FIXED CRITICAL
from dataclasses import dataclass
from typing import Generic, TypeVar, Optional
from datetime import datetime

from src.core.domain.entities.base_entity import BaseEntity
from src.core.domain.repositories.base_repository import BaseRepository
from src.core.domain.repositories.criteria.base_criteria import CriteriaBuilder
from src.core.domain.repositories.criteria.date_range_criteria import DateRangeCriteria
from src.core.application.dto.pagination import PaginationRequest, PaginatedResult
from src.core.application.interfaces.base_use_case import BaseUseCase

T = TypeVar("T", bound=BaseEntity)


@dataclass
class BaseSearchQuery:
    """Base search query with common filters"""

    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    pagination: Optional[PaginationRequest] = None

    def __post_init__(self):
        if self.pagination is None:
            self.pagination = PaginationRequest()


class BaseSearchUseCase(BaseUseCase[BaseSearchQuery, PaginatedResult[T]], Generic[T]):
    """Base use case for searching entities with pagination"""

    def __init__(self, repository: BaseRepository[T]):
        self.repository = repository

    async def execute(self, query: BaseSearchQuery) -> PaginatedResult[T]:
        """Execute search with base criteria"""
        criteria_builder = CriteriaBuilder()

        # Add date range criteria if provided
        if query.created_after or query.created_before:
            criteria_builder.add(
                DateRangeCriteria(
                    field_name="created_at",
                    start_date=query.created_after,
                    end_date=query.created_before,
                )
            )

        # Add custom criteria (override in subclasses)
        self._add_custom_criteria(criteria_builder, query)

        # Get criteria for count (without pagination)
        count_criteria = criteria_builder.build()

        # FIXED: Ensure pagination is not None
        pagination = query.pagination or PaginationRequest()

        # Add pagination
        from src.core.domain.repositories.criteria.pagination_criteria import (
            PaginationCriteria,
        )

        criteria_builder.add(PaginationCriteria(pagination.limit, pagination.offset))
        search_criteria = criteria_builder.build()

        # Execute queries
        entities = await self.repository.find_by_criteria(search_criteria)
        total_count = await self.repository.count_by_criteria(count_criteria)

        # Return paginated result
        return PaginatedResult.create(
            items=entities,
            page=pagination.page,
            page_size=pagination.page_size,
            total_items=total_count,
        )

    def _add_custom_criteria(
        self, criteria_builder: CriteriaBuilder, query: BaseSearchQuery
    ):
        """Override in subclasses to add custom search criteria"""
        pass

