from uuid import UUID

from src.core.domain.value_objects.email import Email
from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.inputs.find_one import UserFindOneInput
from src.feature.users.domain.types.find_one import UserFindOneResponse, UserFindOneData
from src.feature.users.domain.schemes.user import UserGraphQLType  # ✅ USAR NUEVO NOMBRE
from src.feature.users.domain.enums.status import UserStatus as GraphQLUserStatus
from src.feature.users.domain.value_objects.user_status import UserStatus
from src.feature.users.infrastructure.converters.user_converter import UserConverter


class UserFindOneService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def dispatch(self, input: UserFindOneInput) -> UserFindOneResponse:
        """Dispatch find one user operation"""
        try:
            user = None

            if input.user_id:
                user_id = UUID(input.user_id)
                user = await self.user_repository.find_by_id(user_id)
            elif input.email:
                email = Email(input.email)
                user = await self.user_repository.find_by_email(email)

            if not user:
                return UserFindOneResponse(success=False, data=UserFindOneData(user=None), message="User not found", error_code="USER_NOT_FOUND")

            user_scheme = UserConverter.entity_to_graphql(user)

            return UserFindOneResponse(success=True, data=UserFindOneData(user=user_scheme), message="User retrieved successfully")

        except Exception as e:
            return UserFindOneResponse(success=False, data=UserFindOneData(user=None), message=str(e), error_code="FIND_ONE_ERROR")
