# src/feature/users/application/use_cases/user_use_cases.py
from typing import Optional
from uuid import UUID

from src.core.application.use_cases.base_crud_use_cases import BaseCrudUseCases
from ...domain.entities.user import User
from ...domain.repositories.user_repository import UserRepository
from src.core.domain.value_objects.email import Email
from ...domain.value_objects.user_status import UserStatus
from src.core.exceptions.base_exceptions import ValidationException, NotFoundError


class UserUseCases(BaseCrudUseCases[User]):
    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository, "User")
        self.user_repository = user_repository  # Para métodos específicos

    async def create_user(self, email: str, password: str, first_name: str, last_name: str, email_verified: bool = False) -> User:
        if not email or not password:
            raise ValidationException("Email and password are required")
        if not first_name or not last_name:
            raise ValidationException("First name and last name are required")

        email_vo = Email(email)
        if await self.user_repository.exists_by_email(email_vo):
            raise ValidationException(f"User with email {email} already exists")

        user = User(email=email_vo, first_name=first_name.strip(), last_name=last_name.strip(), status=UserStatus.PENDING_VERIFICATION if not email_verified else UserStatus.ACTIVE, email_verified=email_verified)
        return await self.user_repository.save_with_password(user, password)

    async def update_user(self, user_id: UUID, first_name: Optional[str] = None, last_name: Optional[str] = None) -> User:
        user = await self.repository.find_by_id(user_id)
        if not user:
            raise NotFoundError(f"User with ID {user_id} not found")

        user.update_profile(first_name=first_name, last_name=last_name)
        return await self.repository.save(user)

