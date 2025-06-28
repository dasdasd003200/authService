import strawberry
from typing import Optional, List
from src.shared.criteria.graphql_inputs import CriteriaInput


@strawberry.input
class UserFindInput:
    """COMPLETELY GENERIC user find input - can search ANY field like NestJS"""

    # ===== DIRECT CRITERIA (LIKE NESTJS) =====
    criteria: Optional[CriteriaInput] = strawberry.field(default=None, description="Generic criteria for filtering ANY field, ordering, and pagination")

    # ===== LEGACY SIMPLE FILTERS (DEPRECATED - for backward compatibility) =====
    status: Optional[str] = strawberry.field(default=None, description="[DEPRECATED] Filter by status")
    email_verified: Optional[bool] = strawberry.field(default=None, description="[DEPRECATED] Filter by email verification")
    search_text: Optional[str] = strawberry.field(default=None, description="[DEPRECATED] Search in name/email")
    page: int = strawberry.field(default=1, description="[DEPRECATED] Page number")
    page_size: int = strawberry.field(default=10, description="[DEPRECATED] Items per page")
    order_by: Optional[List[str]] = strawberry.field(default=None, description="[DEPRECATED] Order by fields")
