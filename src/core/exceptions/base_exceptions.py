from typing import Optional, Dict, Any


class BaseDomainException(Exception):
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
    pass


class NotFoundError(BaseDomainException):
    pass


class ConflictError(BaseDomainException):
    pass


class UnauthorizedError(BaseDomainException):
    pass
