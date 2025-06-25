from uuid import UUID
from typing import Dict, Any

from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.types.delete import UserDeleteResponse


class UserDeleteService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def dispatch(self, user_id: str, user_context: Dict[str, Any]) -> UserDeleteResponse:
        """Dispatch delete user operation"""
        try:
            entity_id = UUID(user_id)
            user = await self.user_repository.find_by_id(entity_id)

            if not user:
                return UserDeleteResponse(success=False, message=f"User with ID {user_id} not found", error_code="USER_NOT_FOUND")

            deleted = await self.user_repository.delete_by_id(entity_id)

            if deleted:
                return UserDeleteResponse(success=True, message="User deleted successfully")
            else:
                return UserDeleteResponse(success=False, message="Failed to delete user", error_code="DELETE_FAILED")

        except Exception as e:
            return UserDeleteResponse(success=False, message=str(e), error_code="DELETE_ERROR")
