# src/feature/users/domain/inputs/find_one.py
import strawberry
from typing import Optional, List
from src.shared.criteria.graphql_inputs import CriteriaInput


@strawberry.input
class UserFindOneInput:
    # ===== MODERN APPROACH (Recommended) =====
    criteria: Optional[CriteriaInput] = strawberry.field(default=None, description="Universal criteria - can search by ANY field")

    # ===== LEGACY FIELDS (Backward compatibility only) =====
    user_id: Optional[str] = strawberry.field(default=None, description="[LEGACY] Find by user ID")
    email: Optional[str] = strawberry.field(default=None, description="[LEGACY] Find by email")
