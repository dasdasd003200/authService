# src/feature/users/application/use_cases/search_users.py - FIXED CRITICAL
from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from src.core.application.use_cases.base_search_use_case import (
    BaseSearchUseCase,
    BaseSearchQuery,
)
from src.core.domain.repositories.criteria.factory import CriteriaFactory
from src.core.domain.repositories.criteria.base_criteria import CriteriaBuilder
from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.entities.user import User


@dataclass
class SearchUsersQuery(BaseSearchQuery):
    """Query for searching users - extends base with user-specific filters"""

    status: Optional[str] = None
    email_verified: Optional[bool] = None
    search_text: Optional[str] = None  # Search in name/email


@dataclass
class UserSearchResult:
    """Single user result"""

    user_id: str
    email: str
    first_name: str
    last_name: str
    full_name: str
    status: str
    email_verified: bool
    created_at: datetime


class SearchUsersUseCase(BaseSearchUseCase[User]):
    """Use case for searching users - much simpler now!"""

    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository)

    def _add_custom_criteria(self, criteria_builder: CriteriaBuilder, query: BaseSearchQuery):
        """Add user-specific search criteria"""
        # FIXED: Type cast correctly
        if not isinstance(query, SearchUsersQuery):
            return

        # Status filter
        if query.status:
            criteria_builder.add(CriteriaFactory.status(query.status))

        # Email verification filter
        if query.email_verified is not None:
            criteria_builder.add(CriteriaFactory.boolean_field("email_verified", query.email_verified))

        # Text search in name and email
        if query.search_text:
            criteria_builder.add(CriteriaFactory.text_search(query.search_text, ["first_name", "last_name", "email"]))

    def _convert_entities_to_results(self, users: list[User]) -> list[UserSearchResult]:
        """Convert domain entities to result objects"""
        return [
            UserSearchResult(
                user_id=str(user.id),
                email=str(user.email),
                first_name=user.first_name,
                last_name=user.last_name,
                full_name=user.full_name,
                status=user.status.value,
                email_verified=user.email_verified,
                created_at=user.created_at,
            )
            for user in users
        ]
