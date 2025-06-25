# src/feature/users/infrastructure/services/find_one.py
from uuid import UUID

from ...application.use_cases.user_use_cases import UserUseCases
from ...domain.inputs.find_one import UserFindOneInput
from ...domain.types.find_one import UserFindOneResponse, UserFindOneData
from ..converters.user_converter import UserConverter
from src.core.exceptions.base_exceptions import BaseDomainException  # ✅ CORRECTO: desde core


class UserFindOneService:
    """Infrastructure Service - Adapter for single user search"""

    def __init__(self, user_use_cases: UserUseCases):
        self.user_use_cases = user_use_cases

    async def dispatch(self, input: UserFindOneInput) -> UserFindOneResponse:
        """Adapter method: GraphQL input → Use Case → GraphQL response"""
        try:
            user = None

            # Determine search method from input
            if input.user_id:
                user = await self.user_use_cases.find_user_by_id(UUID(input.user_id))
            elif input.email:
                user = await self.user_use_cases.find_user_by_email(input.email)
            else:
                return UserFindOneResponse(success=False, data=UserFindOneData(user=None), message="Either user_id or email must be provided", error_code="MISSING_SEARCH_CRITERIA")

            # Convert to GraphQL response
            user_graphql = UserConverter.entity_to_graphql(user)

            return UserFindOneResponse(success=True, data=UserFindOneData(user=user_graphql), message="User retrieved successfully")

        except BaseDomainException as e:
            return UserFindOneResponse(success=False, data=UserFindOneData(user=None), message=e.message, error_code=e.error_code)
        except Exception as e:
            return UserFindOneResponse(success=False, data=UserFindOneData(user=None), message=str(e), error_code="FIND_ONE_ERROR")

