# src/feature/users/domain/entities/user.py
from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from src.core.domain.entities.base_entity import BaseEntity
from src.core.domain.value_objects.email import Email
from src.feature.users.domain.value_objects.user_status import UserStatus
from src.feature.users.domain.value_objects.password import Password


class User(BaseEntity):
    """Entidad User del dominio"""

    def __init__(
        self,
        email: Email,
        password: Password,
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
        self.password = password
        self.first_name = first_name.strip()
        self.last_name = last_name.strip()
        self.status = status
        self.email_verified = email_verified
        self.last_login = last_login
        self.failed_login_attempts = failed_login_attempts

        self._validate()

    def _validate(self):
        """Validar integridad de la entidad"""
        if not self.first_name:
            raise ValueError("First name es requerido")
        if not self.last_name:
            raise ValueError("Last name es requerido")
        if len(self.first_name) > 50:
            raise ValueError("First name muy largo")
        if len(self.last_name) > 50:
            raise ValueError("Last name muy largo")

    @property
    def full_name(self) -> str:
        """Nombre completo del usuario"""
        return f"{self.first_name} {self.last_name}"

    @property
    def is_active(self) -> bool:
        """Verifica si el usuario está activo"""
        return self.status == UserStatus.ACTIVE

    @property
    def is_locked(self) -> bool:
        """Verifica si el usuario está bloqueado"""
        return self.failed_login_attempts >= 5

    def deactivate(self):
        """Desactiva el usuario"""
        self.status = UserStatus.INACTIVE
        self.update_timestamp()

    def activate(self):
        """Activa el usuario"""
        self.status = UserStatus.ACTIVE
        self.update_timestamp()

    def verify_email(self):
        """Marca el email como verificado"""
        self.email_verified = True
        self.update_timestamp()

    def record_login_success(self):
        """Registra un login exitoso"""
        self.last_login = datetime.now(timezone.utc)
        self.failed_login_attempts = 0
        self.update_timestamp()

    def record_login_failure(self):
        """Registra un intento de login fallido"""
        self.failed_login_attempts += 1
        self.update_timestamp()

    def reset_failed_attempts(self):
        """Resetea los intentos fallidos"""
        self.failed_login_attempts = 0
        self.update_timestamp()

    def change_password(self, new_password: Password):
        """Cambia la contraseña del usuario"""
        self.password = new_password
        self.update_timestamp()

    def update_profile(
        self, first_name: Optional[str] = None, last_name: Optional[str] = None
    ):
        """Actualiza el perfil del usuario"""
        if first_name:
            self.first_name = first_name.strip()
        if last_name:
            self.last_name = last_name.strip()
        self.update_timestamp()
        self._validate()

