import strawberry

from src.feature.users.domain.inputs.find_one import UserFindOneInput
from src.feature.users.domain.types.find_one import UserFindOneResponse
from src.feature.users.application.use_cases.user_use_cases import UserUseCases
from src.feature.users.infrastructure.services.find_one import UserFindOneService
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository


@strawberry.type
class UserFindOneResolver:
    @strawberry.field
    async def user_find_one(self, input: UserFindOneInput) -> UserFindOneResponse:
        """Find a single user by ID or email"""
        repository = DjangoUserRepository()
        use_cases = UserUseCases(repository)
        service = UserFindOneService(use_cases)
        return await service.dispatch(input)

