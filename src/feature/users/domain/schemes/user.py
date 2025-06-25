# CAMBIAR NOMBRE DE LA CLASE PARA EVITAR CONFUSIÓN
import strawberry
from typing import Optional
from datetime import datetime
from ..enums.status import UserStatus


@strawberry.type
class UserGraphQLType:  # ✅ CAMBIAR: User → UserGraphQLType
    """
    User GraphQL Type - Para API responses
    Esta es DIFERENTE a la User entity del domain
    """

    id: str = strawberry.field(description="Unique user identifier")
    email: str = strawberry.field(description="User email address")
    first_name: str = strawberry.field(description="User first name")
    last_name: str = strawberry.field(description="User last name")
    full_name: str = strawberry.field(description="User full name")
    status: UserStatus = strawberry.field(description="User status")
    email_verified: bool = strawberry.field(description="Email verification status")
    last_login: Optional[datetime] = strawberry.field(default=None, description="Last login timestamp")
    failed_login_attempts: int = strawberry.field(description="Failed login attempts count")
    created_at: datetime = strawberry.field(description="Creation timestamp")
    updated_at: datetime = strawberry.field(description="Last update timestamp")

