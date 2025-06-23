# src/feature/users/infrastructure/web/strawberry/mutations.py
import strawberry

from src.feature.users.application.use_cases.create_user import CreateUserCommand
from src.feature.users.application.use_cases.update_user import UpdateUserCommand, ChangePasswordCommand
from src.core.application.use_cases.base import DeleteEntityCommand
from src.core.infrastructure.containers.django_setup import get_user_container

# CORE helpers (genéricos)
from src.core.infrastructure.web.strawberry.helpers.execution import (
    execute_use_case,
    create_error_response,
)
from src.core.infrastructure.web.strawberry.helpers.validators import validate_uuid

# FEATURE-SPECIFIC helpers (específicos de users)
from .helpers.processors import (
    process_create_user_input,
    process_update_user_input,
    process_change_password_input,
)

from .types import CreateUserInput, CreateUserResponse, UpdateUserInput, UpdateUserResponse, ChangePasswordInput, DeleteUserResponse
from .converters import convert_create_result_to_user_type, convert_result_to_type


@strawberry.type
class UserMutations:
    """User mutations - Con Dependency Injection y helpers modulares"""

    @strawberry.mutation
    async def create_user(self, input: CreateUserInput) -> CreateUserResponse:
        """Create user - REFACTORIZADO con helpers modulares"""
        try:
            # Validación centralizada
            validated_data = process_create_user_input(input)

            # Usar container en lugar de instanciar directamente
            container = get_user_container()
            use_case = container.get_create_user_use_case()

            command = CreateUserCommand(
                email=validated_data["email"],
                password=validated_data["password"],
                first_name=validated_data["first_name"],
                last_name=validated_data["last_name"],
                email_verified=validated_data["email_verified"],
            )

            async def _execute():
                result = await use_case.execute(command)
                return convert_create_result_to_user_type(result)

            return await execute_use_case(_execute, CreateUserResponse, "User created successfully")

        except Exception as e:
            return create_error_response(CreateUserResponse, e)

    @strawberry.mutation
    async def update_user(self, input: UpdateUserInput) -> UpdateUserResponse:
        """Update user profile - REFACTORIZADO con helpers modulares"""
        try:
            validated_data = process_update_user_input(input)

            container = get_user_container()
            use_case = container.get_update_user_use_case()

            command = UpdateUserCommand(
                user_id=validated_data["user_id"],
                first_name=validated_data.get("first_name"),
                last_name=validated_data.get("last_name"),
            )

            async def _execute():
                result = await use_case.execute_profile_update(command)
                return convert_result_to_type(result)

            return await execute_use_case(_execute, UpdateUserResponse, "User updated successfully")

        except Exception as e:
            return create_error_response(UpdateUserResponse, e)

    @strawberry.mutation
    async def change_password(self, input: ChangePasswordInput) -> DeleteUserResponse:
        """Change user password - REFACTORIZADO con helpers modulares"""
        try:
            validated_data = process_change_password_input(input)

            container = get_user_container()
            use_case = container.get_update_user_use_case()

            command = ChangePasswordCommand(
                user_id=validated_data["user_id"],
                new_password=validated_data["new_password"],
            )

            async def _execute():
                return await use_case.execute_password_change(command)

            return await execute_use_case(_execute, DeleteUserResponse, "Password changed successfully")

        except Exception as e:
            return create_error_response(DeleteUserResponse, e)

    @strawberry.mutation
    async def delete_user(self, user_id: str) -> DeleteUserResponse:
        """Delete user - REFACTORIZADO con helpers modulares"""
        try:
            entity_id = validate_uuid(user_id, "User ID")

            container = get_user_container()
            use_case = container.get_delete_user_use_case()

            command = DeleteEntityCommand(entity_id=entity_id)

            async def _execute():
                return await use_case.execute(command)

            return await execute_use_case(_execute, DeleteUserResponse, "User deleted successfully")

        except Exception as e:
            return create_error_response(DeleteUserResponse, e)
