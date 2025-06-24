from typing import Dict, Any, Callable
import threading


class ServiceRegistry:
    """Registry global de servicios"""

    _services: Dict[str, Any] = {}
    _factories: Dict[str, Callable] = {}
    _lock = threading.Lock()

    @classmethod
    def register(cls, name: str, factory: Callable):
        with cls._lock:
            cls._factories[name] = factory
        print(f"📝 Service registered: {name}")

    @classmethod
    def get(cls, name: str):
        """Obtener servicio (singleton)"""
        if name in cls._services:
            return cls._services[name]

        if name not in cls._factories:
            raise ValueError(f"Service '{name}' not registered")

        with cls._lock:
            if name not in cls._services:
                cls._services[name] = cls._factories[name]()
            return cls._services[name]

    @classmethod
    def create(cls, name: str):
        """Crear nueva instancia (transient)"""
        if name not in cls._factories:
            raise ValueError(f"Service '{name}' not registered")
        return cls._factories[name]()

    @classmethod
    def reset(cls):
        """Reset para testing"""
        cls._services.clear()
        cls._factories.clear()
