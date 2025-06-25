# src/feature/users/infrastructure/services/create.py
from typing import Dict, Any

from ...application.use_cases.user_use_cases import UserUseCases
from ...domain.inputs.create import UserCreateInput
from ...domain.types.create import UserCreateResponse
from ..converters.user_converter import UserConverter
from src.core.exceptions.base_exceptions import BaseDomainException  # ✅ CORRECTO: desde core


class UserCreateService:
    """
    Infrastructure Service - Adapter between GraphQL and Application layer

    RESPONSABILIDADES:
    - Convertir GraphQL inputs a domain types
    - Llamar Use Cases (Application layer)
    - Convertir domain entities a GraphQL responses
    - Manejar errores y crear responses adecuadas
    - NO lógica de negocio (eso va en Use Cases)
    """

    def __init__(self, user_use_cases: UserUseCases):
        self.user_use_cases = user_use_cases

    async def dispatch(self, input: UserCreateInput, user_context: Dict[str, Any]) -> UserCreateResponse:
        """
        Adapter method: GraphQL input → Use Case → GraphQL response
        """
        try:
            # Call Application Use Case (business logic)
            user = await self.user_use_cases.create_user(email=input.email, password=input.password, first_name=input.first_name, last_name=input.last_name, email_verified=input.email_verified)

            # Convert domain entity to GraphQL type
            user_graphql = UserConverter.entity_to_graphql(user)

            return UserCreateResponse(success=True, data=user_graphql, message="User created successfully")

        except BaseDomainException as e:
            return UserCreateResponse(success=False, message=e.message, error_code=e.error_code)
        except Exception as e:
            return UserCreateResponse(success=False, message=str(e), error_code="CREATE_ERROR")
