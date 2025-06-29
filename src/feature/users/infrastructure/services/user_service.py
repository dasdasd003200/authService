# src/feature/users/infrastructure/services/user_service.py
from typing import Dict, Any

from src.core.infrastructure.web.strawberry.services.base_service import BaseService
from src.core.infrastructure.web.strawberry.responses import FindData, FindOneData
from src.shared.criteria.service_helper import CriteriaServiceHelper
from ...application.use_cases.user_use_cases import UserUseCases
from ...domain.inputs.create import UserCreateInput
from ...domain.inputs.update import UserUpdateInput
from ...domain.inputs.find import UserFindInput
from ...domain.inputs.find_one import UserFindOneInput
from ...domain.types.standard_responses import UserCreateResponse, UserUpdateResponse, UserDeleteResponse, UserFindResponse, UserFindOneResponse
from ...domain.schemes.user import UserGraphQLType
from ...domain.schemes.user_fields import UserFields
from src.core.exceptions.base_exceptions import BaseDomainException
from src.core.infrastructure.web.strawberry.helpers.validators import validate_uuid


class UserService(BaseService):
    def __init__(self, user_use_cases: UserUseCases):
        super().__init__("User")
        self.user_use_cases = user_use_cases
        self.criteria_helper = CriteriaServiceHelper(feature_name="user", search_fields=["first_name", "last_name", "email"], boolean_fields=["email_verified"], string_fields=["email", "status"])

    # ===== QUERIES =====
    async def find(self, input: UserFindInput) -> UserFindResponse:
        try:
            prepare = self.criteria_helper.build_find_prepare(input)
            # CAMBIO: usar método heredado del core
            users, total_count = await self.user_use_cases.find_with_criteria(prepare)

            user_graphql_list = UserGraphQLType.from_entities(users)
            response_data = self.handle_success_find(user_graphql_list, total_count)

            return UserFindResponse(success=response_data["success"], data=FindData(items=response_data["data"]), total_count=response_data["total_count"], message=response_data["message"])
        except BaseDomainException as e:
            error_data = self.handle_exception(e, [])
            return UserFindResponse(success=error_data["success"], data=FindData(items=error_data["data"]), total_count=0, message=error_data["message"], error_code=error_data["error_code"])

    async def find_one(self, input: UserFindOneInput) -> UserFindOneResponse:
        try:
            prepare = self.criteria_helper.build_find_one_prepare(input)
            # CAMBIO: usar método heredado del core
            user = await self.user_use_cases.find_one_with_criteria(prepare)

            user_graphql = UserGraphQLType.from_entity(user) if user else None
            response_data = self.handle_success_find_one(user_graphql)

            return UserFindOneResponse(success=response_data["success"], data=FindOneData(item=response_data["data"]), message=response_data["message"])
        except BaseDomainException as e:
            error_data = self.handle_exception(e, None)
            return UserFindOneResponse(success=error_data["success"], data=FindOneData(item=error_data["data"]), message=error_data["message"], error_code=error_data["error_code"])

    # ===== MUTATIONS =====
    async def create(self, input: UserCreateInput, user_context: Dict[str, Any]) -> UserCreateResponse:
        try:
            create_args = UserFields.create_user_args(input)
            user = await self.user_use_cases.create_user(**create_args)

            user_graphql = UserGraphQLType.from_entity(user)
            response_data = self.handle_success_create(user_graphql)

            return UserCreateResponse(success=response_data["success"], data=response_data["data"], message=response_data["message"])
        except BaseDomainException as e:
            error_data = self.handle_exception(e, None)
            return UserCreateResponse(success=error_data["success"], data=error_data["data"], message=error_data["message"], error_code=error_data["error_code"])

    async def update(self, input: UserUpdateInput, user_context: Dict[str, Any]) -> UserUpdateResponse:
        try:
            user_id = validate_uuid(input.user_id, "User ID")
            update_args = UserFields.update_user_args(input)
            user = await self.user_use_cases.update_user(user_id=user_id, **update_args)

            user_graphql = UserGraphQLType.from_entity(user)
            response_data = self.handle_success_update(user_graphql)

            return UserUpdateResponse(success=response_data["success"], data=response_data["data"], message=response_data["message"])
        except BaseDomainException as e:
            error_data = self.handle_exception(e, None)
            return UserUpdateResponse(success=error_data["success"], data=error_data["data"], message=error_data["message"], error_code=error_data["error_code"])

    async def delete(self, user_id: str, user_context: Dict[str, Any]) -> UserDeleteResponse:
        try:
            user_uuid = validate_uuid(user_id, "User ID")
            # CAMBIO: usar método heredado del core
            success = await self.user_use_cases.delete_by_id(user_uuid)

            if success:
                response_data = self.handle_success_delete()
                return UserDeleteResponse(success=response_data["success"], message=response_data["message"], affected_count=response_data.get("affected_count"))
            else:
                return UserDeleteResponse(success=False, message="Failed to delete user", error_code="DELETE_FAILED")
        except BaseDomainException as e:
            error_data = self.handle_exception(e)
            return UserDeleteResponse(success=error_data["success"], message=error_data["message"], error_code=error_data["error_code"])

