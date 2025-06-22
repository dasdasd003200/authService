# src/feature/users/application/use_cases/create_user.py - CORREGIDO SIN HASHING
from dataclasses import dataclass
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

from src.core.domain.value_objects.email import Email
from src.core.exceptions.base_exceptions import ConflictError, ValidationException
from src.feature.users.domain.entities.user import User
from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.value_objects.user_status import UserStatus


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
    first_name: str
    last_name: str
    full_name: str
    status: str
    email_verified: bool


class CreateUserUseCase:
    """Use case for creating users"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, command: CreateUserCommand) -> CreateUserResult:
        """Execute user creation"""
        # Validate password using Django's validation
        try:
            validate_password(command.password)
        except ValidationError as e:
            raise ValidationException("; ".join(e.messages), error_code="INVALID_PASSWORD")

        # Create value objects
        email = Email(command.email)

        # Check conflicts
        if await self.user_repository.exists_by_email(email):
            raise ConflictError(
                f"User with email {email} already exists",
                error_code="USER_ALREADY_EXISTS",
            )

        # Create entity WITHOUT password
        user = User(
            email=email,
            first_name=command.first_name,
            last_name=command.last_name,
            status=UserStatus.PENDING_VERIFICATION if not command.email_verified else UserStatus.ACTIVE,
            email_verified=command.email_verified,
        )

        # Save with password - Repository handles Django password hashing
        saved_user = await self.user_repository.save_with_password(user, command.password)

        # Return result
        return CreateUserResult(
            user_id=str(saved_user.id),
            email=str(saved_user.email),
            first_name=saved_user.first_name,
            last_name=saved_user.last_name,
            full_name=saved_user.full_name,
            status=saved_user.status.value,
            email_verified=saved_user.email_verified,
        )

