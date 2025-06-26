# src/feature/users/infrastructure/converters/user_converter.py
"""
User Converter - FIXED for minimal CRUD
Removes references to eliminated fields: last_login, failed_login_attempts
"""

from typing import List

from ...domain.entities.user import User
from ...domain.schemes.user import UserGraphQLType
from ...domain.enums.status import UserStatus as GraphQLUserStatus
from ...domain.value_objects.user_status import UserStatus


class UserConverter:
    @staticmethod
    def entity_to_graphql(user: User) -> UserGraphQLType:
        """
        Convert domain entity to GraphQL type
        UPDATED: Removed references to eliminated fields
        """

        # Convert status enum
        graphql_status = GraphQLUserStatus.ACTIVE
        if user.status == UserStatus.INACTIVE:
            graphql_status = GraphQLUserStatus.INACTIVE
        elif user.status == UserStatus.SUSPENDED:
            graphql_status = GraphQLUserStatus.SUSPENDED
        elif user.status == UserStatus.PENDING_VERIFICATION:
            graphql_status = GraphQLUserStatus.PENDING_VERIFICATION

        return UserGraphQLType(
            id=str(user.id),
            email=str(user.email),
            first_name=user.first_name,
            last_name=user.last_name,
            full_name=user.full_name,
            status=graphql_status,
            email_verified=user.email_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
            # REMOVED: last_login=user.last_login,
            # REMOVED: failed_login_attempts=user.failed_login_attempts,
        )

    @staticmethod
    def entities_to_graphql(users: List[User]) -> List[UserGraphQLType]:
        """
        Convert list of entities to GraphQL types
        """
        return [UserConverter.entity_to_graphql(user) for user in users]

    @staticmethod
    def entity_to_graphql_optional(user: User = None) -> UserGraphQLType:
        """
        Convert entity to GraphQL with None check
        """
        if user is None:
            return None
        return UserConverter.entity_to_graphql(user)

