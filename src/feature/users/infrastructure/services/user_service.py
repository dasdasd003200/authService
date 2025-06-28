# src/feature/users/infrastructure/services/user_service.py
from typing import Dict, Any, List
from uuid import UUID

# Import the generic criteria system
from src.shared.criteria.base_criteria import Criteria, Filters, Orders, Filter, Order, FilterOperator, SortDirection
from src.shared.criteria.prepare import PrepareFind, PrepareFindOne
from src.shared.criteria.input_converter import CriteriaInputConverter

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
    """Complete user service using generic Criteria system"""

    def __init__(self, user_use_cases: UserUseCases):
        self.user_use_cases = user_use_cases

    # ===== QUERIES =====

    async def find_users(self, input: UserFindInput) -> UserFindResponse:
        """Find users - supports both criteria and legacy inputs"""
        try:
            # Build criteria from input
            criteria = self._build_find_criteria(input)

            # Create prepare object (like your NestJS approach)
            prepare = PrepareFind(criteria=criteria)

            # Execute use case with criteria
            users, total_count = await self.user_use_cases.find_users_with_criteria(prepare)

            # Convert to GraphQL
            user_graphql_list = UserConverter.entities_to_graphql(users)

            return UserFindResponse(success=True, data=UserFindData(users=user_graphql_list), total_count=total_count, message="Users retrieved successfully")

        except BaseDomainException as e:
            return UserFindResponse(success=False, data=UserFindData(users=[]), total_count=0, message=e.message, error_code=e.error_code)
        except Exception as e:
            return UserFindResponse(success=False, data=UserFindData(users=[]), total_count=0, message=str(e), error_code="INTERNAL_ERROR")

    async def find_user_one(self, input: UserFindOneInput) -> UserFindOneResponse:
        """Find one user - supports both criteria and legacy inputs"""
        try:
            # Build criteria from input
            criteria = self._build_find_one_criteria(input)

            # Create prepare object (like your NestJS approach)
            prepare = PrepareFindOne(filters=criteria.filters)

            # Execute use case
            user = await self.user_use_cases.find_user_one_with_criteria(prepare)

            # Convert to GraphQL
            user_graphql = UserConverter.entity_to_graphql(user) if user else None

            return UserFindOneResponse(success=True, data=UserFindOneData(user=user_graphql), message="User retrieved successfully")

        except BaseDomainException as e:
            return UserFindOneResponse(success=False, data=UserFindOneData(user=None), message=e.message, error_code=e.error_code)
        except Exception as e:
            return UserFindOneResponse(success=False, data=UserFindOneData(user=None), message=str(e), error_code="INTERNAL_ERROR")

    # ===== MUTATIONS =====

    async def create_user(self, input: UserCreateInput, user_context: Dict[str, Any]) -> UserCreateResponse:
        """Create a new user"""
        try:
            user = await self.user_use_cases.create_user(email=input.email, password=input.password, first_name=input.first_name, last_name=input.last_name, email_verified=input.email_verified)

            user_graphql = UserConverter.entity_to_graphql(user)

            return UserCreateResponse(success=True, data=user_graphql, message="User created successfully")

        except BaseDomainException as e:
            return UserCreateResponse(success=False, data=None, message=e.message, error_code=e.error_code)
        except Exception as e:
            return UserCreateResponse(success=False, data=None, message=str(e), error_code="INTERNAL_ERROR")

    async def update_user(self, input: UserUpdateInput, user_context: Dict[str, Any]) -> UserUpdateResponse:
        """Update an existing user"""
        try:
            user_id = validate_uuid(input.user_id, "User ID")

            user = await self.user_use_cases.update_user(user_id=user_id, first_name=input.first_name, last_name=input.last_name)

            user_graphql = UserConverter.entity_to_graphql(user)

            return UserUpdateResponse(success=True, data=user_graphql, message="User updated successfully")

        except BaseDomainException as e:
            return UserUpdateResponse(success=False, data=None, message=e.message, error_code=e.error_code)
        except Exception as e:
            return UserUpdateResponse(success=False, data=None, message=str(e), error_code="INTERNAL_ERROR")

    async def delete_user(self, user_id: str, user_context: Dict[str, Any]) -> UserDeleteResponse:
        """Delete a user"""
        try:
            user_uuid = validate_uuid(user_id, "User ID")

            success = await self.user_use_cases.delete_user(user_uuid)

            return UserDeleteResponse(success=success, message="User deleted successfully" if success else "Failed to delete user")

        except BaseDomainException as e:
            return UserDeleteResponse(success=False, message=e.message, error_code=e.error_code)
        except Exception as e:
            return UserDeleteResponse(success=False, message=str(e), error_code="INTERNAL_ERROR")

    # ===== PRIVATE HELPER METHODS =====

    def _build_find_criteria(self, input: UserFindInput) -> Criteria:
        """Build criteria from input - supports both direct criteria and legacy fields"""

        # If direct criteria is provided, use it (like your NestJS approach)
        if input.criteria:
            return CriteriaInputConverter.from_graphql_input(input.criteria)

        # Otherwise, build from legacy fields
        builder = Criteria.builder()

        # Build filters
        filters = []

        if input.status:
            filters.append(Filter(field="status", operator=FilterOperator.EQ, value=input.status))

        if input.email_verified is not None:
            filters.append(Filter(field="email_verified", operator=FilterOperator.EQ, value=input.email_verified))

        if input.search_text:
            # Generic text search
            search_filters = [Filter(field="first_name", operator=FilterOperator.ICONTAINS, value=input.search_text), Filter(field="last_name", operator=FilterOperator.ICONTAINS, value=input.search_text), Filter(field="email", operator=FilterOperator.ICONTAINS, value=input.search_text)]
            filters.append(Filter(field="", operator=FilterOperator.OR, value=None, nested_filters=search_filters))

        if filters:
            builder.set_filters(Filters(filters))

        # Build orders
        orders = []
        if input.order_by:
            for order_field in input.order_by:
                if order_field.startswith("-"):
                    orders.append(Order(field=order_field[1:], direction=SortDirection.DESC))
                else:
                    orders.append(Order(field=order_field, direction=SortDirection.ASC))
        else:
            orders.append(Order(field="created_at", direction=SortDirection.DESC))

        builder.set_orders(Orders(orders))

        # Set pagination
        offset = (input.page - 1) * input.page_size
        builder.set_limit(input.page_size)
        builder.set_offset(offset)

        return builder.build()

    def _build_find_one_criteria(self, input: UserFindOneInput) -> Criteria:
        """Build criteria for findOne - supports both direct criteria and legacy fields"""

        # If direct criteria is provided, use it
        if input.criteria:
            return CriteriaInputConverter.from_graphql_input(input.criteria)

        # Otherwise, build from legacy fields
        filters = []

        if input.user_id:
            filters.append(Filter(field="id", operator=FilterOperator.EQ, value=UUID(input.user_id)))

        if input.email:
            filters.append(Filter(field="email", operator=FilterOperator.EQ, value=input.email))

        return Criteria(filters=Filters(filters))

