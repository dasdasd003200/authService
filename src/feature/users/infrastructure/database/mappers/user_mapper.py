# src/feature/users/infrastructure/database/mappers/user_mapper.py - CENTRALIZED
from typing import Dict, Any

from src.core.infrastructure.database.mappers.base_mapper import BaseEntityMapper
from src.feature.users.domain.entities.user import User
from src.feature.users.infrastructure.database.models import UserModel
from src.feature.users.domain.schemes.user_fields import UserFields


class UserEntityMapper(BaseEntityMapper[User, UserModel]):
    def model_to_entity(self, model: UserModel) -> User:
        """Use centralized field mapping"""
        # Get constructor args from centralized fields
        args = UserFields.entity_constructor_args(model)
        return User(**args)

    def entity_to_model_data(self, user: User) -> Dict[str, Any]:
        """Use centralized field mapping"""
        # Extract model data using centralized fields
        return UserFields.extract_model_data(user)

