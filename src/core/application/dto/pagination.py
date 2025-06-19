# src/core/application/dto/pagination.py
from dataclasses import dataclass
from typing import Generic, TypeVar, List

T = TypeVar("T")


@dataclass
class PaginationRequest:
    """Request for pagination"""

    page: int = 1
    page_size: int = 10

    def __post_init__(self):
        if self.page < 1:
            self.page = 1
        if self.page_size < 1:
            self.page_size = 10
        if self.page_size > 100:  # Max page size
            self.page_size = 100

    @property
    def offset(self) -> int:
        """Calculate offset from page and page_size"""
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        """Get limit (same as page_size)"""
        return self.page_size


@dataclass
class PaginationInfo:
    """Pagination information"""

    current_page: int
    page_size: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool

    @classmethod
    def create(cls, page: int, page_size: int, total_items: int) -> "PaginationInfo":
        """Create pagination info from basic parameters"""
        total_pages = (total_items + page_size - 1) // page_size  # Ceiling division
        return cls(
            current_page=page,
            page_size=page_size,
            total_items=total_items,
            total_pages=total_pages,
            has_next=page < total_pages,
            has_previous=page > 1,
        )


@dataclass
class PaginatedResult(Generic[T]):
    """Generic paginated result"""

    items: List[T]
    pagination: PaginationInfo

    @classmethod
    def create(
        cls, items: List[T], page: int, page_size: int, total_items: int
    ) -> "PaginatedResult[T]":
        """Create paginated result"""
        pagination = PaginationInfo.create(page, page_size, total_items)
        return cls(items=items, pagination=pagination)
