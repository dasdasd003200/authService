# src/feature/users/infrastructure/database/repositories.py - SIMPLIFIED
from typing import Optional
from uuid import UUID
from datetime import datetime

from src.core.domain.value_objects.email import Email
from src.core.infrastructure.database.repositories import DjangoBaseRepository
from src.feature.users.domain.entities.user import User
from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.value_objects.user_status import UserStatus
from src.feature.users.infrastructure.database.models import UserModel
from src.core.infrastructure.security.password_service import load_password


class DjangoUserRepository(DjangoBaseRepository[User], UserRepository):
    """Django user repository - SIMPLIFIED"""

    def __init__(self):
        super().__init__(UserModel)

    def _model_to_entity(self, model: UserModel) -> User:
        """Convert model to entity"""
        password = load_password(model.password)

        return User(
            id=model.id,
            email=Email(model.email),
            password=password,
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
        """Convert entity to model data"""
        return {
            "id": user.id,
            "email": str(user.email),
            "password": user.password.hash,
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

    # User-specific methods
    async def find_by_email(self, email: Email) -> Optional[User]:
        """Find user by email"""
        try:
            from django.core.exceptions import ObjectDoesNotExist
            from asgiref.sync import sync_to_async

            model = await sync_to_async(UserModel.objects.get)(email=str(email))
            return self._model_to_entity(model)
        except ObjectDoesNotExist:
            return None

    async def exists_by_email(self, email: Email) -> bool:
        """Check if user exists by email"""
        from asgiref.sync import sync_to_async

        return await sync_to_async(UserModel.objects.filter(email=str(email)).exists)()
