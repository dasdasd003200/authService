from src.feature.users.domain.cqrs.queries import UserFindOneQuery  # ✅ IMPORT ABSOLUTO
from src.feature.users.domain.types.find_one import UserFindOneResponse
from src.feature.users.infrastructure.services.find_one import UserFindOneService


class UserFindOneQueryHandler:
    def __init__(self, user_service: UserFindOneService):
        self.user_service = user_service

    async def execute(self, query: UserFindOneQuery) -> UserFindOneResponse:
        return await self.user_service.dispatch(query.input)

