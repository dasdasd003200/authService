# src/feature/users/infrastructure/web/strawberry/queries.py - FIXED
import strawberry
import asyncio
from typing import Optional
from uuid import UUID

from src.feature.users.application.use_cases.get_user import (
    GetUserUseCase,
    GetUserByEmailQuery,
)
from src.core.application.use_cases.base_crud_use_cases import GetEntityByIdQuery
from src.feature.users.application.use_cases.search_users import (
    SearchUsersUseCase,
    SearchUsersQuery,
)
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository
from src.core.infrastructure.web.strawberry.types import PaginationInput
from .types import UserType, UserPaginatedResponse


def handle_async_execution(async_func, *args, **kwargs):
    """Helper to run async functions in sync context"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(async_func(*args, **kwargs))


def safe_execute(func, default_value=None):
    """Safely execute function and return default on error"""
    try:
        return func()
    except Exception:
        return default_value


def convert_user_to_type(user) -> UserType:
    """Convert domain user entity to GraphQL type"""
    from src.core.infrastructure.web.strawberry.types import UserStatusEnumStrawberry

    status_map = {
        "active": UserStatusEnumStrawberry.ACTIVE,
        "inactive": UserStatusEnumStrawberry.INACTIVE,
        "suspended": UserStatusEnumStrawberry.SUSPENDED,
        "pending_verification": UserStatusEnumStrawberry.PENDING_VERIFICATION,
    }

    return UserType(
        id=str(user.id),
        email=str(user.email),
        first_name=user.first_name,
        last_name=user.last_name,
        full_name=user.full_name,
        status=status_map.get(
            user.status.value, UserStatusEnumStrawberry.PENDING_VERIFICATION
        ),
        email_verified=user.email_verified,
        last_login=user.last_login,
        failed_login_attempts=user.failed_login_attempts,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def convert_result_to_type(result) -> UserType:
    """Convert use case result to GraphQL type"""
    from src.core.infrastructure.web.strawberry.types import UserStatusEnumStrawberry

    status_map = {
        "active": UserStatusEnumStrawberry.ACTIVE,
        "inactive": UserStatusEnumStrawberry.INACTIVE,
        "suspended": UserStatusEnumStrawberry.SUSPENDED,
        "pending_verification": UserStatusEnumStrawberry.PENDING_VERIFICATION,
    }

    return UserType(
        id=result.user_id,
        email=result.email,
        first_name=result.first_name,
        last_name=result.last_name,
        full_name=result.full_name,
        status=status_map.get(
            result.status, UserStatusEnumStrawberry.PENDING_VERIFICATION
        ),
        email_verified=result.email_verified,
        last_login=None,
        failed_login_attempts=result.failed_login_attempts,
        created_at=None,
        updated_at=None,
    )


@strawberry.type
class UserQueries:
    """User queries"""

    @strawberry.field
    def user_by_id(self, user_id: str) -> Optional[UserType]:
        """Get user by ID"""

        async def _get_user():
            repository = DjangoUserRepository()
            use_case = GetUserUseCase(repository)

            query = GetEntityByIdQuery(entity_id=UUID(user_id))
            user = await use_case.execute(query)

            return convert_user_to_type(user) if user else None

        return safe_execute(
            lambda: handle_async_execution(_get_user), default_value=None
        )

    @strawberry.field
    def user_by_email(self, email: str) -> Optional[UserType]:
        """Get user by email"""

        async def _get_user():
            repository = DjangoUserRepository()
            use_case = GetUserUseCase(repository)

            query = GetUserByEmailQuery(email=email)
            result = await use_case.execute_by_email(query)

            return convert_result_to_type(result)

        return safe_execute(
            lambda: handle_async_execution(_get_user), default_value=None
        )

    @strawberry.field
    def users(
        self, pagination: Optional[PaginationInput] = None
    ) -> UserPaginatedResponse:
        """Get paginated list of users"""

        async def _get_users():
            if pagination is None:
                pagination_obj = PaginationInput()
            else:
                pagination_obj = pagination

            repository = DjangoUserRepository()
            use_case = SearchUsersUseCase(repository)

            from src.core.application.dto.pagination import PaginationRequest

            query = SearchUsersQuery(
                pagination=PaginationRequest(
                    page=pagination_obj.page, page_size=pagination_obj.page_size
                )
            )

            paginated_result = await use_case.execute(query)

            # Convert entities to GraphQL types
            user_types = [convert_user_to_type(user) for user in paginated_result.items]

            # Convert pagination info
            from src.core.infrastructure.web.strawberry.types import PaginationInfo

            pagination_info = PaginationInfo(
                current_page=paginated_result.pagination.current_page,
                page_size=paginated_result.pagination.page_size,
                total_items=paginated_result.pagination.total_items,
                total_pages=paginated_result.pagination.total_pages,
                has_next=paginated_result.pagination.has_next,
                has_previous=paginated_result.pagination.has_previous,
            )

            return UserPaginatedResponse(items=user_types, pagination=pagination_info)

        def default_response():
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

        return safe_execute(
            lambda: handle_async_execution(_get_users), default_value=default_response()
        )
