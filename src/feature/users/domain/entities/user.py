from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from src.core.domain.entities.base_entity import BaseEntity
from src.core.domain.value_objects.email import Email
from src.feature.users.domain.value_objects.user_status import UserStatus


class User(BaseEntity):
    def __init__(
        self,
        email: Email,
        first_name: str,
        last_name: str,
        status: UserStatus = UserStatus.ACTIVE,
        email_verified: bool = False,
        last_login: Optional[datetime] = None,
        failed_login_attempts: int = 0,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        super().__init__(id, created_at, updated_at)
        self.email = email
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.status = status
        self.email_verified = email_verified
        self.last_login = last_login
        self.failed_login_attempts = failed_login_attempts

        self._validate()

    def _validate(self):
        """Validate entity integrity"""
        if not self.first_name:
            raise ValueError("First name is required")
        if not self.last_name:
            raise ValueError("Last name is required")
        if len(self.first_name) > 50:
            raise ValueError("First name too long")
        if len(self.last_name) > 50:
            raise ValueError("Last name too long")

    @property
    def full_name(self) -> str:
        """User's full name"""
        return f"{self.first_name} {self.last_name}"

    @property
    def is_active(self) -> bool:
        """Check if user is active"""
        return self.status == UserStatus.ACTIVE

    @property
    def is_locked(self) -> bool:
        """Check if user is locked"""
        return self.failed_login_attempts >= 5

    def deactivate(self):
        """Deactivate user"""
        self.status = UserStatus.INACTIVE
        self.update_timestamp()

    def activate(self):
        """Activate user"""
        self.status = UserStatus.ACTIVE
        self.update_timestamp()

    def verify_email(self):
        """Mark email as verified"""
        self.email_verified = True
        self.update_timestamp()

    def record_login_success(self):
        """Record successful login"""
        self.last_login = datetime.now(timezone.utc)
        self.failed_login_attempts = 0
        self.update_timestamp()

    def record_login_failure(self):
        """Record failed login attempt"""
        self.failed_login_attempts += 1
        self.update_timestamp()

    def reset_failed_attempts(self):
        """Reset failed attempts"""
        self.failed_login_attempts = 0
        self.update_timestamp()

    def update_profile(self, first_name: Optional[str] = None, last_name: Optional[str] = None):
        """Update user profile"""
        if first_name:
            self.first_name = first_name.strip()
        if last_name:
            self.last_name = last_name.strip()
        self.update_timestamp()
        self._validate()
