from datetime import datetime, timezone, timedelta
from typing import Optional
from uuid import UUID

from src.core.domain.entities.base_entity import BaseEntity
from ..value_objects.token_type import TokenType
from ..value_objects.session_status import SessionStatus


class Session(BaseEntity):
    def __init__(
        self,
        user_id: UUID,
        token_type: TokenType,
        expires_at: datetime,
        status: SessionStatus = SessionStatus.ACTIVE,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        device_info: Optional[str] = None,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        super().__init__(id, created_at, updated_at)
        self.user_id = user_id
        self.token_type = token_type
        self.expires_at = expires_at
        self.status = status
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.device_info = device_info

    @property
    def is_active(self) -> bool:
        return self.status == SessionStatus.ACTIVE and self.expires_at > datetime.now(timezone.utc)

    @property
    def is_expired(self) -> bool:
        return self.expires_at <= datetime.now(timezone.utc)

    def revoke(self):
        self.status = SessionStatus.REVOKED
        self.update_timestamp()

    def logout(self):
        self.status = SessionStatus.LOGGED_OUT
        self.update_timestamp()

    def extend_expiry(self, additional_minutes: int = 60):
        if self.is_active:
            self.expires_at = datetime.now(timezone.utc) + timedelta(minutes=additional_minutes)
            self.update_timestamp()

    @classmethod
    def create_access_token_session(
        cls,
        user_id: UUID,
        duration_minutes: int = 60,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> "Session":
        expires_at = datetime.now(timezone.utc) + timedelta(minutes=duration_minutes)
        return cls(
            user_id=user_id,
            token_type=TokenType.ACCESS,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent,
        )

    @classmethod
    def create_refresh_token_session(
        cls,
        user_id: UUID,
        duration_days: int = 7,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
    ) -> "Session":
        expires_at = datetime.now(timezone.utc) + timedelta(days=duration_days)
        return cls(
            user_id=user_id,
            token_type=TokenType.REFRESH,
            expires_at=expires_at,
            ip_address=ip_address,
            user_agent=user_agent,
        )
