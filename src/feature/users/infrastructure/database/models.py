# src/feature/users/infrastructure/database/models.py
import uuid
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    """Custom manager for User model"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(email, password, **extra_fields)


class UserModel(AbstractBaseUser):
    """Django model for users"""

    class StatusChoices(models.TextChoices):
        ACTIVE = "active", "Active"
        INACTIVE = "inactive", "Inactive"
        SUSPENDED = "suspended", "Suspended"
        PENDING_VERIFICATION = "pending_verification", "Pending Verification"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, max_length=255, verbose_name="Email Address")
    first_name = models.CharField(max_length=50, verbose_name="First Name")
    last_name = models.CharField(max_length=50, verbose_name="Last Name")
    status = models.CharField(
        max_length=20,
        choices=StatusChoices.choices,
        default=StatusChoices.PENDING_VERIFICATION,
        verbose_name="Status",
    )
    email_verified = models.BooleanField(verbose_name="Email Verified")
    failed_login_attempts = models.IntegerField(verbose_name="Failed Login Attempts")
    last_login = models.DateTimeField(null=True, blank=True, verbose_name="Last Login")

    # Campos para Django Admin
    is_active = models.BooleanField()
    is_staff = models.BooleanField()
    is_superuser = models.BooleanField()

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

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"

    def save(self, *args, **kwargs):
        # Set defaults if not provided (only for fields without defaults)
        if not hasattr(self, "_state") or self._state.adding:
            if self.email_verified is None:
                self.email_verified = False
            if self.failed_login_attempts is None:
                self.failed_login_attempts = 0
            if self.is_active is None:
                self.is_active = True
            if self.is_staff is None:
                self.is_staff = False
            if self.is_superuser is None:
                self.is_superuser = False
        super().save(*args, **kwargs)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def has_perm(self, perm, obj=None):
        _ = perm, obj  # Mark as used
        return self.is_superuser

    def has_module_perms(self, app_label):
        _ = app_label  # Mark as used
        return self.is_superuser

