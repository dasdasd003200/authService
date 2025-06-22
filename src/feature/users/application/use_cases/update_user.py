# src/feature/users/application/use_cases/update_user.py - FIXED
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.core.exceptions.base_exceptions import NotFoundError, ValidationException
from src.feature.users.domain.repositories.user_repository import UserRepository

# USAR PASSWORD DEL CORE
from src.core.infrastructure.security.password_service import create_password


@dataclass
class UpdateUserCommand:
    """Command for updating user"""

    user_id: UUID
    first_name: Optional[str] = None
    last_name: Optional[str] = None


@dataclass
class ChangePasswordCommand:
    """Command for changing password"""

    user_id: UUID
    new_password: str


@dataclass
class UpdateUserResult:
    """Result of updating user"""

    user_id: str
    email: str
    first_name: str
    last_name: str
    full_name: str
    status: str
    email_verified: bool


class UpdateUserUseCase:
    """Use case for updating user information"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute_profile_update(self, command: UpdateUserCommand) -> UpdateUserResult:
        """Update user profile information"""
        user = await self.user_repository.find_by_id(command.user_id)
        if not user:
            raise NotFoundError(f"User with ID {command.user_id} not found", error_code="USER_NOT_FOUND")

        user.update_profile(first_name=command.first_name, last_name=command.last_name)
        updated_user = await self.user_repository.save(user)

        return UpdateUserResult(
            user_id=str(updated_user.id),
            email=str(updated_user.email),
            first_name=updated_user.first_name,
            last_name=updated_user.last_name,
            full_name=updated_user.full_name,
            status=updated_user.status.value,
            email_verified=updated_user.email_verified,
        )

    async def execute_password_change(self, command: ChangePasswordCommand) -> bool:
        """Change user password"""
        user = await self.user_repository.find_by_id(command.user_id)
        if not user:
            raise NotFoundError(f"User with ID {command.user_id} not found", error_code="USER_NOT_FOUND")

        try:
            # USAR PASSWORD DEL CORE
            new_password = create_password(command.new_password)
            user.change_password(new_password)
            await self.user_repository.save(user)
            return True
        except ValueError as e:
            raise ValidationException(str(e), error_code="INVALID_PASSWORD")


class DeactivateUserUseCase:
    """Use case for deactivating users"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, user_id: UUID) -> bool:
        """Deactivate user"""
        user = await self.user_repository.find_by_id(user_id)
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found", error_code="USER_NOT_FOUND")

        user.deactivate()
        await self.user_repository.save(user)
        return True
