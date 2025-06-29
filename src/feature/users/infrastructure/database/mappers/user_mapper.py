from typing import Dict, Any

from src.core.infrastructure.database.mappers.base_mapper import BaseEntityMapper
from src.feature.users.domain.entities.user import User
from src.feature.users.infrastructure.database.models import UserModel
from src.feature.users.domain.schemes.user_fields import UserFields


class UserEntityMapper(BaseEntityMapper[User, UserModel]):
    def model_to_entity(self, model: UserModel) -> User:
        args = UserFields.model_to_entity_args(model)
        return User(**args)

    def entity_to_model_data(self, user: User) -> Dict[str, Any]:
        return UserFields.entity_to_model_data(user)
