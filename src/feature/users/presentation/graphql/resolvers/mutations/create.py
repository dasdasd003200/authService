import strawberry

# ✅ USAR IMPORTS ABSOLUTOS (no relativos)
from src.feature.users.domain.inputs.create import UserCreateInput
from src.feature.users.domain.types.create import UserCreateResponse
from src.feature.users.application.use_cases.user_use_cases import UserUseCases
from src.feature.users.infrastructure.services.create import UserCreateService
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository


@strawberry.type
class UserCreateResolver:
    @strawberry.mutation
    async def user_create(self, input: UserCreateInput) -> UserCreateResponse:
        """Create a new user"""
        repository = DjangoUserRepository()
        use_cases = UserUseCases(repository)
        service = UserCreateService(use_cases)
        return await service.dispatch(input, user_context={})

