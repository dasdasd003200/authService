from src.feature.users.domain.cqrs.queries import UserFindQuery  # ✅ IMPORT ABSOLUTO
from src.feature.users.domain.types.find import UserFindResponse
from src.feature.users.infrastructure.services.find import UserFindService


class UserFindQueryHandler:
    def __init__(self, user_service: UserFindService):
        self.user_service = user_service

    async def execute(self, query: UserFindQuery) -> UserFindResponse:
        return await self.user_service.dispatch(query.input)

