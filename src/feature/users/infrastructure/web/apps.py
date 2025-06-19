# src/feature/users/infrastructure/web/apps.py
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field: str = "django.db.models.BigAutoField"
    name: str = "src.feature.users.infrastructure.web"
    label: str = "users"
    verbose_name: str = "Users Management"

    def ready(self):
        """Import models when app is ready"""
        # Import the models to ensure they are registered
        from src.feature.users.infrastructure.database import models

