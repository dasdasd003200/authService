# src/feature/users/application/use_cases/delete_user.py - NEW SIMPLIFIED
# from uuid import UUID
from src.core.application.use_cases.base_crud_use_cases import DeleteEntityUseCase
from src.feature.users.domain.entities.user import User
from src.feature.users.domain.repositories.user_repository import UserRepository


class DeleteUserUseCase(DeleteEntityUseCase[User]):
    """Use case for deleting users - inherits all functionality!"""

    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository, "User")

    # No additional code needed! Base class handles everything.
    # If you need custom logic, override execute method.
