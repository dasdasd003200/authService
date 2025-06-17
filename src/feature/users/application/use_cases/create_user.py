# src/feature/users/application/use_cases/create_user.py
from dataclasses import dataclass
from typing import Optional

from src.core.domain.value_objects.email import Email
from src.core.exceptions.base_exceptions import ConflictError
from src.feature.users.domain.entities.user import User
from src.feature.users.domain.repositories.user_repository import UserRepository
from src.feature.users.domain.value_objects.password import Password
from src.feature.users.domain.value_objects.user_status import UserStatus


@dataclass
class CreateUserCommand:
    """Comando para crear usuario"""

    email: str
    password: str
    first_name: str
    last_name: str
    email_verified: bool = False


@dataclass
class CreateUserResult:
    """Resultado de crear usuario"""

    user_id: str
    email: str
    full_name: str
    status: str
    email_verified: bool


class CreateUserUseCase:
    """Caso de uso para crear un nuevo usuario"""

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self, command: CreateUserCommand) -> CreateUserResult:
        """Ejecuta la creación del usuario"""

        # Crear value objects
        email = Email(command.email)
        password = Password.create(command.password)

        # Verificar que no existe el usuario
        if await self.user_repository.exists_by_email(email):
            raise ConflictError(
                f"Ya existe un usuario con el email {email}",
                error_code="USER_ALREADY_EXISTS",
            )

        # Crear la entidad
        user = User(
            email=email,
            password=password,
            first_name=command.first_name,
            last_name=command.last_name,
            status=UserStatus.PENDING_VERIFICATION
            if not command.email_verified
            else UserStatus.ACTIVE,
            email_verified=command.email_verified,
        )

        # Guardar en el repositorio
        saved_user = await self.user_repository.save(user)

        # Retornar resultado
        return CreateUserResult(
            user_id=str(saved_user.id),
            email=str(saved_user.email),
            full_name=saved_user.full_name,
            status=saved_user.status.value,
            email_verified=saved_user.email_verified,
        )
