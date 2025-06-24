"""
Configuración de aplicación Django - ESTÁNDAR
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuración de la aplicación core"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.core"

    def ready(self):
        """Ejecutar cuando Django esté listo"""
        # En Django estándar, cada app se configura a sí misma
        # No necesitamos un configurador central
        print("🚀 Core app ready")

