# src/core/domain/value_objects/email.py
import re
from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class Email:
    """Value Object para email con validación"""

    value: str
    EMAIL_PATTERN: ClassVar[str] = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    def __post_init__(self):
        if not self.value:
            raise ValueError("Email no puede estar vacío")

        if not re.match(self.EMAIL_PATTERN, self.value):
            raise ValueError(f"Email inválido: {self.value}")

        # Normalizar email a lowercase
        object.__setattr__(self, "value", self.value.lower().strip())

    def __str__(self) -> str:
        return self.value

    @property
    def domain(self) -> str:
        """Retorna el dominio del email"""
        return self.value.split("@")[1]

    @property
    def local_part(self) -> str:
        """Retorna la parte local del email"""
        return self.value.split("@")[0]
