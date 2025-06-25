# src/feature/users/infrastructure/services/delete.py
from typing import Dict, Any
from uuid import UUID

from ...application.use_cases.user_use_cases import UserUseCases
from ...domain.types.delete import UserDeleteResponse
from src.core.exceptions.base_exceptions import BaseDomainException  # ✅ CORRECTO: desde core


class UserDeleteService:
    """Infrastructure Service - Adapter for user deletion"""

    def __init__(self, user_use_cases: UserUseCases):
        self.user_use_cases = user_use_cases

    async def dispatch(self, user_id: str, user_context: Dict[str, Any]) -> UserDeleteResponse:
        """Adapter method: GraphQL input → Use Case → GraphQL response"""
        try:
            # Call Application Use Case
            deleted = await self.user_use_cases.delete_user(UUID(user_id))

            if deleted:
                return UserDeleteResponse(success=True, message="User deleted successfully")
            else:
                return UserDeleteResponse(success=False, message="Failed to delete user", error_code="DELETE_FAILED")

        except BaseDomainException as e:
            return UserDeleteResponse(success=False, message=e.message, error_code=e.error_code)
        except Exception as e:
            return UserDeleteResponse(success=False, message=str(e), error_code="DELETE_ERROR")

