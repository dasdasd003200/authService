import strawberry
from src.feature.users.domain.inputs.find_one import UserFindOneInput  # ✅ IMPORT ABSOLUTO
from src.feature.users.domain.types.find_one import UserFindOneResponse
from src.feature.users.domain.cqrs.queries import UserFindOneQuery
from src.feature.users.application.query_handlers.find_one import UserFindOneQueryHandler
from src.feature.users.infrastructure.services.find_one import UserFindOneService
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository


@strawberry.type
class UserFindOneResolver:
    @strawberry.field
    async def user_find_one(self, input: UserFindOneInput) -> UserFindOneResponse:
        """Find a single user by ID or email"""
        # Service injection
        repository = DjangoUserRepository()
        service = UserFindOneService(repository)
        handler = UserFindOneQueryHandler(service)

        # Execute query
        query = UserFindOneQuery(input=input)
        return await handler.execute(query)

