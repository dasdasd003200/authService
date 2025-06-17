# src/feature/users/infrastructure/web/graphql/types.py
import graphene
from graphene import ObjectType, String, Boolean, DateTime, ID


class UserType(ObjectType):
    """GraphQL type for User"""

    id = ID(description="Unique user ID")
    email = String(description="User email")
    first_name = String(description="User first name")
    last_name = String(description="User last name")
    full_name = String(description="User full name")
    status = String(description="User status")
    email_verified = Boolean(description="Email verified")
    last_login = DateTime(description="Last login")
    failed_login_attempts = graphene.Int(description="Failed login attempts")
    created_at = DateTime(description="Creation date")
    updated_at = DateTime(description="Update date")

    def resolve_full_name(self, _):
        """Resolve full name"""
        if hasattr(self, "full_name"):
            return self.full_name
        return f"{self.first_name} {self.last_name}"


class UserStatusEnum(graphene.Enum):
    """Enum for user statuses"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"

