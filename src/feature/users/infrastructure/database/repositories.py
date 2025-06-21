# src/feature/users/infrastructure/database/repositories.py
from typing import Optional, List, cast, Union
from uuid import UUID
from datetime import datetime

from asgiref.sync import sync_to_async
from django.core.exceptions import ObjectDoesNotExist

from src.core.domain.value_objects.email import Email
from src.core.domain.repositories.criteria.base_criteria import BaseCriteria
from src.feature.users.domain.entities.user import User
from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.value_objects.user_status import UserStatus
from src.feature.users.infrastructure.database.models import UserModel

# Import the password service from core
from src.core.application.services.password_service import (
    DjangoPasswordAdapter,
    create_password_from_hash,
)


class DjangoUserRepository(UserRepository):
    """Django ORM implementation of user repository"""

    def _model_to_entity(self, model: UserModel) -> User:
        """Converts Django model to domain entity"""
        # Create password adapter using core service
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
        """Converts domain entity to Django model data"""
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

        # Handle password - check if it's Django adapter
        if isinstance(user.password, DjangoPasswordAdapter):
            data["password"] = user.password.django_hash
        else:
            # Fallback for other password types (shouldn't happen normally)
            data["password"] = user.password.hashed_value

        return data

    async def save(self, user: User) -> User:
        """Saves or updates a user"""
        data = self._entity_to_model_data(user)

        model, _ = await sync_to_async(UserModel.objects.update_or_create)(
            id=user.id, defaults=data
        )

        return self._model_to_entity(model)

    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Finds user by ID"""
        try:
            model = await sync_to_async(UserModel.objects.get)(id=user_id)
            return self._model_to_entity(model)
        except ObjectDoesNotExist:
            return None

    async def find_by_email(self, email: Email) -> Optional[User]:
        """Finds user by email"""
        try:
            model = await sync_to_async(UserModel.objects.get)(email=str(email))
            return self._model_to_entity(model)
        except ObjectDoesNotExist:
            return None

    async def exists_by_email(self, email: Email) -> bool:
        """Checks if a user exists with the email"""
        return await sync_to_async(UserModel.objects.filter(email=str(email)).exists)()

    async def find_by_criteria(self, criteria: List[BaseCriteria]) -> List[User]:
        """Finds users by criteria"""
        queryset = UserModel.objects.all()

        # Apply criteria
        for criterion in criteria:
            queryset = criterion.apply(queryset)

        models = await sync_to_async(list)(queryset)
        return [self._model_to_entity(model) for model in models]

    async def delete(self, user_id: UUID) -> bool:
        """Deletes a user (soft delete)"""
        try:
            await sync_to_async(UserModel.objects.filter(id=user_id).update)(
                status=UserStatus.INACTIVE.value
            )
            return True
        except Exception:
            return False

    async def count_by_criteria(self, criteria: List[BaseCriteria]) -> int:
        """Counts users by criteria"""
        queryset = UserModel.objects.all()

        # Apply criteria
        for criterion in criteria:
            queryset = criterion.apply(queryset)

        return await sync_to_async(queryset.count)()
