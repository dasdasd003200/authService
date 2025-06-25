import strawberry

from src.feature.users.domain.inputs.update import UserUpdateInput
from src.feature.users.domain.types.update import UserUpdateResponse
from src.feature.users.application.use_cases.user_use_cases import UserUseCases
from src.feature.users.infrastructure.services.update import UserUpdateService
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository


@strawberry.type
class UserUpdateResolver:
    @strawberry.mutation
    async def user_update(self, input: UserUpdateInput) -> UserUpdateResponse:
        """Update an existing user"""
        repository = DjangoUserRepository()
        use_cases = UserUseCases(repository)
        service = UserUpdateService(use_cases)
        return await service.dispatch(input, user_context={})

