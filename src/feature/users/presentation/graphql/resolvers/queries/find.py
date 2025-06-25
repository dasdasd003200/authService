import strawberry

from src.feature.users.domain.inputs.find import UserFindInput
from src.feature.users.domain.types.find import UserFindResponse
from src.feature.users.application.use_cases.user_use_cases import UserUseCases
from src.feature.users.infrastructure.services.find import UserFindService
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository


@strawberry.type
class UserFindResolver:
    @strawberry.field
    async def users_find(self, input: UserFindInput) -> UserFindResponse:
        """Find users with filtering and pagination"""
        repository = DjangoUserRepository()
        use_cases = UserUseCases(repository)
        service = UserFindService(use_cases)
        return await service.dispatch(input)

