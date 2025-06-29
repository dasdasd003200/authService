# src/feature/users/infrastructure/database/mappers/user_mapper.py - SIMPLIFIED
from typing import Dict, Any

from src.core.domain.value_objects.email import Email
from src.core.infrastructure.database.mappers.base_mapper import BaseEntityMapper
from src.feature.users.domain.entities.user import User
from src.feature.users.domain.value_objects.user_status import UserStatus
from src.feature.users.infrastructure.database.models import UserModel


class UserEntityMapper(BaseEntityMapper[User, UserModel]):
    def model_to_entity(self, model: UserModel) -> User:
        """Use centralized field mapping"""
        return User(
            id=model.id,
            email=Email(model.email),
            first_name=model.first_name,
            last_name=model.last_name,
            status=UserStatus.from_string(model.status),
            email_verified=model.email_verified,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def entity_to_model_data(self, user: User) -> Dict[str, Any]:
        """Use centralized field mapping from schema"""
        from ...domain.schemes.user import UserGraphQLType

        # Create GraphQL type and use its model data conversion
        graphql_user = UserGraphQLType.from_entity(user)
        return graphql_user.to_model_data()

