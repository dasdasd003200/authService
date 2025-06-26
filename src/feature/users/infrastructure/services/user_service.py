from typing import Dict, Any, List
from uuid import UUID

from ...application.use_cases.user_use_cases import UserUseCases

from ...domain.inputs.create import UserCreateInput
from ...domain.inputs.update import UserUpdateInput
from ...domain.inputs.find import UserFindInput
from ...domain.inputs.find_one import UserFindOneInput
from ...domain.types.create import UserCreateResponse
from ...domain.types.update import UserUpdateResponse
from ...domain.types.delete import UserDeleteResponse
from ...domain.types.find import UserFindResponse, UserFindData
from ...domain.types.find_one import UserFindOneResponse, UserFindOneData

from ..converters.user_converter import UserConverter

from src.shared.criteria.factory import CriteriaFactory
from src.shared.criteria.base_criteria import CriteriaBuilder

from src.core.exceptions.base_exceptions import BaseDomainException


class UserService:
    def __init__(self, user_use_cases: UserUseCases):
        self.user_use_cases = user_use_cases

    # ===== CREATE OPERATIONS =====

    async def create_user(self, input: UserCreateInput, user_context: Dict[str, Any] = None) -> UserCreateResponse:
        try:
            user = await self.user_use_cases.create_user(email=input.email, password=input.password, first_name=input.first_name, last_name=input.last_name, email_verified=input.email_verified)
            user_graphql = UserConverter.entity_to_graphql(user)
            return UserCreateResponse(success=True, data=user_graphql, message="User created successfully")

        except BaseDomainException as e:
            return UserCreateResponse(success=False, message=e.message, error_code=e.error_code)
        except Exception as e:
            return UserCreateResponse(success=False, message=str(e), error_code="CREATE_ERROR")

    # ===== UPDATE OPERATIONS =====

    async def update_user(self, input: UserUpdateInput, user_context: Dict[str, Any] = None) -> UserUpdateResponse:
        try:
            user = await self.user_use_cases.update_user(user_id=UUID(input.user_id), first_name=input.first_name, last_name=input.last_name)
            user_graphql = UserConverter.entity_to_graphql(user)
            return UserUpdateResponse(success=True, data=user_graphql, message="User updated successfully")

        except BaseDomainException as e:
            return UserUpdateResponse(success=False, message=e.message, error_code=e.error_code)
        except Exception as e:
            return UserUpdateResponse(success=False, message=str(e), error_code="UPDATE_ERROR")

    # ===== DELETE OPERATIONS =====

    async def delete_user(self, user_id: str, user_context: Dict[str, Any] = None) -> UserDeleteResponse:
        try:
            deleted = await self.user_use_cases.delete_user(UUID(user_id))

            if deleted:
                return UserDeleteResponse(success=True, message="User deleted successfully")
            else:
                return UserDeleteResponse(success=False, message="Failed to delete user", error_code="DELETE_FAILED")

        except BaseDomainException as e:
            return UserDeleteResponse(success=False, message=e.message, error_code=e.error_code)
        except Exception as e:
            return UserDeleteResponse(success=False, message=str(e), error_code="DELETE_ERROR")

    # ===== QUERY OPERATIONS =====

    async def find_users(self, input: UserFindInput) -> UserFindResponse:
        try:
            criteria = self._build_find_criteria(input)
            users, total_count = await self.user_use_cases.find_users_with_criteria(criteria)
            user_graphql_list = UserConverter.entities_to_graphql(users)

            return UserFindResponse(success=True, data=UserFindData(users=user_graphql_list), total_count=total_count, message="Users retrieved successfully")

        except BaseDomainException as e:
            return UserFindResponse(success=False, data=UserFindData(users=[]), total_count=0, message=e.message, error_code=e.error_code)
        except Exception as e:
            return UserFindResponse(success=False, data=UserFindData(users=[]), total_count=0, message=str(e), error_code="FIND_ERROR")

    async def find_user_one(self, input: UserFindOneInput) -> UserFindOneResponse:
        try:
            user = None
            if input.user_id:
                user = await self.user_use_cases.find_user_by_id(UUID(input.user_id))
            elif input.email:
                user = await self.user_use_cases.find_user_by_email(input.email)
            else:
                return UserFindOneResponse(success=False, data=UserFindOneData(user=None), message="Either user_id or email must be provided", error_code="MISSING_SEARCH_CRITERIA")
            user_graphql = UserConverter.entity_to_graphql(user) if user else None

            return UserFindOneResponse(success=True, data=UserFindOneData(user=user_graphql), message="User retrieved successfully")

        except BaseDomainException as e:
            return UserFindOneResponse(success=False, data=UserFindOneData(user=None), message=e.message, error_code=e.error_code)
        except Exception as e:
            return UserFindOneResponse(success=False, data=UserFindOneData(user=None), message=str(e), error_code="FIND_ONE_ERROR")

    # ===== PRIVATE HELPER METHODS =====

    def _build_find_criteria(self, input: UserFindInput) -> List:
        criteria_builder = CriteriaBuilder()

        if input.status:
            criteria_builder.add(CriteriaFactory.status(input.status))

        if input.email_verified is not None:
            criteria_builder.add(CriteriaFactory.boolean_field("email_verified", input.email_verified))

        if input.search_text:
            criteria_builder.add(CriteriaFactory.text_search(input.search_text, ["first_name", "last_name", "email"]))

        offset = (input.page - 1) * input.page_size
        criteria_builder.add(CriteriaFactory.paginate(input.page_size, offset))

        if input.order_by:
            criteria_builder.add(CriteriaFactory.order_by(input.order_by))
        else:
            criteria_builder.add(CriteriaFactory.order_by(["-created_at"]))

        return criteria_builder.build()

    def _handle_error(self, error: Exception, response_class, default_message: str = "An error occurred"):
        if isinstance(error, BaseDomainException):
            return response_class(success=False, message=error.message, error_code=error.error_code)

        return response_class(success=False, message=str(error) if str(error) else default_message, error_code="INTERNAL_ERROR")
