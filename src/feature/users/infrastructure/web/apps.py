"""
Django app configuration for Users feature
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """Users app configuration - Django estándar"""

    default_auto_field = "django.db.models.BigAutoField"
    name = "src.feature.users.infrastructure.web"
    label = "users"
    verbose_name = "Users Management"

    def ready(self):
        """
        Ejecutar cuando la app esté lista
        AQUÍ es donde Django apps se auto-configuran
        """
        # 1. Configurar DI del feature
        self._configure_dependency_injection()

        # 2. Configurar settings específicos del feature (opcional)
        self._configure_feature_settings()

        # 3. Import models to ensure they're registered
        from src.feature.users.infrastructure.database import models

        print("✅ Users app fully configured")

    def _configure_dependency_injection(self):
        """Configurar DI cuando Django esté listo"""
        from src.feature.users.infrastructure.dependency_injection.module import UsersModule

        UsersModule.configure()
        print("🔌 Users: DI configured via AppConfig")

    def _configure_feature_settings(self):
        """Configurar settings específicos del feature"""
        from django.conf import settings

        # Solo si no existen ya
        if not hasattr(settings, "USERS_CONFIG"):
            settings.USERS_CONFIG = {
                "MAX_LOGIN_ATTEMPTS": 5,
                "EMAIL_VERIFICATION_REQUIRED": True,
                "PASSWORD_RESET_TIMEOUT": 24 * 60 * 60,
            }

        print("🔧 Users: Feature settings configured")

