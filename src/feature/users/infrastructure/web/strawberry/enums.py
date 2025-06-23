# src/feature/users/infrastructure/web/strawberry/enums.py
"""
GraphQL enums específicos del feature Users
"""

import strawberry
from enum import Enum


@strawberry.enum
class UserStatus(Enum):
    """User status enum - PERTENECE AL FEATURE USERS"""

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
