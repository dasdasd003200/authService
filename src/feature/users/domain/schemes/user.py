# src/feature/users/domain/schemes/user.py - CENTRALIZED SCHEMA
import strawberry
from typing import Optional, Dict, Any
from datetime import datetime
from ..enums.status import UserStatus


@strawberry.type
class UserGraphQLType:
    """CENTRALIZED User schema - ALL field definitions here"""

    id: str = strawberry.field(description="Unique user identifier")
    email: str = strawberry.field(description="User email address")
    first_name: str = strawberry.field(description="User first name")
    last_name: str = strawberry.field(description="User last name")
    full_name: str = strawberry.field(description="User full name")
    status: UserStatus = strawberry.field(description="User status")
    email_verified: bool = strawberry.field(description="Email verification status")
    created_at: datetime = strawberry.field(description="Creation timestamp")
    updated_at: datetime = strawberry.field(description="Last update timestamp")

    @classmethod
    def from_entity(cls, user) -> "UserGraphQLType":
        """Convert User entity to GraphQL type"""
        from ..value_objects.user_status import UserStatus as DomainStatus
        from ..enums.status import UserStatus as GraphQLStatus

        # Convert domain status to GraphQL status
        status_map = {
            DomainStatus.ACTIVE: GraphQLStatus.ACTIVE,
            DomainStatus.INACTIVE: GraphQLStatus.INACTIVE,
            DomainStatus.SUSPENDED: GraphQLStatus.SUSPENDED,
            DomainStatus.PENDING_VERIFICATION: GraphQLStatus.PENDING_VERIFICATION,
        }

        return cls(
            id=str(user.id),
            email=str(user.email),
            first_name=user.first_name,
            last_name=user.last_name,
            full_name=user.full_name,
            status=status_map[user.status],
            email_verified=user.email_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

    @classmethod
    def from_entities(cls, users) -> list["UserGraphQLType"]:
        """Convert list of User entities to GraphQL types"""
        return [cls.from_entity(user) for user in users]

    def to_model_data(self) -> Dict[str, Any]:
        """Convert to Django model data format"""
        return {
            "id": self.id,
            "email": self.email,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "status": self.status.value,
            "email_verified": self.email_verified,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.status == UserStatus.ACTIVE,
        }

    # FIELD DEFINITIONS for reuse in mappers
    ENTITY_FIELDS = ["id", "email", "first_name", "last_name", "status", "email_verified", "created_at", "updated_at"]

    MODEL_FIELDS = ENTITY_FIELDS + ["is_active"]

    GRAPHQL_FIELDS = ENTITY_FIELDS + ["full_name"]

