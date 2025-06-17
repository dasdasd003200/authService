# src/feature/users/domain/value_objects/password.py
import re
import hashlib
import secrets
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class Password:
    """Value Object para contraseñas con validación y hashing"""

    hashed_value: str
    salt: str

    # Reglas de validación
    MIN_LENGTH: ClassVar[int] = 8
    MAX_LENGTH: ClassVar[int] = 128
    REQUIRE_UPPERCASE: ClassVar[bool] = True
    REQUIRE_LOWERCASE: ClassVar[bool] = True
    REQUIRE_DIGIT: ClassVar[bool] = True
    REQUIRE_SPECIAL: ClassVar[bool] = True
    SPECIAL_CHARS: ClassVar[str] = "!@#$%^&*()_+-=[]{}|;:,.<>?"

    @classmethod
    def create(cls, plain_password: str) -> "Password":
        """Crea una nueva password desde texto plano"""
        cls._validate_password(plain_password)
        salt = secrets.token_hex(32)
        hashed = cls._hash_password(plain_password, salt)
        return cls(hashed_value=hashed, salt=salt)

    @classmethod
    def from_hash(cls, hashed_value: str, salt: str) -> "Password":
        """Crea password desde hash existente (para cargar desde DB)"""
        return cls(hashed_value=hashed_value, salt=salt)

    def verify(self, plain_password: str) -> bool:
        """Verifica si la contraseña coincide"""
        return self.hashed_value == self._hash_password(plain_password, self.salt)

    @classmethod
    def _validate_password(cls, password: str):
        """Valida que la contraseña cumpla los requisitos"""
        if len(password) < cls.MIN_LENGTH:
            raise ValueError(
                f"Password debe tener al menos {cls.MIN_LENGTH} caracteres"
            )

        if len(password) > cls.MAX_LENGTH:
            raise ValueError(
                f"Password no puede tener más de {cls.MAX_LENGTH} caracteres"
            )

        if cls.REQUIRE_UPPERCASE and not re.search(r"[A-Z]", password):
            raise ValueError("Password debe contener al menos una mayúscula")

        if cls.REQUIRE_LOWERCASE and not re.search(r"[a-z]", password):
            raise ValueError("Password debe contener al menos una minúscula")

        if cls.REQUIRE_DIGIT and not re.search(r"\d", password):
            raise ValueError("Password debe contener al menos un número")

        if cls.REQUIRE_SPECIAL and not any(
            char in cls.SPECIAL_CHARS for char in password
        ):
            raise ValueError(
                f"Password debe contener al menos un carácter especial: {cls.SPECIAL_CHARS}"
            )

    @staticmethod
    def _hash_password(password: str, salt: str) -> str:
        """Hashea la contraseña con el salt"""
        return hashlib.pbkdf2_hmac(
            "sha256", password.encode(), salt.encode(), 100000
        ).hex()

    def __str__(self) -> str:
        return "[PROTECTED]"

    def __repr__(self) -> str:
        return "Password([PROTECTED])"
