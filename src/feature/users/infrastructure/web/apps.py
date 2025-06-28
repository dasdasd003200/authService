from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.feature.users.infrastructure.web"
    label = "users"
    verbose_name = "Users Management"

    def ready(self):
        print("✅ Users feature ready")

