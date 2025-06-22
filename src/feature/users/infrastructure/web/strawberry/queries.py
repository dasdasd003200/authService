# src/feature/users/infrastructure/web/strawberry/queries.py - SIMPLIFICADAS
import strawberry

from src.feature.users.application.use_cases.get_user import GetUserUseCase, GetUserByEmailQuery
from src.core.application.use_cases.base_crud_use_cases import GetEntityByIdQuery
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository

from src.core.infrastructure.web.strawberry.helpers import (
    execute_use_case,
    validate_uuid,
    validate_email_format,
    create_error_response,
)

from .types import GetUserResponse, GetUserByEmailResponse
from .converters import convert_user_to_type, convert_result_to_type


@strawberry.type
class UserQueries:
    """User queries - Validación simplificada con helpers centralizados"""

    @strawberry.field
    async def user_by_id(self, user_id: str) -> GetUserResponse:
        """Get user by ID"""
        try:
            # ✅ Validación simple con helper centralizado
            entity_id = validate_uuid(user_id, "User ID")

            repository = DjangoUserRepository()
            use_case = GetUserUseCase(repository)
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
            # ✅ Validación simple con helper centralizado
            clean_email = validate_email_format(email)

            repository = DjangoUserRepository()
            use_case = GetUserUseCase(repository)
            query = GetUserByEmailQuery(email=clean_email)

            async def _execute():
                result = await use_case.execute_by_email(query)
                return convert_result_to_type(result)

            return await execute_use_case(_execute, GetUserByEmailResponse, "User retrieved successfully")

        except Exception as e:
            return create_error_response(GetUserByEmailResponse, e)

