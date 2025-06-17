# src/core/exceptions/base_exceptions.py
from typing import Optional, Dict, Any


class BaseDomainException(Exception):
    """Excepción base del dominio"""

    def __init__(
        self,
        message: str,
        error_code: Optional[str] = None,
        details: Optional[Dict[str, Any]] = None,
    ):
        self.message = message
        self.error_code = error_code or self.__class__.__name__
        self.details = details or {}
        super().__init__(self.message)


class ValidationException(BaseDomainException):
    """Excepción para errores de validación"""

    pass


class NotFoundError(BaseDomainException):
    """Excepción para recursos no encontrados"""

    pass


class ConflictError(BaseDomainException):
    """Excepción para conflictos (ej: duplicados)"""

    pass


class UnauthorizedError(BaseDomainException):
    """Excepción para errores de autorización"""

    pass
