# src/feature/users/infrastructure/web/strawberry/queries.py - FIXED
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
    """User queries - FIXED VERSION"""

    @strawberry.field
    def user_by_id(self, user_id: str) -> Optional[UserType]:
        """Get user by ID - SYNC VERSION"""
        try:
            repository = DjangoUserRepository()
            use_case = GetUserUseCase(repository)
            query = GetEntityByIdQuery(entity_id=UUID(user_id))

            # Execute async function synchronously
            import asyncio

            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            user = loop.run_until_complete(use_case.execute(query))
            return convert_user_to_type(user) if user else None

        except Exception:
            return None

    @strawberry.field
    def user_by_email(self, email: str) -> Optional[UserType]:
        """Get user by email - SYNC VERSION"""
        try:
            repository = DjangoUserRepository()
            use_case = GetUserUseCase(repository)
            query = GetUserByEmailQuery(email=email)

            # Execute async function synchronously
            import asyncio

            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

            result = loop.run_until_complete(use_case.execute_by_email(query))
            return convert_result_to_type(result)

        except Exception:
            return None

