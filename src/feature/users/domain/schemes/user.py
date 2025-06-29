# src/feature/users/domain/schemes/user.py - FIXED NAMING
import strawberry
from datetime import datetime
from ..value_objects.user_status import UserStatus


@strawberry.type
class UserGraphQLType:
    """Clean User GraphQL schema with explicit camelCase naming"""

    id: str = strawberry.field(description="Unique user identifier")
    email: str = strawberry.field(description="User email address")

    first_name: str = strawberry.field(name="firstName", description="User first name")
    last_name: str = strawberry.field(name="lastName", description="User last name")
    full_name: str = strawberry.field(name="fullName", description="User full name")

    status: UserStatus = strawberry.field(description="User status")

    email_verified: bool = strawberry.field(name="emailVerified", description="Email verification status")
    created_at: datetime = strawberry.field(name="createdAt", description="Creation timestamp")
    updated_at: datetime = strawberry.field(name="updatedAt", description="Last update timestamp")

    @classmethod
    def from_entity(cls, user) -> "UserGraphQLType":
        """Simple entity to GraphQL conversion"""
        return cls(
            id=str(user.id),
            email=str(user.email),
            first_name=user.first_name,
            last_name=user.last_name,
            full_name=user.full_name,
            status=user.status,
            email_verified=user.email_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    @classmethod
    def from_entities(cls, users) -> list["UserGraphQLType"]:
        """Convert list of entities"""
        return [cls.from_entity(user) for user in users]

