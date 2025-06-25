from uuid import UUID

from src.core.domain.value_objects.email import Email
from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.inputs.find_one import UserFindOneInput
from src.feature.users.domain.types.find_one import UserFindOneResponse, UserFindOneData
from src.feature.users.domain.schemes.user import UserGraphQLType  # ✅ USAR NUEVO NOMBRE
from src.feature.users.domain.enums.status import UserStatus as GraphQLUserStatus
from src.feature.users.domain.value_objects.user_status import UserStatus


class UserFindOneService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def dispatch(self, input: UserFindOneInput) -> UserFindOneResponse:
        """Dispatch find one user operation"""
        try:
            user = None

            # Find by ID or email
            if input.user_id:
                user_id = UUID(input.user_id)
                user = await self.user_repository.find_by_id(user_id)
            elif input.email:
                email = Email(input.email)
                user = await self.user_repository.find_by_email(email)

            if not user:
                return UserFindOneResponse(success=False, data=UserFindOneData(user=None), message="User not found", error_code="USER_NOT_FOUND")

            # Convert to scheme
            user_scheme = self._convert_to_scheme(user)

            return UserFindOneResponse(success=True, data=UserFindOneData(user=user_scheme), message="User retrieved successfully")

        except Exception as e:
            return UserFindOneResponse(success=False, data=UserFindOneData(user=None), message=str(e), error_code="FIND_ONE_ERROR")

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

