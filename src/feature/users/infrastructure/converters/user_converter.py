from typing import List

from ...domain.entities.user import User
from ...domain.schemes.user import UserGraphQLType
from ...domain.enums.status import UserStatus as GraphQLUserStatus
from ...domain.value_objects.user_status import UserStatus


class UserConverter:
    @staticmethod
    def entity_to_graphql(user: User) -> UserGraphQLType:
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
        )

    @staticmethod
    def entities_to_graphql(users: List[User]) -> List[UserGraphQLType]:
        return [UserConverter.entity_to_graphql(user) for user in users]

    @staticmethod
    def entity_to_graphql_optional(user: User = None) -> UserGraphQLType:
        if user is None:
            return None
        return UserConverter.entity_to_graphql(user)

