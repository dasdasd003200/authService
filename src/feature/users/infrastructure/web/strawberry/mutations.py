# src/feature/users/infrastructure/web/strawberry/mutations.py - FIXED
import strawberry
import asyncio
from typing import Optional
from uuid import UUID

from src.core.exceptions.base_exceptions import BaseDomainException
from src.feature.users.application.use_cases.create_user import (
    CreateUserUseCase,
    CreateUserCommand,
)
from src.feature.users.application.use_cases.delete_user import DeleteUserUseCase
from src.core.application.use_cases.base_crud_use_cases import DeleteEntityCommand
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository
from .types import CreateUserInput, UserType, CreateUserResponse


def handle_async_execution(async_func, *args, **kwargs):
    """Helper to run async functions in sync context"""
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    return loop.run_until_complete(async_func(*args, **kwargs))


def create_success_response(response_class, message: str, data=None):
    """Create success response"""
    return response_class(success=True, message=message, error_code=None, data=data)


def create_error_response(response_class, error: Exception):
    """Create error response from exception"""
    if isinstance(error, BaseDomainException):
        return response_class(
            success=False, message=error.message, error_code=error.error_code, data=None
        )
    else:
        return response_class(
            success=False,
            message=f"An unexpected error occurred: {str(error)}",
            error_code="INTERNAL_ERROR",
            data=None,
        )


def convert_result_to_user_type(result) -> UserType:
    """Convert use case result to GraphQL type"""
    from src.core.infrastructure.web.strawberry.types import UserStatusEnumStrawberry

    status_map = {
        "active": UserStatusEnumStrawberry.ACTIVE,
        "inactive": UserStatusEnumStrawberry.INACTIVE,
        "suspended": UserStatusEnumStrawberry.SUSPENDED,
        "pending_verification": UserStatusEnumStrawberry.PENDING_VERIFICATION,
    }

    return UserType(
        id=result.user_id,
        email=result.email,
        first_name=getattr(result, "first_name", ""),
        last_name=getattr(result, "last_name", ""),
        full_name=result.full_name,
        status=status_map.get(
            result.status, UserStatusEnumStrawberry.PENDING_VERIFICATION
        ),
        email_verified=result.email_verified,
        last_login=None,
        failed_login_attempts=0,
        created_at=None,
        updated_at=None,
    )


@strawberry.type
class UserMutations:
    """User mutations"""

    @strawberry.mutation
    def create_user(self, input: CreateUserInput) -> CreateUserResponse:
        """Create a new user"""

        async def _create_user():
            repository = DjangoUserRepository()
            use_case = CreateUserUseCase(repository)

            command = CreateUserCommand(
                email=input.email,
                password=input.password,
                first_name=input.first_name,
                last_name=input.last_name,
                email_verified=input.email_verified,
            )

            result = await use_case.execute(command)
            return convert_result_to_user_type(result)

        try:
            user_data = handle_async_execution(_create_user)
            return create_success_response(
                CreateUserResponse, "User created successfully", user_data
            )
        except Exception as e:
            return create_error_response(CreateUserResponse, e)

    @strawberry.mutation
    def delete_user(
        self, user_id: str
    ) -> CreateUserResponse:  # Usando mismo response type
        """Delete a user"""

        async def _delete_user():
            repository = DjangoUserRepository()
            use_case = DeleteUserUseCase(repository)

            command = DeleteEntityCommand(entity_id=UUID(user_id))
            return await use_case.execute(command)

        try:
            success = handle_async_execution(_delete_user)
            message = (
                "User deleted successfully" if success else "Failed to delete user"
            )
            return create_success_response(CreateUserResponse, message, None)
        except Exception as e:
            return create_error_response(CreateUserResponse, e)
