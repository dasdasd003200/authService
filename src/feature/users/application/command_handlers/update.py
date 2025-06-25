from src.feature.users.domain.cqrs.commands import UserUpdateCommand  # ✅ IMPORT ABSOLUTO
from src.feature.users.domain.types.update import UserUpdateResponse
from src.feature.users.infrastructure.services.update import UserUpdateService


class UserUpdateCommandHandler:
    def __init__(self, user_service: UserUpdateService):
        self.user_service = user_service

    async def execute(self, command: UserUpdateCommand) -> UserUpdateResponse:
        return await self.user_service.dispatch(command.input, command.user_context)

