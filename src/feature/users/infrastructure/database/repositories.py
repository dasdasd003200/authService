# src/feature/users/infrastructure/database/repositories.py - CORREGIDO CON DJANGO PASSWORD METHODS
from typing import Optional
from uuid import UUID
from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist

from src.core.domain.value_objects.email import Email
from src.core.infrastructure.database.repositories import DjangoBaseRepository
from src.feature.users.domain.entities.user import User
from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.value_objects.user_status import UserStatus
from src.feature.users.infrastructure.database.models import UserModel


class DjangoUserRepository(DjangoBaseRepository[User], UserRepository):
    """Django user repository with password management"""

    def __init__(self):
        super().__init__(UserModel)

    def _model_to_entity(self, model: UserModel) -> User:
        """Convert model to entity - SIN password field"""
        return User(
            id=model.id,
            email=Email(model.email),
            first_name=model.first_name,
            last_name=model.last_name,
            status=UserStatus.from_string(model.status),
            email_verified=model.email_verified,
            last_login=model.last_login,
            failed_login_attempts=model.failed_login_attempts,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _entity_to_model_data(self, user: User) -> dict:
        """Convert entity to model data - SIN password field"""
        return {
            "id": user.id,
            "email": str(user.email),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "status": user.status.value,
            "email_verified": user.email_verified,
            "last_login": user.last_login,
            "failed_login_attempts": user.failed_login_attempts,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            "is_active": user.status == UserStatus.ACTIVE,
            "is_staff": False,
            "is_superuser": False,
        }

    # Standard user query methods
    async def find_by_email(self, email: Email) -> Optional[User]:
        """Find user by email"""
        try:
            model = await sync_to_async(UserModel.objects.get)(email=str(email))
            return self._model_to_entity(model)
        except ObjectDoesNotExist:
            return None

    async def exists_by_email(self, email: Email) -> bool:
        """Check if user exists by email"""
        return await sync_to_async(UserModel.objects.filter(email=str(email)).exists)()

    # Password management methods using Django's system
    async def save_with_password(self, entity: User, plain_password: str) -> User:
        """Save user entity with password using Django's hashing"""
        data = self._entity_to_model_data(entity)

        # Create or update model
        model, created = await sync_to_async(self.model_class.objects.update_or_create)(id=entity.id, defaults=data)

        # Set password using Django's method (handles hashing)
        model.set_password(plain_password)
        await sync_to_async(model.save)()

        return self._model_to_entity(model)

    async def verify_password(self, user_id: UUID, plain_password: str) -> bool:
        """Verify user password using Django's verification"""
        try:
            model = await sync_to_async(UserModel.objects.get)(id=user_id)
            return model.check_password(plain_password)
        except ObjectDoesNotExist:
            return False

    async def change_password(self, user_id: UUID, new_plain_password: str) -> bool:
        """Change user password using Django's hashing"""
        try:
            model = await sync_to_async(UserModel.objects.get)(id=user_id)
            model.set_password(new_plain_password)
            await sync_to_async(model.save)()
            return True
        except ObjectDoesNotExist:
            return False

