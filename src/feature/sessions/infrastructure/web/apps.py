from django.apps import AppConfig


class SessionsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "src.feature.sessions.infrastructure.web"
    label = "auth_sessions"  # ⬅️ CAMBIO: Evitar conflicto con django.contrib.sessions
    verbose_name = "Authentication Sessions"

    def ready(self):
        print("🔐 Auth Sessions feature ready")
