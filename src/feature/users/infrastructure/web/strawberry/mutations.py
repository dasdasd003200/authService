# 1. src/feature/users/infrastructure/web/strawberry/mutations.py
"""
User Mutations - IMPORT CORREGIDO
"""

import strawberry
from ...dependency_injection import get_create_user_use_case, get_update_user_use_case, get_delete_user_use_case
from src.feature.users.application.use_cases.create_user import CreateUserCommand
from src.feature.users.application.use_cases.update_user import UpdateUserCommand, ChangePasswordCommand
from src.core.application.use_cases.base import DeleteEntityCommand

from src.core.infrastructure.web.strawberry.helpers.execution import (
    execute_use_case,
    create_error_response,
)
from src.core.infrastructure.web.strawberry.helpers.validators import validate_uuid

from .helpers.processors import (
    process_create_user_input,
    process_update_user_input,
    process_change_password_input,
)

from .types import CreateUserInput, CreateUserResponse, UpdateUserInput, UpdateUserResponse, ChangePasswordInput, DeleteUserResponse
from .converters import convert_create_result_to_user_type, convert_result_to_type


@strawberry.type
class UserMutations:
    """User mutations - IMPORT CORREGIDO"""

    @strawberry.mutation
    async def create_user(self, input: CreateUserInput) -> CreateUserResponse:
        """Create user"""
        try:
            validated_data = process_create_user_input(input)
            use_case = get_create_user_use_case()  # ✅ Ahora funciona

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
        """Update user"""
        try:
            validated_data = process_update_user_input(input)
            use_case = get_update_user_use_case()  # ✅ Ahora funciona

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
    async def delete_user(self, user_id: str) -> DeleteUserResponse:
        """Delete user"""
        try:
            entity_id = validate_uuid(user_id, "User ID")
            use_case = get_delete_user_use_case()  # ✅ Ahora funciona

            command = DeleteEntityCommand(entity_id=entity_id)

            async def _execute():
                return await use_case.execute(command)

            return await execute_use_case(_execute, DeleteUserResponse, "User deleted successfully")

        except Exception as e:
            return create_error_response(DeleteUserResponse, e)

