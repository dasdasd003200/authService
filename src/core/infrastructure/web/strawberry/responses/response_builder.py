from typing import Any, List as PyList
from src.core.exceptions.base_exceptions import BaseDomainException


class ResponseBuilder:
    @staticmethod
    def success_data(data: Any, message: str = None) -> dict:
        return {"success": True, "data": data, "message": message or "Operation completed successfully"}

    @staticmethod
    def success_list(data: PyList[Any], total_count: int, message: str = None) -> dict:
        return {"success": True, "data": data, "total_count": total_count, "message": message or f"Found {len(data)} items"}

    @staticmethod
    def success_operation(message: str = None, affected_count: int = None) -> dict:
        return {"success": True, "message": message or "Operation completed successfully", "affected_count": affected_count}

    @staticmethod
    def error_from_exception(exception: BaseDomainException, data: Any = None) -> dict:
        return {"success": False, "data": data, "message": exception.message, "error_code": exception.error_code}

    @staticmethod
    def error_custom(message: str, error_code: str = "OPERATION_FAILED", data: Any = None) -> dict:
        return {"success": False, "data": data, "message": message, "error_code": error_code}

    @staticmethod
    def not_found(entity_name: str, identifier: str = None) -> dict:
        message = f"{entity_name} not found"
        if identifier:
            message += f" with identifier: {identifier}"

        return {"success": False, "data": None, "message": message, "error_code": "NOT_FOUND"}
