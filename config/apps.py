from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Configuración de la aplicación core"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.core"

    def ready(self):
        print("🚀 Core app ready")
