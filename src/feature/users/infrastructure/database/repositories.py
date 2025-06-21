# src/feature/users/infrastructure/database/repositories.py - SIMPLIFIED FIXED
from typing import Optional, cast, Union
from datetime import datetime
from uuid import UUID

from src.core.domain.value_objects.email import Email
from src.core.infrastructure.database.repositories import DjangoBaseRepository
from src.feature.users.domain.entities.user import User
from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.value_objects.user_status import UserStatus
from src.feature.users.infrastructure.database.models import UserModel
from src.core.application.services.password_service import create_password_from_hash


class DjangoUserRepository(DjangoBaseRepository[User], UserRepository):
    """Django implementation of user repository - much simpler now!"""

    def __init__(self):
        super().__init__(UserModel)

    def _model_to_entity(self, model: UserModel) -> User:
        """Convert Django model to domain entity"""
        password = create_password_from_hash(cast(str, model.password))

        return User(
            id=cast(UUID, model.id),
            email=Email(cast(str, model.email)),
            password=password,
            first_name=cast(str, model.first_name),
            last_name=cast(str, model.last_name),
            status=UserStatus.from_string(cast(str, model.status)),
            email_verified=cast(bool, model.email_verified),
            last_login=cast(Union[datetime, None], model.last_login),
            failed_login_attempts=cast(int, model.failed_login_attempts),
            created_at=cast(datetime, model.created_at),
            updated_at=cast(datetime, model.updated_at),
        )

    def _entity_to_model_data(self, user: User) -> dict:
        """Convert domain entity to Django model data"""
        from src.core.application.services.password_service import DjangoPasswordAdapter

        data = {
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

        # Handle password
        if isinstance(user.password, DjangoPasswordAdapter):
            data["password"] = user.password.django_hash
        else:
            data["password"] = user.password.hashed_value

        return data

    # Only implement user-specific methods
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

