from typing import List

from src.shared.criteria.factory import CriteriaFactory
from src.shared.criteria.base_criteria import CriteriaBuilder
from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.inputs.find import UserFindInput
from src.feature.users.domain.types.find import UserFindResponse, UserFindData
from src.feature.users.domain.schemes.user import UserGraphQLType  # ✅ USAR NUEVO NOMBRE
from src.feature.users.domain.enums.status import UserStatus as GraphQLUserStatus
from src.feature.users.domain.value_objects.user_status import UserStatus


class UserFindService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def dispatch(self, input: UserFindInput) -> UserFindResponse:
        """Dispatch find users operation"""
        try:
            # Build criteria
            criteria = self._build_criteria(input)

            # Find users
            users = await self.user_repository.find_by_criteria(criteria)
            total_count = await self.user_repository.count_by_criteria(criteria)

            # Convert to schemes
            user_schemes = [self._convert_to_scheme(user) for user in users]

            return UserFindResponse(success=True, data=UserFindData(users=user_schemes), total_count=total_count, message="Users retrieved successfully")

        except Exception as e:
            return UserFindResponse(success=False, data=UserFindData(users=[]), total_count=0, message=str(e), error_code="FIND_ERROR")

    def _build_criteria(self, input: UserFindInput) -> List:
        """Build criteria from input"""
        criteria_builder = CriteriaBuilder()

        # Filters
        if input.status:
            criteria_builder.add(CriteriaFactory.status(input.status))

        if input.email_verified is not None:
            criteria_builder.add(CriteriaFactory.boolean_field("email_verified", input.email_verified))

        if input.search_text:
            criteria_builder.add(CriteriaFactory.text_search(input.search_text, ["first_name", "last_name", "email"]))

        # Pagination
        offset = (input.page - 1) * input.page_size
        criteria_builder.add(CriteriaFactory.paginate(input.page_size, offset))

        # Ordering
        if input.order_by:
            criteria_builder.add(CriteriaFactory.order_by(input.order_by))

        return criteria_builder.build()

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
