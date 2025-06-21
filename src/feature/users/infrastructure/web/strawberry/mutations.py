# src/feature/users/infrastructure/web/strawberry/mutations.py
"""
Strawberry GraphQL mutations for User feature.
"""

import strawberry

from src.core.exceptions.base_exceptions import BaseDomainException
from src.core.infrastructure.web.strawberry.types import UserStatusEnumStrawberry
from src.feature.users.application.use_cases.create_user import (
    CreateUserUseCase,
    CreateUserCommand,
)
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository
from .types import CreateUserInput, CreateUserResponse, UserType


def convert_user_to_type(user_result) -> UserType:
    """Convert use case result to GraphQL type"""
    # Convert status string to enum
    status_map = {
        "active": UserStatusEnumStrawberry.ACTIVE,
        "inactive": UserStatusEnumStrawberry.INACTIVE,
        "suspended": UserStatusEnumStrawberry.SUSPENDED,
        "pending_verification": UserStatusEnumStrawberry.PENDING_VERIFICATION,
    }

    strawberry_status = status_map.get(
        user_result.status, UserStatusEnumStrawberry.PENDING_VERIFICATION
    )

    return UserType(
        id=user_result.user_id,
        email=user_result.email,
        first_name=user_result.first_name if hasattr(user_result, "first_name") else "",
        last_name=user_result.last_name if hasattr(user_result, "last_name") else "",
        full_name=user_result.full_name,
        status=strawberry_status,
        email_verified=user_result.email_verified,
        last_login=None,  # Not in create result
        failed_login_attempts=0,  # Default for new user
        created_at=None,  # Will be set by resolver if needed
        updated_at=None,  # Will be set by resolver if needed
    )


@strawberry.type
class UserMutations:
    """User mutations"""

    @strawberry.mutation
    def create_user(self, input: CreateUserInput) -> CreateUserResponse:
        """Create a new user - SYNC VERSION!"""

        try:
            # Create the use case
            repository = DjangoUserRepository()
            use_case = CreateUserUseCase(repository)

            # Create command
            command = CreateUserCommand(
                email=input.email,
                password=input.password,
                first_name=input.first_name,
                last_name=input.last_name,
                email_verified=input.email_verified,
            )

            # Execute use case synchronously
            import asyncio

            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            result = loop.run_until_complete(use_case.execute(command))

            # Convert to GraphQL type
            user_data = convert_user_to_type(result)

            # Return success response
            return CreateUserResponse(
                success=True,
                message="User created successfully",
                error_code=None,
                data=user_data,
            )

        except BaseDomainException as e:
            # Handle domain exceptions
            return CreateUserResponse(
                success=False, message=e.message, error_code=e.error_code, data=None
            )

        except Exception as e:
            # Handle unexpected exceptions
            return CreateUserResponse(
                success=False,
                message=f"An unexpected error occurred: {str(e)}",
                error_code="INTERNAL_ERROR",
                data=None,
            )

