# src/feature/users/application/use_cases/search_users.py
from dataclasses import dataclass
from typing import List, Optional
from datetime import datetime

from src.core.domain.repositories.criteria.base_criteria import CriteriaBuilder
from src.core.domain.repositories.criteria.date_range_criteria import DateRangeCriteria
from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.value_objects.user_status import UserStatus


@dataclass
class SearchUsersQuery:
    """Query for searching users"""

    status: Optional[str] = None
    email_verified: Optional[bool] = None
    created_after: Optional[datetime] = None
    created_before: Optional[datetime] = None
    limit: int = 10
    offset: int = 0


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


@dataclass
class SearchUsersResult:
    """Result of searching users"""

    users: List[UserSearchResult]
    total_count: int
    has_next: bool
    has_previous: bool


class UserStatusCriteria:
    """Criteria for filtering by user status"""

    def __init__(self, status: UserStatus):
        self.status = status

    def apply(self, queryset):
        return queryset.filter(status=self.status.value)

    def to_dict(self):
        return {"type": "user_status", "status": self.status.value}


class EmailVerifiedCriteria:
    """Criteria for filtering by email verification"""

    def __init__(self, email_verified: bool):
        self.email_verified = email_verified

    def apply(self, queryset):
        return queryset.filter(email_verified=self.email_verified)

    def to_dict(self):
        return {"type": "email_verified", "email_verified": self.email_verified}


class PaginationCriteria:
    """Criteria for pagination"""

    def __init__(self, limit: int, offset: int):
        self.limit = limit
        self.offset = offset

    def apply(self, queryset):
        return queryset[self.offset : self.offset + self.limit]

    def to_dict(self):
        return {"type": "pagination", "limit": self.limit, "offset": self.offset}


class SearchUsersUseCase:
    """Use case for searching users with filters and pagination"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, query: SearchUsersQuery) -> SearchUsersResult:
        """Search users with criteria"""

        # Build criteria
        criteria_builder = CriteriaBuilder()

        # Status filter
        if query.status:
            status = UserStatus.from_string(query.status)
            criteria_builder.add(UserStatusCriteria(status))

        # Email verification filter
        if query.email_verified is not None:
            criteria_builder.add(EmailVerifiedCriteria(query.email_verified))

        # Date range filter
        if query.created_after or query.created_before:
            criteria_builder.add(
                DateRangeCriteria(
                    field_name="created_at",
                    start_date=query.created_after,
                    end_date=query.created_before,
                )
            )

        # Get criteria for count (without pagination)
        count_criteria = criteria_builder.build()

        # Add pagination
        criteria_builder.add(PaginationCriteria(query.limit, query.offset))
        search_criteria = criteria_builder.build()

        # Execute queries
        users = await self.user_repository.find_by_criteria(search_criteria)
        total_count = await self.user_repository.count_by_criteria(count_criteria)

        # Convert to results
        user_results = [
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

        # Calculate pagination info
        has_next = (query.offset + query.limit) < total_count
        has_previous = query.offset > 0

        return SearchUsersResult(
            users=user_results,
            total_count=total_count,
            has_next=has_next,
            has_previous=has_previous,
        )
