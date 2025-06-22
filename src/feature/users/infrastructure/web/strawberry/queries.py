# src/feature/users/infrastructure/web/strawberry/queries.py - ASYNC NATIVO
import strawberry
from typing import Optional
from uuid import UUID

from src.feature.users.application.use_cases.get_user import GetUserUseCase, GetUserByEmailQuery
from src.core.application.use_cases.base_crud_use_cases import GetEntityByIdQuery
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository
from .types import UserType
from .converters import convert_user_to_type, convert_result_to_type


@strawberry.type
class UserQueries:
    """User queries - ASYNC NATIVO"""

    @strawberry.field
    async def user_by_id(self, user_id: str) -> Optional[UserType]:
        """Get user by ID - ASYNC NATIVO"""
        try:
            repository = DjangoUserRepository()
            use_case = GetUserUseCase(repository)
            query = GetEntityByIdQuery(entity_id=UUID(user_id))

            # ASYNC NATIVO - sin loop.run_until_complete()
            user = await use_case.execute(query)
            return convert_user_to_type(user) if user else None

        except Exception:
            return None

    @strawberry.field
    async def user_by_email(self, email: str) -> Optional[UserType]:
        """Get user by email - ASYNC NATIVO"""
        try:
            repository = DjangoUserRepository()
            use_case = GetUserUseCase(repository)
            query = GetUserByEmailQuery(email=email)

            # ASYNC NATIVO - sin loop.run_until_complete()
            result = await use_case.execute_by_email(query)
            return convert_result_to_type(result)

        except Exception:
            return None

