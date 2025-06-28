# src/feature/users/domain/inputs/find.py
import strawberry
from typing import Optional, List
from src.shared.criteria.graphql_inputs import CriteriaInput


@strawberry.input
class UserFindInput:
    # ===== MODERN APPROACH (Recommended) =====
    criteria: Optional[CriteriaInput] = strawberry.field(default=None, description="Universal criteria - can filter ANY field, order, paginate")

    # ===== LEGACY FIELDS (Backward compatibility only) =====
    status: Optional[str] = strawberry.field(default=None, description="[LEGACY] Filter by status")
    email_verified: Optional[bool] = strawberry.field(default=None, description="[LEGACY] Filter by email verification")
    search_text: Optional[str] = strawberry.field(default=None, description="[LEGACY] Search in name/email")
    page: int = strawberry.field(default=1, description="[LEGACY] Page number")
    page_size: int = strawberry.field(default=10, description="[LEGACY] Items per page")
