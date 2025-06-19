# src/feature/users/infrastructure/database/models.py
import uuid
from typing import Any, Optional
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):  # Removed type parameter
    """Custom manager for User model"""

    def create_user(
        self, email: str, password: Optional[str] = None, **extra_fields: Any
    ) -> "UserModel":
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
        self, email: str, password: Optional[str] = None, **extra_fields: Any
    ) -> "UserModel":
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("status", UserModel.StatusChoices.ACTIVE)
        extra_fields.setdefault("email_verified", True)
        return self.create_user(email, password, **extra_fields)


class UserModel(AbstractBaseUser):
    """Django model for users"""

    class StatusChoices(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        SUSPENDED = "suspended", "Suspended"
        PENDING_VERIFICATION = "pending_verification", "Pending Verification"

    # Primary fields
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255, verbose_name="Email Address")
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")

    # Status and verification fields
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING_VERIFICATION,
        verbose_name="Status",
    )
    email_verified = models.BooleanField(default=False, verbose_name="Email Verified")
    failed_login_attempts = (
        models.PositiveIntegerField(  # Changed to PositiveIntegerField
            default=0, verbose_name="Failed Login Attempts"
        )
    )
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="Last Login")

    # Django admin fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated At")

    # Password storage (managed by value object)
    password_hash = models.CharField(
        max_length=255, verbose_name="Password Hash", blank=True
    )
    password_salt = models.CharField(
        max_length=64, verbose_name="Password Salt", blank=True
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name"]

    objects = UserManager()

    class Meta:
        db_table = "users"
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name} ({self.email})"

    @property
    def full_name(self) -> str:
        """Return user's full name"""
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm: str, obj: Any = None) -> bool:
        """Check if user has a specific permission"""
        # Note: perm and obj parameters are required by Django interface
        # but not used in this simple implementation
        _ = perm, obj  # Mark as used to avoid linter warnings
        return self.is_superuser

    def has_module_perms(self, app_label: str) -> bool:
        """Check if user has permissions for a specific app"""
        # Note: app_label parameter is required by Django interface
        # but not used in this simple implementation
        _ = app_label  # Mark as used to avoid linter warnings
        return self.is_superuser
