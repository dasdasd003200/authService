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

# Infrastructure
from ..services.create import UserCreateService
from ..services.update import UserUpdateService
from ..services.delete import UserDeleteService
from ..services.find import UserFindService
from ..services.find_one import UserFindOneService
from ..database.repositories import DjangoUserRepository


@strawberry.type
class UserResolvers:
    """
    Consolidated User GraphQL Resolvers

    ⚠️ MANTIENE LÓGICA EXACTAMENTE IGUAL A LA ORIGINAL
    Solo cambia: múltiples archivos -> un archivo
    """

    # ===== MUTATIONS =====

    @strawberry.mutation
    async def user_create(self, input: UserCreateInput) -> UserCreateResponse:
        """Create a new user - LÓGICA EXACTAMENTE IGUAL"""
        repository = DjangoUserRepository()  # ← IGUAL que antes
        use_cases = UserUseCases(repository)  # ← IGUAL que antes
        service = UserCreateService(use_cases)  # ← IGUAL que antes
        return await service.dispatch(input, user_context={})

    @strawberry.mutation
    async def user_update(self, input: UserUpdateInput) -> UserUpdateResponse:
        """Update an existing user - LÓGICA EXACTAMENTE IGUAL"""
        repository = DjangoUserRepository()  # ← IGUAL que antes
        use_cases = UserUseCases(repository)  # ← IGUAL que antes
        service = UserUpdateService(use_cases)  # ← IGUAL que antes
        return await service.dispatch(input, user_context={})

    @strawberry.mutation
    async def user_delete(self, user_id: str) -> UserDeleteResponse:
        """Delete an existing user - LÓGICA EXACTAMENTE IGUAL"""
        repository = DjangoUserRepository()  # ← IGUAL que antes
        use_cases = UserUseCases(repository)  # ← IGUAL que antes
        service = UserDeleteService(use_cases)  # ← IGUAL que antes
        return await service.dispatch(user_id, user_context={})

    # ===== QUERIES =====

    @strawberry.field
    async def users_find(self, input: UserFindInput) -> UserFindResponse:
        """Find users with filtering and pagination - LÓGICA EXACTAMENTE IGUAL"""
        repository = DjangoUserRepository()  # ← IGUAL que antes
        use_cases = UserUseCases(repository)  # ← IGUAL que antes
        service = UserFindService(use_cases)  # ← IGUAL que antes
        return await service.dispatch(input)

    @strawberry.field
    async def user_find_one(self, input: UserFindOneInput) -> UserFindOneResponse:
        """Find a single user by ID or email - LÓGICA EXACTAMENTE IGUAL"""
        repository = DjangoUserRepository()  # ← IGUAL que antes
        use_cases = UserUseCases(repository)  # ← IGUAL que antes
        service = UserFindOneService(use_cases)  # ← IGUAL que antes
        return await service.dispatch(input)


# ===== SCHEMA MIXINS =====


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

