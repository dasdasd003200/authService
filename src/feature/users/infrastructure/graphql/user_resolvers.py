import strawberry
from ...domain.inputs.create import UserCreateInput
from ...domain.inputs.update import UserUpdateInput
from ...domain.inputs.find import UserFindInput
from ...domain.inputs.find_one import UserFindOneInput
from ...domain.types.create import UserCreateResponse
from ...domain.types.update import UserUpdateResponse
from ...domain.types.delete import UserDeleteResponse
from ...domain.types.find import UserFindResponse
from ...domain.types.find_one import UserFindOneResponse

from ...application.use_cases.user_use_cases import UserUseCases
from ..database.repositories import DjangoUserRepository
from ..services.user_service import UserService


@strawberry.type
class UserResolvers:
    def __init__(self):
        self._repository = None
        self._use_cases = None
        self._service = None

    @property
    def repository(self):
        if self._repository is None:
            self._repository = DjangoUserRepository()
        return self._repository

    @property
    def use_cases(self):
        if self._use_cases is None:
            self._use_cases = UserUseCases(self.repository)
        return self._use_cases

    @property
    def service(self):
        if self._service is None:
            self._service = UserService(self.use_cases)
        return self._service

    # ===== QUERIES (Like your @Query methods) =====

    @strawberry.field
    async def users_find(self, input: UserFindInput) -> UserFindResponse:
        """Universal find - handles ANY criteria"""
        return await self.service.find(input)

    @strawberry.field
    async def user_find_one(self, input: UserFindOneInput) -> UserFindOneResponse:
        """Universal findOne - handles ANY criteria"""
        return await self.service.find_one(input)

    # ===== MUTATIONS (Like your @Mutation methods) =====

    @strawberry.mutation
    async def user_create(self, input: UserCreateInput) -> UserCreateResponse:
        """Create user"""
        return await self.service.create(input, user_context={})

    @strawberry.mutation
    async def user_update(self, input: UserUpdateInput) -> UserUpdateResponse:
        """Update user"""
        return await self.service.update(input, user_context={})

    @strawberry.mutation
    async def user_delete(self, user_id: str) -> UserDeleteResponse:
        """Delete user"""
        return await self.service.delete(user_id, user_context={})


# ===== SCHEMA MIXINS (Clean exports for main schema) =====


@strawberry.type
class UserQueries:
    """Query mixin for main schema"""

    @strawberry.field
    async def users_find(self, input: UserFindInput) -> UserFindResponse:
        resolver = UserResolvers()  # Fixed: UserResolvers not UserResolver
        return await resolver.users_find(input)

    @strawberry.field
    async def user_find_one(self, input: UserFindOneInput) -> UserFindOneResponse:
        resolver = UserResolvers()  # Fixed: UserResolvers not UserResolver
        return await resolver.user_find_one(input)


@strawberry.type
class UserMutations:
    """Mutation mixin for main schema"""

    @strawberry.mutation
    async def user_create(self, input: UserCreateInput) -> UserCreateResponse:
        resolver = UserResolvers()  # Fixed: UserResolvers not UserResolver
        return await resolver.user_create(input)

    @strawberry.mutation
    async def user_update(self, input: UserUpdateInput) -> UserUpdateResponse:
        resolver = UserResolvers()  # Fixed: UserResolvers not UserResolver
        return await resolver.user_update(input)

    @strawberry.mutation
    async def user_delete(self, user_id: str) -> UserDeleteResponse:
        resolver = UserResolvers()  # Fixed: UserResolvers not UserResolver
        return await resolver.user_delete(user_id)

