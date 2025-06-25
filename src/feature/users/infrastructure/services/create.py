from typing import Dict, Any

from src.core.domain.value_objects.email import Email
from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.entities.user import User
from src.feature.users.domain.value_objects.user_status import UserStatus
from src.feature.users.domain.inputs.create import UserCreateInput
from src.feature.users.domain.types.create import UserCreateResponse
from src.feature.users.domain.schemes.user import UserGraphQLType  # ✅ USAR NUEVO NOMBRE
from src.feature.users.domain.enums.status import UserStatus as GraphQLUserStatus


class UserCreateService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def dispatch(self, input: UserCreateInput, user_context: Dict[str, Any]) -> UserCreateResponse:
        """Dispatch create user operation"""
        try:
            # Validate email uniqueness
            email = Email(input.email)
            if await self.user_repository.exists_by_email(email):
                return UserCreateResponse(success=False, message=f"User with email {input.email} already exists", error_code="USER_ALREADY_EXISTS")

            # Create user entity
            user = User(
                email=email,
                first_name=input.first_name,
                last_name=input.last_name,
                status=UserStatus.PENDING_VERIFICATION if not input.email_verified else UserStatus.ACTIVE,
                email_verified=input.email_verified,
            )

            # Save user with password
            saved_user = await self.user_repository.save_with_password(user, input.password)

            # Convert to GraphQL scheme
            user_scheme = self._convert_to_scheme(saved_user)

            return UserCreateResponse(success=True, data=user_scheme, message="User created successfully")

        except Exception as e:
            return UserCreateResponse(success=False, message=str(e), error_code="CREATE_ERROR")

    def _convert_to_scheme(self, user: User) -> UserGraphQLType:  # ✅ CAMBIAR TIPO RETORNO
        """Convert domain entity to GraphQL scheme"""
        # Convert domain status to GraphQL enum
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
