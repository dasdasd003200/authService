# src/feature/users/infrastructure/web/graphql/mutations.py
import graphene
from graphene import ObjectType, Mutation, String, Boolean, Field

from src.core.exceptions.base_exceptions import ValidationException, ConflictError
from src.feature.users.application.use_cases.create_user import (
    CreateUserUseCase,
    CreateUserCommand,
)
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository
from src.feature.users.infrastructure.web.graphql.types import UserType


class CreateUserInput(graphene.InputObjectType):
    """Input para crear usuario"""

    email = String(required=True, description="Email del usuario")
    password = String(required=True, description="Contraseña del usuario")
    first_name = String(required=True, description="Nombre del usuario")
    last_name = String(required=True, description="Apellido del usuario")
    email_verified = Boolean(default_value=False, description="Email verificado")


class CreateUserPayload(ObjectType):
    """Respuesta de crear usuario"""

    success = Boolean(description="Indica si la operación fue exitosa")
    user = Field(UserType, description="Usuario creado")
    message = String(description="Mensaje de respuesta")
    error_code = String(description="Código de error si aplica")


class CreateUser(Mutation):
    """Mutation para crear un nuevo usuario"""

    class Arguments:
        input = CreateUserInput(required=True)

    Output = CreateUserPayload

    async def mutate(self, info, input):
        """Ejecuta la mutation"""
        try:
            # Crear el caso de uso
            repository = DjangoUserRepository()
            use_case = CreateUserUseCase(repository)

            # Crear comando
            command = CreateUserCommand(
                email=input.email,
                password=input.password,
                first_name=input.first_name,
                last_name=input.last_name,
                email_verified=input.email_verified,
            )

            # Ejecutar caso de uso
            result = await use_case.execute(command)

            return CreateUserPayload(
                success=True,
                user=UserType(
                    id=result.user_id,
                    email=result.email,
                    first_name=input.first_name,
                    last_name=input.last_name,
                    full_name=result.full_name,
                    status=result.status,
                    email_verified=result.email_verified,
                ),
                message="Usuario creado exitosamente",
            )

        except ValidationException as e:
            return CreateUserPayload(
                success=False, message=str(e), error_code=e.error_code
            )

        except ConflictError as e:
            return CreateUserPayload(
                success=False, message=str(e), error_code=e.error_code
            )

        except Exception as e:
            return CreateUserPayload(
                success=False,
                message="Error interno del servidor",
                error_code="INTERNAL_ERROR",
            )


class UserMutations(ObjectType):
    """Mutations de usuarios"""

    create_user = CreateUser.Field()
