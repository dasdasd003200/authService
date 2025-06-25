from uuid import UUID
from typing import Dict, Any

from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.inputs.update import UserUpdateInput
from src.feature.users.domain.types.update import UserUpdateResponse
from src.feature.users.domain.schemes.user import UserGraphQLType  # ✅ USAR NUEVO NOMBRE
from src.feature.users.domain.enums.status import UserStatus as GraphQLUserStatus
from src.feature.users.domain.value_objects.user_status import UserStatus


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

            # Update user
            user.update_profile(first_name=input.first_name, last_name=input.last_name)

            # Save user
            updated_user = await self.user_repository.save(user)

            # Convert to GraphQL scheme
            user_scheme = self._convert_to_scheme(updated_user)

            return UserUpdateResponse(success=True, data=user_scheme, message="User updated successfully")

        except Exception as e:
            return UserUpdateResponse(success=False, message=str(e), error_code="UPDATE_ERROR")

    def _convert_to_scheme(self, user) -> UserGraphQLType:  # ✅ CAMBIAR TIPO RETORNO
        """Convert domain entity to GraphQL scheme"""
        graphql_status = GraphQLUserStatus.ACTIVE
        if user.status == UserStatus.INACTIVE:
            graphql_status = GraphQLUserStatus.INACTIVE
        elif user.status == UserStatus.SUSPENDED:
            graphql_status = GraphQLUserStatus.SUSPENDED
        elif user.status == UserStatus.PENDING_VERIFICATION:
            graphql_status = GraphQLUserStatus.PENDING_VERIFICATION

        return UserGraphQLType(  # ✅ CAMBIAR CLASE
            id=str(user.id),
            email=str(user.email),
            first_name=user.first_name,
            last_name=user.last_name,
            full_name=user.full_name,
            status=graphql_status,
            email_verified=user.email_verified,
            last_login=user.last_login,
            failed_login_attempts=user.failed_login_attempts,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )

