import strawberry
from enum import Enum


@strawberry.enum
class UserStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"


# Aquí podrían ir otros enums específicos de users en el futuro
# @strawberry.enum
# class UserRole(Enum):
#     ADMIN = "admin"
#     USER = "user"
#     MODERATOR = "moderator"
