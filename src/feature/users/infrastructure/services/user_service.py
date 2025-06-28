from typing import Dict, Any

from src.shared.criteria.service_helper import CriteriaServiceHelper
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
from src.core.exceptions.base_exceptions import BaseDomainException
from src.core.infrastructure.web.strawberry.helpers.validators import validate_uuid


class UserService:
    def __init__(self, user_use_cases: UserUseCases):
        self.user_use_cases = user_use_cases
        # Initialize shared criteria helper with user-specific search fields
        self.criteria_helper = CriteriaServiceHelper(feature_name="user", search_fields=["first_name", "last_name", "email"], boolean_fields=["email_verified"], string_fields=["email", "status"])

    # ===== QUERIES (Super clean) =====

    async def find(self, input: UserFindInput) -> UserFindResponse:
        try:
            prepare = self.criteria_helper.build_find_prepare(input)
            users, total_count = await self.user_use_cases.find_users_with_criteria(prepare)
            user_graphql_list = UserConverter.entities_to_graphql(users)
            return UserFindResponse(success=True, data=UserFindData(users=user_graphql_list), total_count=total_count, message="Users retrieved successfully")
        except BaseDomainException as e:
            return UserFindResponse(success=False, data=UserFindData(users=[]), total_count=0, message=e.message, error_code=e.error_code)
        except Exception as e:
            return UserFindResponse(success=False, data=UserFindData(users=[]), total_count=0, message=str(e), error_code="INTERNAL_ERROR")

    async def find_one(self, input: UserFindOneInput) -> UserFindOneResponse:
        try:
            prepare = self.criteria_helper.build_find_one_prepare(input)
            user = await self.user_use_cases.find_user_one_with_criteria(prepare)
            user_graphql = UserConverter.entity_to_graphql(user) if user else None
            return UserFindOneResponse(success=True, data=UserFindOneData(user=user_graphql), message="User retrieved successfully")
        except BaseDomainException as e:
            return UserFindOneResponse(success=False, data=UserFindOneData(user=None), message=e.message, error_code=e.error_code)
        except Exception as e:
            return UserFindOneResponse(success=False, data=UserFindOneData(user=None), message=str(e), error_code="INTERNAL_ERROR")

    # ===== MUTATIONS (Super clean) =====

    async def create(self, input: UserCreateInput, user_context: Dict[str, Any]) -> UserCreateResponse:
        try:
            user = await self.user_use_cases.create_user(email=input.email, password=input.password, first_name=input.first_name, last_name=input.last_name, email_verified=input.email_verified)
            user_graphql = UserConverter.entity_to_graphql(user)
            return UserCreateResponse(success=True, data=user_graphql, message="User created successfully")
        except BaseDomainException as e:
            return UserCreateResponse(success=False, data=None, message=e.message, error_code=e.error_code)
        except Exception as e:
            return UserCreateResponse(success=False, data=None, message=str(e), error_code="INTERNAL_ERROR")

    async def update(self, input: UserUpdateInput, user_context: Dict[str, Any]) -> UserUpdateResponse:
        try:
            user_id = validate_uuid(input.user_id, "User ID")
            user = await self.user_use_cases.update_user(user_id=user_id, first_name=input.first_name, last_name=input.last_name)
            user_graphql = UserConverter.entity_to_graphql(user)
            return UserUpdateResponse(success=True, data=user_graphql, message="User updated successfully")
        except BaseDomainException as e:
            return UserUpdateResponse(success=False, data=None, message=e.message, error_code=e.error_code)
        except Exception as e:
            return UserUpdateResponse(success=False, data=None, message=str(e), error_code="INTERNAL_ERROR")

    async def delete(self, user_id: str, user_context: Dict[str, Any]) -> UserDeleteResponse:
        try:
            user_uuid = validate_uuid(user_id, "User ID")
            success = await self.user_use_cases.delete_user(user_uuid)
            return UserDeleteResponse(success=success, message="User deleted successfully" if success else "Failed to delete user")

        except BaseDomainException as e:
            return UserDeleteResponse(success=False, message=e.message, error_code=e.error_code)
        except Exception as e:
            return UserDeleteResponse(success=False, message=str(e), error_code="INTERNAL_ERROR")
