# ===== CREAR: src/feature/users/module.py =====
"""
Users module following the clean architecture pattern
This structure allows easy replication of other features
"""

from .application.command_handlers.create import UserCreateCommandHandler
from .application.command_handlers.update import UserUpdateCommandHandler
from .application.command_handlers.delete import UserDeleteCommandHandler
from .application.query_handlers.find import UserFindQueryHandler
from .application.query_handlers.find_one import UserFindOneQueryHandler

from .infrastructure.services.create import UserCreateService
from .infrastructure.services.update import UserUpdateService
from .infrastructure.services.delete import UserDeleteService
from .infrastructure.services.find import UserFindService
from .infrastructure.services.find_one import UserFindOneService

from .infrastructure.database.repositories import DjangoUserRepository
from .presentation.graphql.resolvers.mutations.create import UserCreateResolver
from .presentation.graphql.resolvers.mutations.update import UserUpdateResolver
from .presentation.graphql.resolvers.mutations.delete import UserDeleteResolver
from .presentation.graphql.resolvers.queries.find import UserFindResolver
from .presentation.graphql.resolvers.queries.find_one import UserFindOneResolver


class UserModule:
    """
    Users module configuration
    Pattern: Each feature has its own independent module
    """

    # Command Handlers
    command_handlers = [
        UserCreateCommandHandler,
        UserUpdateCommandHandler,
        UserDeleteCommandHandler,
    ]

    # Query Handlers
    query_handlers = [
        UserFindQueryHandler,
        UserFindOneQueryHandler,
    ]

    # Services
    services = [
        UserCreateService,
        UserUpdateService,
        UserDeleteService,
        UserFindService,
        UserFindOneService,
    ]

    # GraphQL Resolvers
    resolvers = [
        UserCreateResolver,
        UserUpdateResolver,
        UserDeleteResolver,
        UserFindResolver,
        UserFindOneResolver,
    ]

    # Repository
    repository = DjangoUserRepository

    @classmethod
    def configure_dependency_injection(cls):
        """Configure DI container for this feature"""
        from config.services import ServiceRegistry

        # Repository (singleton)
        ServiceRegistry.register("users.repository", cls._create_repository)

        # Services (transient)
        ServiceRegistry.register("users.create_service", cls._create_create_service)
        ServiceRegistry.register("users.update_service", cls._create_update_service)
        ServiceRegistry.register("users.delete_service", cls._create_delete_service)
        ServiceRegistry.register("users.find_service", cls._create_find_service)
        ServiceRegistry.register("users.find_one_service", cls._create_find_one_service)

        # Command Handlers (transient)
        ServiceRegistry.register("users.create_handler", cls._create_create_handler)
        ServiceRegistry.register("users.update_handler", cls._create_update_handler)
        ServiceRegistry.register("users.delete_handler", cls._create_delete_handler)

        # Query Handlers (transient)
        ServiceRegistry.register("users.find_handler", cls._create_find_handler)
        ServiceRegistry.register("users.find_one_handler", cls._create_find_one_handler)

        print("✅ Users: DI services registered")

    @staticmethod
    def _create_repository():
        return DjangoUserRepository()

    @staticmethod
    def _create_create_service():
        from config.services import ServiceRegistry

        return UserCreateService(ServiceRegistry.get("users.repository"))

    @staticmethod
    def _create_update_service():
        from config.services import ServiceRegistry

        return UserUpdateService(ServiceRegistry.get("users.repository"))

    @staticmethod
    def _create_delete_service():
        from config.services import ServiceRegistry

        return UserDeleteService(ServiceRegistry.get("users.repository"))

    @staticmethod
    def _create_find_service():
        from config.services import ServiceRegistry

        return UserFindService(ServiceRegistry.get("users.repository"))

    @staticmethod
    def _create_find_one_service():
        from config.services import ServiceRegistry

        return UserFindOneService(ServiceRegistry.get("users.repository"))

    @staticmethod
    def _create_create_handler():
        from config.services import ServiceRegistry

        return UserCreateCommandHandler(ServiceRegistry.get("users.create_service"))

    @staticmethod
    def _create_update_handler():
        from config.services import ServiceRegistry

        return UserUpdateCommandHandler(ServiceRegistry.get("users.update_service"))

    @staticmethod
    def _create_delete_handler():
        from config.services import ServiceRegistry

        return UserDeleteCommandHandler(ServiceRegistry.get("users.delete_service"))

    @staticmethod
    def _create_find_handler():
        from config.services import ServiceRegistry

        return UserFindQueryHandler(ServiceRegistry.get("users.find_service"))

    @staticmethod
    def _create_find_one_handler():
        from config.services import ServiceRegistry

        return UserFindOneQueryHandler(ServiceRegistry.get("users.find_one_service"))
