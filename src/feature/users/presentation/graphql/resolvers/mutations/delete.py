import strawberry
from src.feature.users.domain.types.delete import UserDeleteResponse  # ✅ IMPORT ABSOLUTO
from src.feature.users.domain.cqrs.commands import UserDeleteCommand
from src.feature.users.application.command_handlers.delete import UserDeleteCommandHandler
from src.feature.users.infrastructure.services.delete import UserDeleteService
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository


@strawberry.type
class UserDeleteResolver:
    @strawberry.mutation
    async def user_delete(self, user_id: str) -> UserDeleteResponse:
        """Delete an existing user"""
        # Service injection
        repository = DjangoUserRepository()
        service = UserDeleteService(repository)
        handler = UserDeleteCommandHandler(service)

        # Execute command
        command = UserDeleteCommand(user_id=user_id, user_context={})
        return await handler.execute(command)

