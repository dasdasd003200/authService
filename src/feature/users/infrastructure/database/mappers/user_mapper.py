# src/feature/users/infrastructure/database/mappers/user_mapper.py
"""
User Entity Mapper - FIXED for minimal CRUD
Removes references to eliminated fields: last_login, failed_login_attempts, is_staff, is_superuser
"""

from typing import Dict, Any

from src.core.domain.value_objects.email import Email
from src.core.infrastructure.database.mappers.base_mapper import BaseEntityMapper
from src.feature.users.domain.entities.user import User
from src.feature.users.domain.value_objects.user_status import UserStatus
from src.feature.users.infrastructure.database.models import UserModel


class UserEntityMapper(BaseEntityMapper[User, UserModel]):
    def model_to_entity(self, model: UserModel) -> User:
        """
        Convert Django model to domain entity
        UPDATED: Only maps existing fields
        """
        return User(
            id=model.id,
            email=Email(model.email),
            first_name=model.first_name,
            last_name=model.last_name,
            status=UserStatus.from_string(model.status),
            email_verified=model.email_verified,
            created_at=model.created_at,
            updated_at=model.updated_at,
            # REMOVED: last_login=model.last_login,
            # REMOVED: failed_login_attempts=model.failed_login_attempts,
        )

    def entity_to_model_data(self, user: User) -> Dict[str, Any]:
        """
        Convert domain entity to Django model data
        UPDATED: Only maps existing fields
        """
        return {
            "id": user.id,
            "email": str(user.email),
            "first_name": user.first_name,
            "last_name": user.last_name,
            "status": user.status.value,
            "email_verified": user.email_verified,
            "created_at": user.created_at,
            "updated_at": user.updated_at,
            # Django-specific fields (keep minimal)
            "is_active": user.status == UserStatus.ACTIVE,
            # REMOVED: "is_staff": False,
            # REMOVED: "is_superuser": False,
            # REMOVED: "last_login": user.last_login,
            # REMOVED: "failed_login_attempts": user.failed_login_attempts,
        }

