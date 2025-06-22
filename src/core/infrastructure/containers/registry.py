# src/core/infrastructure/containers/registry.py
"""
Registry global para containers
"""

from typing import Dict, Type
from .base_container import BaseContainer


class ContainerRegistry:
    """Registry global para todos los containers"""

    _containers: Dict[str, BaseContainer] = {}
    _initialized = False

    @classmethod
    def register(cls, name: str, container: BaseContainer) -> None:
        """Registrar un container"""
        cls._containers[name] = container

    @classmethod
    def get_container(cls, name: str) -> BaseContainer:
        """Obtener un container por nombre"""
        if not cls._initialized:
            cls._initialize_all()

        if name not in cls._containers:
            raise ValueError(f"Container '{name}' not found")
        return cls._containers[name]

    @classmethod
    def _initialize_all(cls) -> None:
        """Inicializar todos los containers"""
        for container in cls._containers.values():
            container.configure()
        cls._initialized = True

    @classmethod
    def reset(cls) -> None:
        """Reset para testing"""
        cls._containers.clear()
        cls._initialized = False


# Función helper para obtener containers fácilmente
def get_container(name: str) -> BaseContainer:
    """Helper function para obtener containers"""
    return ContainerRegistry.get_container(name)
