# src/feature/users/infrastructure/web/strawberry/queries.py
"""
Strawberry GraphQL queries for User feature.
"""

import strawberry
import asyncio
from typing import Optional
from uuid import UUID

from src.core.domain.value_objects.email import Email
from src.core.infrastructure.web.strawberry.types import (
    PaginationInput,
    UserStatusEnumStrawberry,
)
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository
from .types import UserType, UserPaginatedResponse


def convert_domain_user_to_type(user) -> UserType:
    """Convert domain user entity to GraphQL type"""
    # Convert status to Strawberry enum
    status_map = {
        "active": UserStatusEnumStrawberry.ACTIVE,
        "inactive": UserStatusEnumStrawberry.INACTIVE,
        "suspended": UserStatusEnumStrawberry.SUSPENDED,
        "pending_verification": UserStatusEnumStrawberry.PENDING_VERIFICATION,
    }

    strawberry_status = status_map.get(
        user.status.value, UserStatusEnumStrawberry.PENDING_VERIFICATION
    )

    return UserType(
        id=str(user.id),
        email=str(user.email),
        first_name=user.first_name,
        last_name=user.last_name,
        full_name=user.full_name,
        status=strawberry_status,
        email_verified=user.email_verified,
        last_login=user.last_login,
        failed_login_attempts=user.failed_login_attempts,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def get_or_create_event_loop():
    """Get current event loop or create a new one"""
    try:
        return asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        return loop


@strawberry.type
class UserQueries:
    """User queries"""

    @strawberry.field
    def user_by_id(self, user_id: str) -> Optional[UserType]:
        """Get user by ID - SYNC VERSION!"""

        try:
            repository = DjangoUserRepository()

            async def _get_user():
                return await repository.find_by_id(UUID(user_id))

            loop = get_or_create_event_loop()
            user = loop.run_until_complete(_get_user())

            if not user:
                return None

            return convert_domain_user_to_type(user)

        except Exception:
            return None

    @strawberry.field
    def user_by_email(self, email: str) -> Optional[UserType]:
        """Get user by email - SYNC VERSION!"""

        try:
            repository = DjangoUserRepository()

            async def _get_user():
                email_vo = Email(email)
                return await repository.find_by_email(email_vo)

            loop = get_or_create_event_loop()
            user = loop.run_until_complete(_get_user())

            if not user:
                return None

            return convert_domain_user_to_type(user)

        except Exception:
            return None

    @strawberry.field
    def users(
        self, pagination: Optional[PaginationInput] = None
    ) -> UserPaginatedResponse:
        """Get paginated list of users - SYNC VERSION!"""

        try:
            # Handle pagination
            if pagination is None:
                pagination = PaginationInput()

            repository = DjangoUserRepository()

            async def _get_users():
                return await repository.find_by_criteria([])

            loop = get_or_create_event_loop()
            users = loop.run_until_complete(_get_users())

            # Apply pagination (simple version)
            page = max(1, pagination.page)
            page_size = max(1, min(100, pagination.page_size))
            offset = (page - 1) * page_size

            total_items = len(users)
            paginated_users = users[offset : offset + page_size]

            # Convert to GraphQL types
            user_types = [convert_domain_user_to_type(user) for user in paginated_users]

            # Calculate pagination info
            total_pages = (total_items + page_size - 1) // page_size

            from src.core.infrastructure.web.strawberry.types import PaginationInfo

            pagination_info = PaginationInfo(
                current_page=page,
                page_size=page_size,
                total_items=total_items,
                total_pages=total_pages,
                has_next=page < total_pages,
                has_previous=page > 1,
            )

            return UserPaginatedResponse(items=user_types, pagination=pagination_info)

        except Exception:
            # Return empty result on error
            from src.core.infrastructure.web.strawberry.types import PaginationInfo

            return UserPaginatedResponse(
                items=[],
                pagination=PaginationInfo(
                    current_page=1,
                    page_size=10,
                    total_items=0,
                    total_pages=0,
                    has_next=False,
                    has_previous=False,
                ),
            )

