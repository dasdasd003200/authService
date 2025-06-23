# src/feature/users/infrastructure/database/mappers/user_mapper.py
from typing import Dict, Any

from src.core.domain.value_objects.email import Email
from src.core.infrastructure.database.mappers.base_mapper import BaseEntityMapper
from src.feature.users.domain.entities.user import User
from src.feature.users.domain.value_objects.user_status import UserStatus
from src.feature.users.infrastructure.database.models import UserModel


class UserEntityMapper(BaseEntityMapper[User, UserModel]):
    """
    User-specific mapper - SOLO conversión específica de User

    Conoce:
    - Estructura específica de UserModel
    - Estructura específica de User entity
    - Value objects específicos de User (Email, UserStatus)

    NO conoce:
    - Persistencia (eso es del repository)
    - Lógica de negocio compleja (eso es de services)
    """

    def model_to_entity(self, model: UserModel) -> User:
        """Convert UserModel to User entity"""
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

    def entity_to_model_data(self, user: User) -> Dict[str, Any]:
        """Convert User entity to UserModel data dict"""
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
            # Django-specific fields
            "is_active": user.status == UserStatus.ACTIVE,
            "is_staff": False,
            "is_superuser": False,
        }
