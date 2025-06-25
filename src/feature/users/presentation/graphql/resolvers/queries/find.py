import strawberry
from src.feature.users.domain.inputs.find import UserFindInput  # ✅ IMPORT ABSOLUTO
from src.feature.users.domain.types.find import UserFindResponse
from src.feature.users.domain.cqrs.queries import UserFindQuery
from src.feature.users.application.query_handlers.find import UserFindQueryHandler
from src.feature.users.infrastructure.services.find import UserFindService
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository


@strawberry.type
class UserFindResolver:
    @strawberry.field
    async def users_find(self, input: UserFindInput) -> UserFindResponse:
        """Find users with filtering and pagination"""
        # Service injection
        repository = DjangoUserRepository()
        service = UserFindService(repository)
        handler = UserFindQueryHandler(service)

        # Execute query
        query = UserFindQuery(input=input)
        return await handler.execute(query)

