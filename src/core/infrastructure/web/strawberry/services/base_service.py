from typing import Any, Dict
from src.core.exceptions.base_exceptions import BaseDomainException
from ..responses.response_builder import ResponseBuilder


class BaseService:
    def __init__(self, entity_name: str):
        self.entity_name = entity_name
        self.builder = ResponseBuilder()

    def handle_success_create(self, data: Any) -> Dict[str, Any]:
        return self.builder.success_data(data=data, message=f"{self.entity_name} created successfully")

    def handle_success_update(self, data: Any) -> Dict[str, Any]:
        return self.builder.success_data(data=data, message=f"{self.entity_name} updated successfully")

    def handle_success_delete(self, affected_count: int = 1) -> Dict[str, Any]:
        return self.builder.success_operation(message=f"{self.entity_name} deleted successfully", affected_count=affected_count)

    def handle_success_find(self, data: list, total_count: int) -> Dict[str, Any]:
        return self.builder.success_list(data=data, total_count=total_count, message=f"Found {len(data)} {self.entity_name.lower()}(s)")

    def handle_success_find_one(self, data: Any) -> Dict[str, Any]:
        if data is None:
            return self.builder.not_found(self.entity_name)

        return self.builder.success_data(data=data, message=f"{self.entity_name} retrieved successfully")

    def handle_exception(self, exception: BaseDomainException, data: Any = None) -> Dict[str, Any]:
        return self.builder.error_from_exception(exception, data)

    def handle_not_found(self, identifier: str = None) -> Dict[str, Any]:
        return self.builder.not_found(self.entity_name, identifier)
