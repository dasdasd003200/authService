"""
Users Module - SOLO configuración de DI
"""

from config.services import ServiceRegistry


class UsersModule:
    """Module que configura servicios de Users - SOLO DI"""

    @staticmethod
    def configure():
        """Configurar servicios DI del feature Users"""

        # Repository (singleton)
        ServiceRegistry.register("users.repository", UsersModule._create_user_repository)

        # Use Cases (transient)
        ServiceRegistry.register("users.create_use_case", UsersModule._create_create_user_use_case)
        ServiceRegistry.register("users.get_use_case", UsersModule._create_get_user_use_case)
        ServiceRegistry.register("users.update_use_case", UsersModule._create_update_user_use_case)
        ServiceRegistry.register("users.delete_use_case", UsersModule._create_delete_user_use_case)
        ServiceRegistry.register("users.search_use_case", UsersModule._create_search_user_use_case)
        ServiceRegistry.register("users.deactivate_use_case", UsersModule._create_deactivate_user_use_case)

        print("🔌 Users: DI services registered")

    # Factory methods (sin cambios)
    @staticmethod
    def _create_user_repository():
        from src.feature.users.infrastructure.database.repositories import DjangoUserRepository

        return DjangoUserRepository()

    @staticmethod
    def _create_create_user_use_case():
        from src.feature.users.application.use_cases.create_user import CreateUserUseCase

        return CreateUserUseCase(ServiceRegistry.get("users.repository"))

    @staticmethod
    def _create_get_user_use_case():
        from src.feature.users.application.use_cases.get_user import GetUserUseCase

        return GetUserUseCase(ServiceRegistry.get("users.repository"))

    @staticmethod
    def _create_update_user_use_case():
        from src.feature.users.application.use_cases.update_user import UpdateUserUseCase

        return UpdateUserUseCase(ServiceRegistry.get("users.repository"))

    @staticmethod
    def _create_delete_user_use_case():
        from src.feature.users.application.use_cases.delete_user import DeleteUserUseCase

        return DeleteUserUseCase(ServiceRegistry.get("users.repository"))

    @staticmethod
    def _create_search_user_use_case():
        from src.feature.users.application.use_cases.search_users import SearchUsersUseCase

        return SearchUsersUseCase(ServiceRegistry.get("users.repository"))

    @staticmethod
    def _create_deactivate_user_use_case():
        from src.feature.users.application.use_cases.update_user import DeactivateUserUseCase

        return DeactivateUserUseCase(ServiceRegistry.get("users.repository"))

