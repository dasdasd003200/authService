# src/feature/users/infrastructure/web/graphql/queries.py
from graphene import ObjectType, String, Field, List, ID, Int

from src.feature.users.infrastructure.database.repositories import DjangoUserRepository
from src.feature.users.infrastructure.web.graphql.types import UserType
from src.core.domain.value_objects.email import Email


class UserData:
    """Simple data container for GraphQL UserType"""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class UserQueries(ObjectType):
    """User queries"""

    user_by_id = Field(
        UserType, user_id=ID(required=True), description="Get user by ID"
    )

    user_by_email = Field(
        UserType, email=String(required=True), description="Get user by email"
    )

    users = Field(
        List(UserType),
        limit=Int(default_value=10),
        offset=Int(default_value=0),
        description="Get list of users",
    )

    async def resolve_user_by_id(self, info, user_id):
        """Resolve user by ID"""
        _ = info  # Mark as used to avoid linter warnings
        try:
            repository = DjangoUserRepository()
            user = await repository.find_by_id(user_id)

            if not user:
                return None

            return UserData(
                id=str(user.id),
                email=str(user.email),
                first_name=user.first_name,
                last_name=user.last_name,
                full_name=user.full_name,
                status=user.status.value,
                email_verified=user.email_verified,
                last_login=user.last_login,
                failed_login_attempts=user.failed_login_attempts,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
        except Exception:
            return None

    async def resolve_user_by_email(self, info, email):
        """Resolve user by email"""
        _ = info  # Mark as used to avoid linter warnings
        try:
            repository = DjangoUserRepository()
            email_vo = Email(email)
            user = await repository.find_by_email(email_vo)

            if not user:
                return None

            return UserData(
                id=str(user.id),
                email=str(user.email),
                first_name=user.first_name,
                last_name=user.last_name,
                full_name=user.full_name,
                status=user.status.value,
                email_verified=user.email_verified,
                last_login=user.last_login,
                failed_login_attempts=user.failed_login_attempts,
                created_at=user.created_at,
                updated_at=user.updated_at,
            )
        except Exception:
            return None

    async def resolve_users(self, info, limit=10, offset=0):
        """Resolve list of users"""
        _ = info  # Mark as used to avoid linter warnings
        try:
            repository = DjangoUserRepository()
            users = await repository.find_by_criteria([])

            # Apply pagination
            paginated_users = users[offset : offset + limit]

            return [
                UserData(
                    id=str(user.id),
                    email=str(user.email),
                    first_name=user.first_name,
                    last_name=user.last_name,
                    full_name=user.full_name,
                    status=user.status.value,
                    email_verified=user.email_verified,
                    last_login=user.last_login,
                    failed_login_attempts=user.failed_login_attempts,
                    created_at=user.created_at,
                    updated_at=user.updated_at,
                )
                for user in paginated_users
            ]
        except Exception:
            return []

