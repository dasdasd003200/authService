from typing import Dict, Any

from src.core.domain.value_objects.email import Email
from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.entities.user import User
from src.feature.users.domain.value_objects.user_status import UserStatus
from src.feature.users.domain.inputs.create import UserCreateInput
from src.feature.users.domain.types.create import UserCreateResponse
from src.feature.users.domain.schemes.user import UserGraphQLType
from src.feature.users.domain.enums.status import UserStatus as GraphQLUserStatus
from src.feature.users.infrastructure.converters.user_converter import UserConverter


class UserCreateService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def dispatch(self, input: UserCreateInput, user_context: Dict[str, Any]) -> UserCreateResponse:
        """Dispatch create user operation"""
        try:
            email = Email(input.email)
            if await self.user_repository.exists_by_email(email):
                return UserCreateResponse(success=False, message=f"User with email {input.email} already exists", error_code="USER_ALREADY_EXISTS")

            user = User(
                email=email,
                first_name=input.first_name,
                last_name=input.last_name,
                status=UserStatus.PENDING_VERIFICATION if not input.email_verified else UserStatus.ACTIVE,
                email_verified=input.email_verified,
            )

            saved_user = await self.user_repository.save_with_password(user, input.password)

            user_scheme = UserConverter.entity_to_graphql(saved_user)

            return UserCreateResponse(success=True, data=user_scheme, message="User created successfully")

        except Exception as e:
            return UserCreateResponse(success=False, message=str(e), error_code="CREATE_ERROR")
