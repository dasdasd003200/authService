# src/feature/users/infrastructure/web/strawberry/queries.py - ACTUALIZADO IMPORTS
import strawberry

from src.feature.users.application.use_cases.get_user import GetUserByEmailQuery
from src.core.application.use_cases.base import GetEntityByIdQuery

from src.core.infrastructure.containers.django_setup import get_user_container

from src.core.infrastructure.web.strawberry.helpers.execution import (
    execute_use_case,
    create_error_response,
)
from src.core.infrastructure.web.strawberry.helpers.validators import (
    validate_uuid,
    validate_email_format,
)

from .types import GetUserResponse, GetUserByEmailResponse
from .converters import convert_user_to_type, convert_result_to_type


@strawberry.type
class UserQueries:
    """User queries - REFACTORIZADO con Dependency Injection y helpers modulares"""

    @strawberry.field
    async def user_by_id(self, user_id: str) -> GetUserResponse:
        """Get user by ID - REFACTORIZADO con helpers modulares"""
        try:
            entity_id = validate_uuid(user_id, "User ID")

            container = get_user_container()
            use_case = container.get_get_user_use_case()

            query = GetEntityByIdQuery(entity_id=entity_id)

            async def _execute():
                user = await use_case.execute(query)
                return convert_user_to_type(user) if user else None

            return await execute_use_case(_execute, GetUserResponse, "User retrieved successfully")

        except Exception as e:
            return create_error_response(GetUserResponse, e)

    @strawberry.field
    async def user_by_email(self, email: str) -> GetUserByEmailResponse:
        """Get user by email - REFACTORIZADO con helpers modulares"""
        try:
            clean_email = validate_email_format(email)

            container = get_user_container()
            use_case = container.get_get_user_use_case()

            query = GetUserByEmailQuery(email=clean_email)

            async def _execute():
                result = await use_case.execute_by_email(query)
                return convert_result_to_type(result)

            return await execute_use_case(_execute, GetUserByEmailResponse, "User retrieved successfully")

        except Exception as e:
            return create_error_response(GetUserByEmailResponse, e)

