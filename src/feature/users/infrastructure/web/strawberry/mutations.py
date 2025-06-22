# src/feature/users/infrastructure/web/strawberry/mutations.py - USANDO CORE HELPERS
import strawberry

from src.feature.users.application.use_cases.create_user import CreateUserUseCase, CreateUserCommand
from src.core.application.use_cases.base_crud_use_cases import DeleteEntityUseCase, DeleteEntityCommand
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository

# USAR NUEVOS HELPERS
from src.core.infrastructure.web.strawberry.helpers import (
    execute_use_case,
    validate_uuid,
    create_success_response,
    create_error_response,
)
from .types import CreateUserInput, CreateUserResponse, DeleteUserResponse, UserType
from .converters import convert_create_result_to_user_type


@strawberry.type
class UserMutations:
    """User mutations - USANDO CORE HELPERS"""

    @strawberry.mutation
    async def create_user(self, input: CreateUserInput) -> CreateUserResponse:
        """Create user - PATTERN LIMPIO"""
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

            # USAR HELPER PARA EJECUTAR USE CASE
            async def _execute():
                result = await use_case.execute(command)
                return convert_create_result_to_user_type(result)

            return await execute_use_case(_execute, CreateUserResponse, "User created successfully")

        except Exception as e:
            return create_error_response(CreateUserResponse, e)

    @strawberry.mutation
    async def delete_user(self, user_id: str) -> DeleteUserResponse:
        """Delete user - PATTERN LIMPIO"""
        try:
            # VALIDAR UUID USANDO HELPER
            entity_id = validate_uuid(user_id, "User ID")

            repository = DjangoUserRepository()
            use_case = DeleteEntityUseCase(repository, "User")
            command = DeleteEntityCommand(entity_id=entity_id)

            # USAR HELPER PARA EJECUTAR USE CASE
            async def _execute():
                return await use_case.execute(command)

            return await execute_use_case(_execute, DeleteUserResponse, "User deleted successfully")

        except Exception as e:
            return create_error_response(DeleteUserResponse, e)

