# src/core/application/use_cases/base_crud_use_cases.py - CLEANED
from dataclasses import dataclass
from typing import TypeVar, Generic, Optional
from uuid import UUID

from src.core.domain.entities.base_entity import BaseEntity
from src.core.domain.repositories.base_repository import BaseRepository
from src.core.exceptions.base_exceptions import NotFoundError
from src.core.application.interfaces.base_use_case import BaseUseCase

T = TypeVar("T", bound=BaseEntity)


@dataclass
class GetEntityByIdQuery:
    """Generic query for getting entity by ID"""

    entity_id: UUID


@dataclass
class DeleteEntityCommand:
    """Generic command for deleting entity"""

    entity_id: UUID


class GetEntityByIdUseCase(BaseUseCase[GetEntityByIdQuery, Optional[T]], Generic[T]):
    """Base use case for getting entity by ID"""

    def __init__(self, repository: BaseRepository[T], entity_name: str = "Entity"):
        self.repository = repository
        self.entity_name = entity_name

    async def execute(self, query: GetEntityByIdQuery) -> Optional[T]:
        """Execute get entity by ID"""
        entity = await self.repository.find_by_id(query.entity_id)

        if not entity:
            raise NotFoundError(
                f"{self.entity_name} with ID {query.entity_id} not found",
                error_code=f"{self.entity_name.upper()}_NOT_FOUND",
            )

        return entity


class DeleteEntityUseCase(BaseUseCase[DeleteEntityCommand, bool], Generic[T]):
    """Base use case for deleting entity"""

    def __init__(self, repository: BaseRepository[T], entity_name: str = "Entity"):
        self.repository = repository
        self.entity_name = entity_name

    async def execute(self, command: DeleteEntityCommand) -> bool:
        """Execute delete entity"""
        # Check if entity exists first
        entity = await self.repository.find_by_id(command.entity_id)
        if not entity:
            raise NotFoundError(
                f"{self.entity_name} with ID {command.entity_id} not found",
                error_code=f"{self.entity_name.upper()}_NOT_FOUND",
            )

        return await self.repository.delete(command.entity_id)


# src/feature/users/application/use_cases/delete_user.py - CLEANED
from src.core.application.use_cases.base_crud_use_cases import DeleteEntityUseCase
from src.feature.users.domain.entities.user import User
from src.feature.users.domain.repositories.user_repository import UserRepository


class DeleteUserUseCase(DeleteEntityUseCase[User]):
    """Use case for deleting users - inherits all functionality!"""

    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository, "User")


# src/feature/users/application/use_cases/get_user.py - CLEANED
from dataclasses import dataclass
from typing import Optional

from src.core.application.use_cases.base_crud_use_cases import GetEntityByIdUseCase
from src.core.domain.value_objects.email import Email
from src.core.exceptions.base_exceptions import NotFoundError
from src.feature.users.domain.entities.user import User
from src.feature.users.domain.repositories.user_repository import UserRepository


@dataclass
class GetUserByEmailQuery:
    """Query for getting user by email"""

    email: str


@dataclass
class GetUserResult:
    """Result of getting user"""

    user_id: str
    email: str
    first_name: str
    last_name: str
    full_name: str
    status: str
    email_verified: bool
    last_login: Optional[str] = None
    failed_login_attempts: int = 0


class GetUserUseCase(GetEntityByIdUseCase[User]):
    """Use case for retrieving users - inherits get_by_id functionality"""

    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository, "User")
        self.user_repository = user_repository

    async def execute_by_email(self, query: GetUserByEmailQuery) -> GetUserResult:
        """Get user by email - only user-specific method"""
        email = Email(query.email)
        user = await self.user_repository.find_by_email(email)

        if not user:
            raise NotFoundError(
                f"User with email {query.email} not found", error_code="USER_NOT_FOUND"
            )

        return self._user_to_result(user)

    def _user_to_result(self, user: User) -> GetUserResult:
        """Convert user entity to result"""
        return GetUserResult(
            user_id=str(user.id),
            email=str(user.email),
            first_name=user.first_name,
            last_name=user.last_name,
            full_name=user.full_name,
            status=user.status.value,
            email_verified=user.email_verified,
            last_login=user.last_login.isoformat() if user.last_login else None,
            failed_login_attempts=user.failed_login_attempts,
        )

