# src/core/infrastructure/containers/base_container.py
"""
Base container para dependency injection
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Type, TypeVar, Callable
import threading

T = TypeVar("T")


class BaseContainer(ABC):
    """
    Contenedor base para inyección de dependencias
    Implementa singleton pattern y lazy loading
    """

    def __init__(self):
        self._instances: Dict[str, Any] = {}
        self._factories: Dict[str, Callable] = {}
        self._lock = threading.Lock()

    def register_singleton(self, name: str, factory: Callable[[], T]) -> None:
        """Registrar una factory que crea singletons"""
        with self._lock:
            self._factories[name] = factory

    def register_transient(self, name: str, factory: Callable[[], T]) -> None:
        """Registrar una factory que crea nuevas instancias cada vez"""
        # Para transient, no guardamos instancias
        with self._lock:
            self._factories[name] = factory

    def get(self, name: str) -> Any:
        """Obtener una instancia por nombre"""
        # Verificar si ya tenemos la instancia (singleton)
        if name in self._instances:
            return self._instances[name]

        # Verificar si tenemos la factory
        if name not in self._factories:
            raise ValueError(f"No factory registered for '{name}'")

        # Crear la instancia
        with self._lock:
            # Double-check locking pattern
            if name not in self._instances:
                instance = self._factories[name]()
                self._instances[name] = instance
            return self._instances[name]

    def create_new(self, name: str) -> Any:
        """Crear una nueva instancia (para transient dependencies)"""
        if name not in self._factories:
            raise ValueError(f"No factory registered for '{name}'")
        return self._factories[name]()

    @abstractmethod
    def configure(self) -> None:
        """Configurar las dependencias del contenedor"""
        pass


class ContainerError(Exception):
    """Error específico del contenedor"""

    pass
