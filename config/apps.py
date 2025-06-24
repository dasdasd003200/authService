"""
Configuración de aplicación Django - LIMPIO
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuración de la aplicación core"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.core"

    def ready(self):
        """Ejecutar cuando Django esté listo"""
        # Solo configurar modules - ¡NO containers!
        from config.app_modules import configure_all_modules

        configure_all_modules()

