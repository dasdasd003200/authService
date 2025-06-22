# src/feature/users/infrastructure/web/strawberry/mutations.py - FIXED
import strawberry

from src.feature.users.application.use_cases.create_user import CreateUserUseCase, CreateUserCommand
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository
from .types import CreateUserInput, CreateUserResponse
from .converters import convert_create_result_to_user_type


@strawberry.type
class UserMutations:
    """User mutations - FIXED VERSION"""

    @strawberry.mutation
    def create_user(self, input: CreateUserInput) -> CreateUserResponse:
        """Create user - SYNC VERSION"""
        try:
            repository = DjangoUserRepository()
            use_case = CreateUserUseCase(repository)

            command = CreateUserCommand(
                email=input.email,
                password=input.password,
                first_name=input.first_name,
                last_name=input.last_name,
                email_verified=input.email_verified,
            )

            # Execute async function synchronously
            import asyncio

            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            result = loop.run_until_complete(use_case.execute(command))
            user_data = convert_create_result_to_user_type(result)

            return CreateUserResponse(success=True, message="User created successfully", error_code=None, data=user_data)

        except Exception as e:
            return CreateUserResponse(success=False, message=str(e), error_code="USER_CREATION_ERROR", data=None)

    @strawberry.mutation
    def delete_user(self, user_id: str) -> CreateUserResponse:
        """Delete user - SYNC VERSION"""
        try:
            from uuid import UUID
            from src.core.application.use_cases.base_crud_use_cases import DeleteEntityUseCase, DeleteEntityCommand

            repository = DjangoUserRepository()
            use_case = DeleteEntityUseCase(repository, "User")
            command = DeleteEntityCommand(entity_id=UUID(user_id))

            # Execute async function synchronously
            import asyncio

            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            success = loop.run_until_complete(use_case.execute(command))

            return CreateUserResponse(success=success, message="User deleted successfully" if success else "Failed to delete user", error_code=None, data=None)

        except Exception as e:
            return CreateUserResponse(success=False, message=str(e), error_code="USER_DELETION_ERROR", data=None)

