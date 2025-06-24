# 2. src/feature/users/infrastructure/web/strawberry/queries.py
"""
User Queries - IMPORT CORREGIDO
"""

import strawberry

# ✅ CORRECTO - Import desde la raíz del feature:
from ...dependency_injection import get_get_user_use_case

from src.feature.users.application.use_cases.get_user import GetUserByEmailQuery
from src.core.application.use_cases.base import GetEntityByIdQuery

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
    """User queries - IMPORT CORREGIDO"""

    @strawberry.field
    async def user_by_id(self, user_id: str) -> GetUserResponse:
        """Get user by ID"""
        try:
            entity_id = validate_uuid(user_id, "User ID")
            use_case = get_get_user_use_case()  # ✅ Ahora funciona

            query = GetEntityByIdQuery(entity_id=entity_id)

            async def _execute():
                user = await use_case.execute(query)
                return convert_user_to_type(user) if user else None

            return await execute_use_case(_execute, GetUserResponse, "User retrieved successfully")

        except Exception as e:
            return create_error_response(GetUserResponse, e)

    @strawberry.field
    async def user_by_email(self, email: str) -> GetUserByEmailResponse:
        """Get user by email"""
        try:
            clean_email = validate_email_format(email)
            use_case = get_get_user_use_case()

            query = GetUserByEmailQuery(email=clean_email)

            async def _execute():
                result = await use_case.execute_by_email(query)
                return convert_result_to_type(result)

            return await execute_use_case(_execute, GetUserByEmailResponse, "User retrieved successfully")

        except Exception as e:
            return create_error_response(GetUserByEmailResponse, e)

