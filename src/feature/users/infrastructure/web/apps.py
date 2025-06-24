from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.feature.users.infrastructure.web"
    label = "users"
    verbose_name = "Users Management"

    def ready(self):
        self._configure_dependency_injection()
        self._configure_feature_settings()
        from src.feature.users.infrastructure.database import models

        print("✅ Users app fully configured")

    def _configure_dependency_injection(self):
        from src.feature.users.infrastructure.dependency_injection.module import UsersModule

        UsersModule.configure()
        print("🔌 Users: DI configured via AppConfig")

    def _configure_feature_settings(self):
        from django.conf import settings

        if not hasattr(settings, "USERS_CONFIG"):
            settings.USERS_CONFIG = {
                "MAX_LOGIN_ATTEMPTS": 5,
                "EMAIL_VERIFICATION_REQUIRED": True,
                "PASSWORD_RESET_TIMEOUT": 24 * 60 * 60,
            }

        print("🔧 Users: Feature settings configured")
