# config/apps.py
"""
Configuración de aplicación Django
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuración de la aplicación core"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.core"

    def ready(self):
        """Ejecutar cuando Django esté listo"""
        # Configurar containers
        from src.core.infrastructure.containers.django_setup import setup_containers

        setup_containers()
