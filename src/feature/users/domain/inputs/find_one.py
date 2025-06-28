import strawberry
from typing import Optional
from src.shared.criteria.graphql_inputs import CriteriaInput


@strawberry.input
class UserFindOneInput:
    """COMPLETELY GENERIC user find one input - can search ANY field like NestJS"""

    # ===== DIRECT CRITERIA (LIKE NESTJS) =====
    criteria: Optional[CriteriaInput] = strawberry.field(default=None, description="Generic criteria for finding one user by ANY field")

    # ===== LEGACY SIMPLE FILTERS (DEPRECATED - for backward compatibility) =====
    user_id: Optional[str] = strawberry.field(default=None, description="[DEPRECATED] Find by user ID")
    email: Optional[str] = strawberry.field(default=None, description="[DEPRECATED] Find by email")
