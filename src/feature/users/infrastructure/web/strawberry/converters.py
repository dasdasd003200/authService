# src/feature/users/infrastructure/web/strawberry/converters.py - ARREGLADO
"""
Entity to GraphQL converters - USANDO CORE HELPERS CORRECTOS
"""

# USAR LOS HELPERS CORRECTOS QUE SÍ EXISTEN
from src.core.infrastructure.web.strawberry.helpers import (
    safe_uuid_str,  # CAMBIÓ: uuid_to_string -> safe_uuid_str
    safe_str,
    convert_domain_enum_to_graphql,  # CAMBIÓ: convert_enum_to_graphql -> convert_domain_enum_to_graphql
)
from src.core.infrastructure.web.strawberry.types import UserStatus  # CAMBIÓ: UserStatusEnumStrawberry -> UserStatus
from .types import UserType


def convert_user_to_type(user) -> UserType:
    """Convert domain user entity to GraphQL type"""
    return UserType(
        id=safe_uuid_str(user.id),  # ARREGLADO
        email=safe_str(user.email),
        first_name=user.first_name,
        last_name=user.last_name,
        full_name=user.full_name,
        status=convert_domain_enum_to_graphql(user.status.value, UserStatus),  # ARREGLADO
        email_verified=user.email_verified,
        last_login=user.last_login,
        failed_login_attempts=user.failed_login_attempts,
        created_at=user.created_at,
        updated_at=user.updated_at,
    )


def convert_result_to_type(result) -> UserType:
    """Convert use case result to GraphQL type"""
    return UserType(
        id=result.user_id,
        email=result.email,
        first_name=result.first_name,
        last_name=result.last_name,
        full_name=result.full_name,
        status=convert_domain_enum_to_graphql(result.status, UserStatus),  # ARREGLADO
        email_verified=result.email_verified,
        last_login=None,
        failed_login_attempts=result.failed_login_attempts,
        created_at=None,
        updated_at=None,
    )


def convert_create_result_to_user_type(result) -> UserType:
    """Convert create result to GraphQL type"""
    return UserType(
        id=result.user_id,
        email=result.email,
        first_name=getattr(result, "first_name", ""),
        last_name=getattr(result, "last_name", ""),
        full_name=result.full_name,
        status=convert_domain_enum_to_graphql(result.status, UserStatus),  # ARREGLADO
        email_verified=result.email_verified,
        last_login=None,
        failed_login_attempts=0,
        created_at=None,
        updated_at=None,
    )

