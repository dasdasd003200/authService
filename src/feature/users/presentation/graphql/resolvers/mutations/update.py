import strawberry
from src.feature.users.domain.inputs.update import UserUpdateInput  # ✅ IMPORT ABSOLUTO
from src.feature.users.domain.types.update import UserUpdateResponse
from src.feature.users.domain.cqrs.commands import UserUpdateCommand
from src.feature.users.application.command_handlers.update import UserUpdateCommandHandler
from src.feature.users.infrastructure.services.update import UserUpdateService
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository


@strawberry.type
class UserUpdateResolver:
    @strawberry.mutation
    async def user_update(self, input: UserUpdateInput) -> UserUpdateResponse:
        """Update an existing user"""
        # Service injection
        repository = DjangoUserRepository()
        service = UserUpdateService(repository)
        handler = UserUpdateCommandHandler(service)

        # Execute command
        command = UserUpdateCommand(input=input, user_context={})
        return await handler.execute(command)

