import strawberry

from src.feature.users.domain.types.delete import UserDeleteResponse
from src.feature.users.application.use_cases.user_use_cases import UserUseCases
from src.feature.users.infrastructure.services.delete import UserDeleteService
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository


@strawberry.type
class UserDeleteResolver:
    @strawberry.mutation
    async def user_delete(self, user_id: str) -> UserDeleteResponse:
        """Delete an existing user"""
        repository = DjangoUserRepository()
        use_cases = UserUseCases(repository)
        service = UserDeleteService(use_cases)
        return await service.dispatch(user_id, user_context={})

