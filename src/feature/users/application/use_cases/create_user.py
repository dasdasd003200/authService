# src/feature/users/application/use_cases/create_user.py - SIMPLIFICADO
from dataclasses import dataclass

from src.core.domain.value_objects.email import Email
from src.core.exceptions.base_exceptions import ConflictError
from src.feature.users.domain.entities.user import User
from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.value_objects.user_status import UserStatus

# CORREGIDO: Usar el core service simplificado
from src.core.infrastructure.security.password_service import hash_password


@dataclass
class CreateUserCommand:
    """Command for creating user"""

    email: str
    password: str
    first_name: str
    last_name: str
    email_verified: bool = False


@dataclass
class CreateUserResult:
    """Result of creating user"""

    user_id: str
    email: str
    full_name: str
    status: str
    email_verified: bool


class CreateUserUseCase:
    """Use case for creating users"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, command: CreateUserCommand) -> CreateUserResult:
        """Execute user creation"""
        # Create value objects
        email = Email(command.email)
        password_hash = hash_password(command.password)  # SIMPLIFICADO: usa core service

        # Check conflicts
        if await self.user_repository.exists_by_email(email):
            raise ConflictError(
                f"User with email {email} already exists",
                error_code="USER_ALREADY_EXISTS",
            )

        # Create entity
        user = User(
            email=email,
            password_hash=password_hash,  # CAMBIADO: pasa el hash directamente
            first_name=command.first_name,
            last_name=command.last_name,
            status=UserStatus.PENDING_VERIFICATION if not command.email_verified else UserStatus.ACTIVE,
            email_verified=command.email_verified,
        )

        # Save
        saved_user = await self.user_repository.save(user)

        # Return result
        return CreateUserResult(
            user_id=str(saved_user.id),
            email=str(saved_user.email),
            full_name=saved_user.full_name,
            status=saved_user.status.value,
            email_verified=saved_user.email_verified,
        )

