from typing import Any, List as PyList
from src.core.exceptions.base_exceptions import BaseDomainException


class ResponseBuilder:
    """Centralized response builder with consistent messaging"""

    @staticmethod
    def success_data(data: Any, message: str = None) -> dict:
        """Build successful data response"""
        return {"success": True, "data": data, "message": message or "Operation completed successfully"}

    @staticmethod
    def success_list(data: PyList[Any], total_count: int, message: str = None) -> dict:
        """Build successful list response"""
        return {"success": True, "data": data, "total_count": total_count, "message": message or f"Found {len(data)} items"}

    @staticmethod
    def success_operation(message: str = None, affected_count: int = None) -> dict:
        """Build successful operation response"""
        return {"success": True, "message": message or "Operation completed successfully", "affected_count": affected_count}

    @staticmethod
    def error_from_exception(exception: BaseDomainException, data: Any = None) -> dict:
        """Build error response from domain exception"""
        return {"success": False, "data": data, "message": exception.message, "error_code": exception.error_code}

    @staticmethod
    def error_custom(message: str, error_code: str = "OPERATION_FAILED", data: Any = None) -> dict:
        """Build custom error response"""
        return {"success": False, "data": data, "message": message, "error_code": error_code}

    @staticmethod
    def not_found(entity_name: str, identifier: str = None) -> dict:
        """Build not found response"""
        message = f"{entity_name} not found"
        if identifier:
            message += f" with identifier: {identifier}"

        return {"success": False, "data": None, "message": message, "error_code": "NOT_FOUND"}

