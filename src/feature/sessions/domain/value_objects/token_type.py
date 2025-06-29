# src/feature/sessions/domain/value_objects/token_type.py
import strawberry
from enum import Enum


@strawberry.enum
class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"

    def __str__(self) -> str:
        return self.value

    @classmethod
    def from_string(cls, value: str) -> "TokenType":
        for token_type in cls:
            if token_type.value == value.lower():
                return token_type
        raise ValueError(f"Invalid token type: {value}")

