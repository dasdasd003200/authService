from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.feature.users.infrastructure.web"
    label = "users"
    verbose_name = "Users Management"

    def ready(self):
        # Configure this feature's DI using the new module
        from ...module import UserModule

        UserModule.configure_dependency_injection()

        print("✅ Users feature configured with clean architecture")

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
