# src/feature/users/infrastructure/services/find.py
from typing import List

from ...application.use_cases.user_use_cases import UserUseCases
from ...domain.inputs.find import UserFindInput
from ...domain.types.find import UserFindResponse, UserFindData
from ..converters.user_converter import UserConverter
from src.shared.criteria.factory import CriteriaFactory  # ✅ CORRECTO: desde shared
from src.shared.criteria.base_criteria import CriteriaBuilder  # ✅ CORRECTO: desde shared
from src.core.exceptions.base_exceptions import BaseDomainException  # ✅ CORRECTO: desde core


class UserFindService:
    """Infrastructure Service - Adapter for user search"""

    def __init__(self, user_use_cases: UserUseCases):
        self.user_use_cases = user_use_cases

    async def dispatch(self, input: UserFindInput) -> UserFindResponse:
        """Adapter method: GraphQL input → Use Case → GraphQL response"""
        try:
            # Build criteria from GraphQL input
            criteria = self._build_criteria(input)

            # Call Application Use Case
            users, total_count = await self.user_use_cases.find_users_with_criteria(criteria)

            # Convert to GraphQL response
            user_graphql_list = UserConverter.entities_to_graphql(users)

            return UserFindResponse(success=True, data=UserFindData(users=user_graphql_list), total_count=total_count, message="Users retrieved successfully")

        except BaseDomainException as e:
            return UserFindResponse(success=False, data=UserFindData(users=[]), total_count=0, message=e.message, error_code=e.error_code)
        except Exception as e:
            return UserFindResponse(success=False, data=UserFindData(users=[]), total_count=0, message=str(e), error_code="FIND_ERROR")

    def _build_criteria(self, input: UserFindInput) -> List:
        """Build criteria from GraphQL input - Infrastructure concern"""
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

