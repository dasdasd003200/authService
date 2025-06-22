# src/feature/users/infrastructure/containers/user_container.py
"""
Contenedor de dependencias para Users feature
"""

from src.core.infrastructure.containers.base_container import BaseContainer

# Domain imports
from src.feature.users.domain.repositories.user_repository import UserRepository

# Infrastructure imports
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository

# Application imports
from src.feature.users.application.use_cases.create_user import CreateUserUseCase
from src.feature.users.application.use_cases.get_user import GetUserUseCase
from src.feature.users.application.use_cases.update_user import UpdateUserUseCase, DeactivateUserUseCase
from src.feature.users.application.use_cases.delete_user import DeleteUserUseCase
from src.feature.users.application.use_cases.search_users import SearchUsersUseCase


class UserContainer(BaseContainer):
    """Contenedor para todas las dependencias de Users"""

    def configure(self) -> None:
        """Configurar todas las dependencias"""

        # ===== REPOSITORIES =====
        self.register_singleton("user_repository", lambda: DjangoUserRepository())

        # ===== USE CASES =====
        # Create User
        self.register_transient("create_user_use_case", lambda: CreateUserUseCase(user_repository=self.get("user_repository")))

        # Get User
        self.register_transient("get_user_use_case", lambda: GetUserUseCase(user_repository=self.get("user_repository")))

        # Update User
        self.register_transient("update_user_use_case", lambda: UpdateUserUseCase(user_repository=self.get("user_repository")))

        # Delete User
        self.register_transient("delete_user_use_case", lambda: DeleteUserUseCase(user_repository=self.get("user_repository")))

        # Search Users
        self.register_transient("search_users_use_case", lambda: SearchUsersUseCase(user_repository=self.get("user_repository")))

        # Deactivate User
        self.register_transient("deactivate_user_use_case", lambda: DeactivateUserUseCase(user_repository=self.get("user_repository")))

    # ===== CONVENIENCE METHODS =====
    def get_user_repository(self) -> UserRepository:
        """Get user repository"""
        return self.get("user_repository")

    def get_create_user_use_case(self) -> CreateUserUseCase:
        """Get create user use case"""
        return self.create_new("create_user_use_case")

    def get_get_user_use_case(self) -> GetUserUseCase:
        """Get get user use case"""
        return self.create_new("get_user_use_case")

    def get_update_user_use_case(self) -> UpdateUserUseCase:
        """Get update user use case"""
        return self.create_new("update_user_use_case")

    def get_delete_user_use_case(self) -> DeleteUserUseCase:
        """Get delete user use case"""
        return self.create_new("delete_user_use_case")

    def get_search_users_use_case(self) -> SearchUsersUseCase:
        """Get search users use case"""
        return self.create_new("search_users_use_case")

    def get_deactivate_user_use_case(self) -> DeactivateUserUseCase:
        """Get deactivate user use case"""
        return self.create_new("deactivate_user_use_case")
