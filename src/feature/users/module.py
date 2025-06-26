# src/feature/users/module.py
"""
Users module following Clean Architecture - UPDATED
Structure: Infrastructure GraphQL → Infrastructure Services → Application Use Cases → Domain → Infrastructure Repositories
"""

from .application.use_cases.user_use_cases import UserUseCases
from .infrastructure.services.create import UserCreateService
from .infrastructure.services.update import UserUpdateService
from .infrastructure.services.delete import UserDeleteService
from .infrastructure.services.find import UserFindService
from .infrastructure.services.find_one import UserFindOneService
from .infrastructure.database.repositories import DjangoUserRepository

# CAMBIO: Importamos desde infrastructure/graphql en lugar de presentation
from .infrastructure.graphql.user_resolvers import UserResolvers, UserQueries, UserMutations


class UserModule:
    """
    Users module configuration - Clean Architecture compliant
    """

    # Application Layer
    use_cases = [UserUseCases]

    # Infrastructure Services (Adapters)
    services = [
        UserCreateService,
        UserUpdateService,
        UserDeleteService,
        UserFindService,
        UserFindOneService,
    ]

    # GraphQL Resolvers (Infrastructure - no longer presentation)
    resolvers = [
        UserResolvers,
        UserQueries,
        UserMutations,
    ]

    # Repository (Infrastructure)
    repository = DjangoUserRepository

    @classmethod
    def configure_dependency_injection(cls):
        """Configure DI container for this feature"""
        from config.services import ServiceRegistry

        # Repository (singleton)
        ServiceRegistry.register("users.repository", cls._create_repository)

        # Use Cases (transient - depends on repository)
        ServiceRegistry.register("users.use_cases", cls._create_use_cases)

        # Infrastructure Services (transient - depends on use cases)
        ServiceRegistry.register("users.create_service", cls._create_create_service)
        ServiceRegistry.register("users.update_service", cls._create_update_service)
        ServiceRegistry.register("users.delete_service", cls._create_delete_service)
        ServiceRegistry.register("users.find_service", cls._create_find_service)
        ServiceRegistry.register("users.find_one_service", cls._create_find_one_service)

        print("✅ Users module configured with Clean Architecture")

    # ===== FACTORY METHODS =====
    @staticmethod
    def _create_repository():
        return DjangoUserRepository()

    @staticmethod
    def _create_use_cases():
        from config.services import ServiceRegistry

        return UserUseCases(ServiceRegistry.get("users.repository"))

    @staticmethod
    def _create_create_service():
        from config.services import ServiceRegistry

        return UserCreateService(ServiceRegistry.get("users.use_cases"))

    @staticmethod
    def _create_update_service():
        from config.services import ServiceRegistry

        return UserUpdateService(ServiceRegistry.get("users.use_cases"))

    @staticmethod
    def _create_delete_service():
        from config.services import ServiceRegistry

        return UserDeleteService(ServiceRegistry.get("users.use_cases"))

    @staticmethod
    def _create_find_service():
        from config.services import ServiceRegistry

        return UserFindService(ServiceRegistry.get("users.use_cases"))

    @staticmethod
    def _create_find_one_service():
        from config.services import ServiceRegistry

        return UserFindOneService(ServiceRegistry.get("users.use_cases"))

