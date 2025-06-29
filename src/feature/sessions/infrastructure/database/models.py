import uuid
from django.db import models
from django.conf import settings


class SessionModel(models.Model):
    class TokenTypeChoices(models.TextChoices):
        ACCESS = "access", "Access Token"
        REFRESH = "refresh", "Refresh Token"

    class StatusChoices(models.TextChoices):
        ACTIVE = "active", "Active"
        EXPIRED = "expired", "Expired"
        REVOKED = "revoked", "Revoked"
        LOGGED_OUT = "logged_out", "Logged Out"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    # User relationship
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="auth_sessions",  # ⬅️ CAMBIO: Evitar conflicto
        verbose_name="User",
    )

    # Session data
    token_type = models.CharField(max_length=10, choices=TokenTypeChoices.choices, verbose_name="Token Type")
    status = models.CharField(max_length=15, choices=StatusChoices.choices, default=StatusChoices.ACTIVE, verbose_name="Status")
    expires_at = models.DateTimeField(verbose_name="Expires At")

    # Device/Client info
    ip_address = models.GenericIPAddressField(null=True, blank=True, verbose_name="IP Address")
    user_agent = models.TextField(null=True, blank=True, verbose_name="User Agent")
    device_info = models.CharField(max_length=255, null=True, blank=True, verbose_name="Device Info")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    class Meta:
        app_label = "auth_sessions"  # ⬅️ CAMBIO: Nuevo label
        db_table = "auth_sessions"  # ⬅️ CAMBIO: Nueva tabla
        verbose_name = "Authentication Session"
        verbose_name_plural = "Authentication Sessions"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["token_type", "status"]),
            models.Index(fields=["expires_at"]),
            models.Index(fields=["created_at"]),
            models.Index(fields=["user", "token_type", "status"]),
        ]

    def __str__(self) -> str:
        return f"{self.user.email} - {self.token_type} ({self.status})"

    @property
    def user_id(self) -> uuid.UUID:
        return self.user.id if self.user else None

    def clean(self):
        super().clean()
        # Add any model-level validation here if needed
