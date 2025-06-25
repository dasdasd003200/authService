from src.feature.users.domain.cqrs.commands import UserCreateCommand  # ✅ IMPORT ABSOLUTO
from src.feature.users.domain.types.create import UserCreateResponse
from src.feature.users.infrastructure.services.create import UserCreateService


class UserCreateCommandHandler:
    def __init__(self, user_service: UserCreateService):
        self.user_service = user_service

    async def execute(self, command: UserCreateCommand) -> UserCreateResponse:
        return await self.user_service.dispatch(command.input, command.user_context)

