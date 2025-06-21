# src/feature/users/application/use_cases/create_user.py
from dataclasses import dataclass

from src.core.domain.value_objects.email import Email
from src.core.exceptions.base_exceptions import ConflictError
from src.feature.users.domain.entities.user import User
from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.value_objects.user_status import UserStatus

# Import the Django password adapter
from src.feature.users.infrastructure.database.repositories import DjangoPasswordAdapter


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
    """Use case for creating a new user"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, command: CreateUserCommand) -> CreateUserResult:
        """Executes user creation"""

        # Create value objects
        email = Email(command.email)
        # Use Django password adapter instead of domain Password
        password = DjangoPasswordAdapter.create_django(command.password)

        # Check that user doesn't exist
        if await self.user_repository.exists_by_email(email):
            raise ConflictError(
                f"User with email {email} already exists",
                error_code="USER_ALREADY_EXISTS",
            )

        # Create entity
        user = User(
            email=email,
            password=password,
            first_name=command.first_name,
            last_name=command.last_name,
            status=UserStatus.PENDING_VERIFICATION
            if not command.email_verified
            else UserStatus.ACTIVE,
            email_verified=command.email_verified,
        )

        # Save in repository
        saved_user = await self.user_repository.save(user)

        # Return result
        return CreateUserResult(
            user_id=str(saved_user.id),
            email=str(saved_user.email),
            full_name=saved_user.full_name,
            status=saved_user.status.value,
            email_verified=saved_user.email_verified,
        )

