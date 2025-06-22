# src/core/infrastructure/containers/django_setup.py
"""
Configuración de containers para Django
"""

from .registry import ContainerRegistry
from src.feature.users.infrastructure.containers import UserContainer


def setup_containers():
    """Configurar todos los containers de la aplicación"""

    # Registrar User Container
    user_container = UserContainer()
    ContainerRegistry.register("users", user_container)

    # Aquí agregarías otros containers cuando tengas más features
    # auth_container = AuthContainer()
    # ContainerRegistry.register('auth', auth_container)

    print("✅ Dependency Injection Containers configured successfully")


def get_user_container() -> UserContainer:
    """Helper para obtener el user container"""
    return ContainerRegistry.get_container("users")
