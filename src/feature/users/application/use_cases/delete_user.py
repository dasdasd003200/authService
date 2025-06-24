from src.core.application.use_cases.base import DeleteEntityUseCase
from src.feature.users.domain.entities.user import User
from src.feature.users.domain.repositories.user_repository import UserRepository


class DeleteUserUseCase(DeleteEntityUseCase[User]):
    """Use case for deleting users - inherits all functionality!"""

    def __init__(self, user_repository: UserRepository):
        super().__init__(user_repository, "User")
