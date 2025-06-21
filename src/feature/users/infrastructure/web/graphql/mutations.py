# src/feature/users/infrastructure/web/graphql/mutations.py
import graphene
from graphene import ObjectType, Mutation, String, Boolean, Field
from asgiref.sync import sync_to_async

from src.core.exceptions.base_exceptions import ValidationException, ConflictError
from src.feature.users.application.use_cases.create_user import (
    CreateUserUseCase,
    CreateUserCommand,
)
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository
from src.feature.users.infrastructure.web.graphql.types import UserType


class CreateUserInput(graphene.InputObjectType):
    """Input for creating user"""

    email = String(required=True, description="User email")
    password = String(required=True, description="User password")
    first_name = String(required=True, description="User first name")
    last_name = String(required=True, description="User last name")
    email_verified = Boolean(default_value=False, description="Email verified")


class CreateUserPayload(ObjectType):
    """Response for creating user"""

    success = Boolean(description="Indicates if operation was successful")
    user = Field(UserType, description="Created user")
    message = String(description="Response message")
    error_code = String(description="Error code if applicable")


class UserData:
    """Simple data container for GraphQL UserType"""

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)


class CreateUserResponse:
    """Response object for CreateUser mutation"""

    def __init__(
        self, success: bool, user=None, message: str = "", error_code: str = ""
    ):
        self.success = success
        self.user = user
        self.message = message
        self.error_code = error_code


class CreateUser(Mutation):
    """Mutation for creating a new user"""

    class Arguments:
        input = CreateUserInput(required=True)

    Output = CreateUserPayload

    def mutate(self, info, input):
        """Executes the mutation - SYNC VERSION"""

        async def create_user_async():
            """Async helper function"""
            try:
                # Create the use case
                repository = DjangoUserRepository()
                use_case = CreateUserUseCase(repository)

                # Create command
                command = CreateUserCommand(
                    email=input.email,
                    password=input.password,
                    first_name=input.first_name,
                    last_name=input.last_name,
                    email_verified=input.email_verified,
                )

                # Execute use case
                result = await use_case.execute(command)

                # Create user data object for GraphQL
                user_data = UserData(
                    id=result.user_id,
                    email=result.email,
                    first_name=input.first_name,
                    last_name=input.last_name,
                    full_name=result.full_name,
                    status=result.status,
                    email_verified=result.email_verified,
                )

                return CreateUserResponse(
                    success=True, user=user_data, message="User created successfully"
                )

            except ValidationException as e:
                return CreateUserResponse(
                    success=False, message=str(e), error_code=e.error_code
                )

            except ConflictError as e:
                return CreateUserResponse(
                    success=False, message=str(e), error_code=e.error_code
                )

            except Exception as e:
                return CreateUserResponse(
                    success=False,
                    message=f"Internal server error: {str(e)}",
                    error_code="INTERNAL_ERROR",
                )

        # Convert async to sync using sync_to_async
        import asyncio

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(create_user_async())
            return result
        finally:
            loop.close()


class UserMutations(ObjectType):
    """User mutations"""

    create_user = CreateUser.Field()
