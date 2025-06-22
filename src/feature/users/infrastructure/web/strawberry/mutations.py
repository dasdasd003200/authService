# src/feature/users/infrastructure/web/strawberry/mutations.py - USANDO INPUT PROCESSORS
import strawberry

from src.feature.users.application.use_cases.create_user import CreateUserUseCase, CreateUserCommand
from src.feature.users.application.use_cases.update_user import UpdateUserUseCase, UpdateUserCommand, ChangePasswordCommand
from src.core.application.use_cases.base_crud_use_cases import DeleteEntityUseCase, DeleteEntityCommand
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository

from src.core.infrastructure.web.strawberry.helpers import (
    execute_use_case,
    validate_uuid,
    process_create_user_input,
    process_update_user_input,
    process_change_password_input,
    create_error_response,
)
from .types import CreateUserInput, CreateUserResponse, UpdateUserInput, UpdateUserResponse, ChangePasswordInput, DeleteUserResponse, UserType
from .converters import convert_create_result_to_user_type, convert_result_to_type


@strawberry.type
class UserMutations:
    """User mutations - Con validación centralizada"""

    @strawberry.mutation
    async def create_user(self, input: CreateUserInput) -> CreateUserResponse:
        """Create user - Validación centralizada"""
        try:
            # ✅ Validación centralizada en un solo lugar
            validated_data = process_create_user_input(input)

            repository = DjangoUserRepository()
            use_case = CreateUserUseCase(repository)

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
        """Update user profile - Validación centralizada"""
        try:
            # ✅ Validación centralizada en un solo lugar
            validated_data = process_update_user_input(input)

            repository = DjangoUserRepository()
            use_case = UpdateUserUseCase(repository)

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
        """Change user password - Validación centralizada"""
        try:
            # ✅ Validación centralizada en un solo lugar
            validated_data = process_change_password_input(input)

            repository = DjangoUserRepository()
            use_case = UpdateUserUseCase(repository)

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
        """Delete user - Validación simple para single parameter"""
        try:
            # ✅ Validación simple para parámetro único
            entity_id = validate_uuid(user_id, "User ID")

            repository = DjangoUserRepository()
            use_case = DeleteEntityUseCase(repository, "User")
            command = DeleteEntityCommand(entity_id=entity_id)

            async def _execute():
                return await use_case.execute(command)

            return await execute_use_case(_execute, DeleteUserResponse, "User deleted successfully")

        except Exception as e:
            return create_error_response(DeleteUserResponse, e)

