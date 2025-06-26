# src/feature/users/infrastructure/graphql/user_resolvers.py
"""
Infrastructure Layer - GraphQL Resolvers
UPDATED: Now uses consolidated UserService instead of 5 separate services
"""

import strawberry

# Domain types
from ...domain.inputs.create import UserCreateInput
from ...domain.inputs.update import UserUpdateInput
from ...domain.inputs.find import UserFindInput
from ...domain.inputs.find_one import UserFindOneInput
from ...domain.types.create import UserCreateResponse
from ...domain.types.update import UserUpdateResponse
from ...domain.types.delete import UserDeleteResponse
from ...domain.types.find import UserFindResponse
from ...domain.types.find_one import UserFindOneResponse

# Application layer
from ...application.use_cases.user_use_cases import UserUseCases
from ..database.repositories import DjangoUserRepository

# CAMBIO: Import consolidated service instead of 5 separate services
from ..services.user_service import UserService

# REMOVED: No longer needed individual services
# from ..services.create import UserCreateService
# from ..services.update import UserUpdateService
# from ..services.delete import UserDeleteService
# from ..services.find import UserFindService
# from ..services.find_one import UserFindOneService


@strawberry.type
class UserResolvers:
    """
    Consolidated User GraphQL Resolvers - UPDATED
    Now uses single UserService instead of 5 separate services

    BENEFITS:
    - Cleaner code: one service instead of 5
    - Better performance: reused dependencies
    - Easier maintenance: centralized CRUD logic
    - Same functionality: zero breaking changes
    """

    def __init__(self):
        """Initialize with lazy loading"""
        self._repository = None
        self._use_cases = None
        self._user_service = None

    @property
    def repository(self):
        """Lazy load repository"""
        if self._repository is None:
            self._repository = DjangoUserRepository()
        return self._repository

    @property
    def use_cases(self):
        """Lazy load use cases"""
        if self._use_cases is None:
            self._use_cases = UserUseCases(self.repository)
        return self._use_cases

    @property
    def user_service(self):
        """Lazy load consolidated service"""
        if self._user_service is None:
            self._user_service = UserService(self.use_cases)
        return self._user_service

    # ===== MUTATIONS =====

    @strawberry.mutation
    async def user_create(self, input: UserCreateInput) -> UserCreateResponse:
        """Create user - UPDATED to use consolidated service"""
        return await self.user_service.create_user(input, user_context={})

    @strawberry.mutation
    async def user_update(self, input: UserUpdateInput) -> UserUpdateResponse:
        """Update user - UPDATED to use consolidated service"""
        return await self.user_service.update_user(input, user_context={})

    @strawberry.mutation
    async def user_delete(self, user_id: str) -> UserDeleteResponse:
        """Delete user - UPDATED to use consolidated service"""
        return await self.user_service.delete_user(user_id, user_context={})

    # ===== QUERIES =====

    @strawberry.field
    async def users_find(self, input: UserFindInput) -> UserFindResponse:
        """Find users - UPDATED to use consolidated service"""
        return await self.user_service.find_users(input)

    @strawberry.field
    async def user_find_one(self, input: UserFindOneInput) -> UserFindOneResponse:
        """Find single user - UPDATED to use consolidated service"""
        return await self.user_service.find_user_one(input)


# ===== SCHEMA MIXINS (No changes needed) =====


@strawberry.type
class UserQueries:
    """User queries for main schema"""

    @strawberry.field
    async def users_find(self, input: UserFindInput) -> UserFindResponse:
        resolver = UserResolvers()
        return await resolver.users_find(input)

    @strawberry.field
    async def user_find_one(self, input: UserFindOneInput) -> UserFindOneResponse:
        resolver = UserResolvers()
        return await resolver.user_find_one(input)


@strawberry.type
class UserMutations:
    """User mutations for main schema"""

    @strawberry.mutation
    async def user_create(self, input: UserCreateInput) -> UserCreateResponse:
        resolver = UserResolvers()
        return await resolver.user_create(input)

    @strawberry.mutation
    async def user_update(self, input: UserUpdateInput) -> UserUpdateResponse:
        resolver = UserResolvers()
        return await resolver.user_update(input)

    @strawberry.mutation
    async def user_delete(self, user_id: str) -> UserDeleteResponse:
        resolver = UserResolvers()
        return await resolver.user_delete(user_id)

