from src.feature.users.domain.cqrs.commands import UserDeleteCommand  # ✅ IMPORT ABSOLUTO
from src.feature.users.domain.types.delete import UserDeleteResponse
from src.feature.users.infrastructure.services.delete import UserDeleteService


class UserDeleteCommandHandler:
    def __init__(self, user_service: UserDeleteService):
        self.user_service = user_service

    async def execute(self, command: UserDeleteCommand) -> UserDeleteResponse:
        return await self.user_service.dispatch(command.user_id, command.user_context)

