from typing import List

from src.shared.criteria.factory import CriteriaFactory
from src.shared.criteria.base_criteria import CriteriaBuilder
from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.inputs.find import UserFindInput
from src.feature.users.domain.types.find import UserFindResponse, UserFindData
from src.feature.users.domain.schemes.user import UserGraphQLType  # ✅ USAR NUEVO NOMBRE
from src.feature.users.domain.enums.status import UserStatus as GraphQLUserStatus
from src.feature.users.domain.value_objects.user_status import UserStatus
from src.feature.users.infrastructure.converters.user_converter import UserConverter


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

            user_schemes = UserConverter.entities_to_graphql(users)

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
