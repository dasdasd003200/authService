# src/core/infrastructure/web/strawberry/types.py - LIMPIO
"""
Tipos base para GraphQL - SOLO LO GENÉRICO REUTILIZABLE
"""

import strawberry
from typing import Optional, List
from datetime import datetime
from enum import Enum


# ===== INPUT TYPES =====
@strawberry.input
class PaginationInput:
    """Standard pagination input"""

    page: int = strawberry.field(default=1, description="Page number (starts from 1)")
    page_size: int = strawberry.field(default=10, description="Items per page (max 100)")

    def __post_init__(self):
        if self.page < 1:
            self.page = 1
        if self.page_size < 1:
            self.page_size = 10
        if self.page_size > 100:
            self.page_size = 100


@strawberry.input
class DateRangeInput:
    """Standard date range input"""

    start_date: Optional[datetime] = strawberry.field(default=None, description="Start date")
    end_date: Optional[datetime] = strawberry.field(default=None, description="End date")


@strawberry.input
class SearchInput:
    """Standard search input"""

    query: Optional[str] = strawberry.field(default=None, description="Search term")
    pagination: Optional[PaginationInput] = strawberry.field(default=None, description="Pagination")
    date_range: Optional[DateRangeInput] = strawberry.field(default=None, description="Date filter")


# ===== OUTPUT TYPES =====
@strawberry.type
class PaginationInfo:
    """Standard pagination info"""

    current_page: int = strawberry.field(description="Current page number")
    page_size: int = strawberry.field(description="Items per page")
    total_items: int = strawberry.field(description="Total number of items")
    total_pages: int = strawberry.field(description="Total number of pages")
    has_next: bool = strawberry.field(description="Has next page")
    has_previous: bool = strawberry.field(description="Has previous page")


@strawberry.type
class BaseResponse:
    """Base response for all operations"""

    success: bool = strawberry.field(description="Operation success status")
    message: Optional[str] = strawberry.field(description="Human readable message")
    error_code: Optional[str] = strawberry.field(description="Error code for handling")


# ===== COMMON ENUMS =====
@strawberry.enum
class SortOrder(Enum):
    """Standard sort order"""

    ASC = "asc"
    DESC = "desc"


# ===== AUDIT FIELDS =====
@strawberry.type
class AuditFields:
    """Standard audit fields for entities"""

    created_at: Optional[datetime] = strawberry.field(description="Creation timestamp")
    updated_at: Optional[datetime] = strawberry.field(description="Last update timestamp")


# ===== ERROR TYPES =====
@strawberry.type
class FieldError:
    """Field-specific validation error"""

    field: str = strawberry.field(description="Field name")
    message: str = strawberry.field(description="Error message")


@strawberry.type
class ValidationErrorResponse(BaseResponse):
    """Response for validation errors"""

    field_errors: Optional[List[FieldError]] = strawberry.field(description="Field-specific errors", default=None)

