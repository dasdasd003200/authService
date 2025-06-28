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

        self._validate()

    def _validate(self):
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
        return f"{self.first_name} {self.last_name}"

    @property
    def is_active(self) -> bool:
        return self.status == UserStatus.ACTIVE

    def update_profile(self, first_name: Optional[str] = None, last_name: Optional[str] = None):
        if first_name:
            self.first_name = first_name.strip()
        if last_name:
            self.last_name = last_name.strip()
        self.update_timestamp()
        self._validate()
