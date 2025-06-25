from uuid import UUID
from typing import Dict, Any

from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.inputs.update import UserUpdateInput
from src.feature.users.domain.types.update import UserUpdateResponse
from src.feature.users.domain.schemes.user import UserGraphQLType  # ✅ USAR NUEVO NOMBRE
from src.feature.users.domain.enums.status import UserStatus as GraphQLUserStatus
from src.feature.users.domain.value_objects.user_status import UserStatus
from src.feature.users.infrastructure.converters.user_converter import UserConverter


class UserUpdateService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def dispatch(self, input: UserUpdateInput, user_context: Dict[str, Any]) -> UserUpdateResponse:
        """Dispatch update user operation"""
        try:
            # Find user
            user_id = UUID(input.user_id)
            user = await self.user_repository.find_by_id(user_id)

            if not user:
                return UserUpdateResponse(success=False, message=f"User with ID {input.user_id} not found", error_code="USER_NOT_FOUND")

            user.update_profile(first_name=input.first_name, last_name=input.last_name)

            updated_user = await self.user_repository.save(user)

            user_scheme = UserConverter.entity_to_graphql(updated_user)

            return UserUpdateResponse(success=True, data=user_scheme, message="User updated successfully")

        except Exception as e:
            return UserUpdateResponse(success=False, message=str(e), error_code="UPDATE_ERROR")
