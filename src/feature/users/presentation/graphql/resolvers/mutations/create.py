import strawberry
from src.feature.users.domain.inputs.create import UserCreateInput  # ✅ IMPORT ABSOLUTO
from src.feature.users.domain.types.create import UserCreateResponse
from src.feature.users.domain.cqrs.commands import UserCreateCommand
from src.feature.users.application.command_handlers.create import UserCreateCommandHandler
from src.feature.users.infrastructure.services.create import UserCreateService
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository


@strawberry.type
class UserCreateResolver:
    @strawberry.mutation
    async def user_create(self, input: UserCreateInput) -> UserCreateResponse:
        """Create a new user"""
        # Service injection (can be improved with proper DI later)
        repository = DjangoUserRepository()
        service = UserCreateService(repository)
        handler = UserCreateCommandHandler(service)

        # Execute command
        command = UserCreateCommand(input=input, user_context={})
        return await handler.execute(command)

