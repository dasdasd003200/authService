# src/feature/users/module.py
"""
CLEAN User Module - Simple and Direct
"""

from .application.use_cases.user_use_cases import UserUseCases
from .infrastructure.database.repositories import DjangoUserRepository
from .infrastructure.services.user_service import UserService
from .infrastructure.graphql.user_resolvers import UserQueries, UserMutations


class UserModule:
    """Simple module for Users feature"""

    FEATURE_NAME = "users"

    @classmethod
    def get_service(cls):
        """Get user service - simple instantiation"""
        repository = DjangoUserRepository()
        use_cases = UserUseCases(repository)
        return UserService(use_cases)

    @classmethod
    def get_repository(cls):
        return DjangoUserRepository()

    @classmethod
    def get_use_cases(cls):
        repository = DjangoUserRepository()
        return UserUseCases(repository)

    @classmethod
    def get_queries(cls):
        return UserQueries

    @classmethod
    def get_mutations(cls):
        return UserMutations

