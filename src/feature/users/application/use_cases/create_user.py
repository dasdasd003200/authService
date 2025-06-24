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
    email: str
    password: str
    first_name: str
    last_name: str
    email_verified: bool = False


@dataclass
class CreateUserResult:
    user_id: str
    email: str
    first_name: str
    last_name: str
    full_name: str
    status: str
    email_verified: bool


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, command: CreateUserCommand) -> CreateUserResult:
        try:
            validate_password(command.password)
        except ValidationError as e:
            raise ValidationException("; ".join(e.messages), error_code="INVALID_PASSWORD")

        email = Email(command.email)

        if await self.user_repository.exists_by_email(email):
            raise ConflictError(
                f"User with email {email} already exists",
                error_code="USER_ALREADY_EXISTS",
            )

        user = User(
            email=email,
            first_name=command.first_name,
            last_name=command.last_name,
            status=UserStatus.PENDING_VERIFICATION if not command.email_verified else UserStatus.ACTIVE,
            email_verified=command.email_verified,
        )

        saved_user = await self.user_repository.save_with_password(user, command.password)

        return CreateUserResult(
            user_id=str(saved_user.id),
            email=str(saved_user.email),
            first_name=saved_user.first_name,
            last_name=saved_user.last_name,
            full_name=saved_user.full_name,
            status=saved_user.status.value,
            email_verified=saved_user.email_verified,
        )
