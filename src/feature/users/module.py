# src/feature/users/module.py
"""
Users module following Clean Architecture - UPDATED
Uses consolidated UserService instead of 5 separate services
"""

from .application.use_cases.user_use_cases import UserUseCases
from .infrastructure.database.repositories import DjangoUserRepository

from .infrastructure.services.user_service import UserService

# GraphQL Resolvers (Infrastructure)
from .infrastructure.graphql.user_resolvers import UserResolvers, UserQueries, UserMutations


class UserModule:
    """
    Users module configuration - Clean Architecture compliant
    UPDATED: Now uses consolidated services
    """

    # Application Layer
    use_cases = [UserUseCases]

    # Infrastructure Services (UPDATED: now only one service)
    services = [
        UserService,  # ← Replaces 5 individual services
    ]

    # GraphQL Resolvers (Infrastructure)
    resolvers = [
        UserResolvers,
        UserQueries,
        UserMutations,
    ]

    # Repository (Infrastructure)
    repository = DjangoUserRepository

    @classmethod
    def configure_dependency_injection(cls):
        """Configure DI container for this feature - UPDATED"""
        from config.services import ServiceRegistry

        # Repository (singleton)
        ServiceRegistry.register("users.repository", cls._create_repository)

        # Use Cases (transient - depends on repository)
        ServiceRegistry.register("users.use_cases", cls._create_use_cases)

        # UPDATED: Single consolidated service instead of 5
        ServiceRegistry.register("users.service", cls._create_user_service)

        print("✅ Users module configured with consolidated UserService")

    # ===== FACTORY METHODS - UPDATED =====

    @staticmethod
    def _create_repository():
        return DjangoUserRepository()

    @staticmethod
    def _create_use_cases():
        from config.services import ServiceRegistry

        return UserUseCases(ServiceRegistry.get("users.repository"))

    @staticmethod
    def _create_user_service():
        """UPDATED: Create consolidated UserService"""
        from config.services import ServiceRegistry

        return UserService(ServiceRegistry.get("users.use_cases"))
