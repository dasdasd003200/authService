# src/feature/users/infrastructure/services/update.py
from typing import Dict, Any
from uuid import UUID

from ...application.use_cases.user_use_cases import UserUseCases
from ...domain.inputs.update import UserUpdateInput
from ...domain.types.update import UserUpdateResponse
from ..converters.user_converter import UserConverter
from src.core.exceptions.base_exceptions import BaseDomainException  # ✅ CORRECTO: desde core


class UserUpdateService:
    """Infrastructure Service - Adapter for user updates"""

    def __init__(self, user_use_cases: UserUseCases):
        self.user_use_cases = user_use_cases

    async def dispatch(self, input: UserUpdateInput, user_context: Dict[str, Any]) -> UserUpdateResponse:
        """Adapter method: GraphQL input → Use Case → GraphQL response"""
        try:
            # Call Application Use Case
            user = await self.user_use_cases.update_user(user_id=UUID(input.user_id), first_name=input.first_name, last_name=input.last_name)

            # Convert to GraphQL response
            user_graphql = UserConverter.entity_to_graphql(user)

            return UserUpdateResponse(success=True, data=user_graphql, message="User updated successfully")

        except BaseDomainException as e:
            return UserUpdateResponse(success=False, message=e.message, error_code=e.error_code)
        except Exception as e:
            return UserUpdateResponse(success=False, message=str(e), error_code="UPDATE_ERROR")

