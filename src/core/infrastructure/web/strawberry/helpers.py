# src/core/infrastructure/web/strawberry/helpers.py - COMPLETO Y CORREGIDO
"""
Core helpers - COMPLETO CON TODAS LAS FUNCIONES
"""

import asyncio
from typing import TypeVar, Callable, Any, Optional, Type
from uuid import UUID

from src.core.exceptions.base_exceptions import BaseDomainException

T = TypeVar("T")


# ===== ASYNC EXECUTION =====
# DEPRECATED: No usar handle_async_execution - usar async nativo en Strawberry


def handle_async_execution(async_func: Callable, *args, **kwargs) -> Any:
    """
    DEPRECATED: Run async functions in sync context

    WARNING: This can cause deadlocks and event loop issues.
    Use native async/await in Strawberry mutations/queries instead.
    """
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    return loop.run_until_complete(async_func(*args, **kwargs))


def safe_execute(func: Callable, default_value: Any = None) -> Any:
    """Safely execute function"""
    try:
        return func()
    except Exception:
        return default_value


# ===== RESPONSE FACTORIES =====


def create_success_response(response_class: Type[T], message: str, data: Any = None) -> T:
    """Create success response"""
    return response_class(success=True, message=message, error_code=None, data=data)


def create_error_response(response_class: Type[T], error: Exception) -> T:
    """Create error response"""
    if isinstance(error, BaseDomainException):
        return response_class(success=False, message=error.message, error_code=error.error_code, data=None)
    else:
        return response_class(success=False, message=f"Error: {str(error)}", error_code="INTERNAL_ERROR", data=None)


# ===== DECORATORS =====
# DEPRECATED: Use native async in Strawberry instead


def async_graphql_mutation(response_class: Type[T]):
    """
    DEPRECATED: Decorator for async mutations

    WARNING: Use native async/await in Strawberry instead:

    @strawberry.mutation
    async def my_mutation(self, input: MyInput) -> MyResponse:
        try:
            result = await my_use_case.execute(command)
            return MyResponse(success=True, data=result)
        except Exception as e:
            return MyResponse(success=False, message=str(e))
    """

    def decorator(async_func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            async def _execute():
                try:
                    result = await async_func(*args, **kwargs)
                    return create_success_response(response_class, "Success", result)
                except Exception as e:
                    return create_error_response(response_class, e)

            return handle_async_execution(_execute)

        return wrapper

    return decorator


def async_graphql_query(default_value: Any = None):
    """
    DEPRECATED: Decorator for async queries

    WARNING: Use native async/await in Strawberry instead:

    @strawberry.field
    async def my_query(self, id: str) -> Optional[MyType]:
        try:
            result = await my_use_case.execute(query)
            return convert_to_type(result)
        except Exception:
            return None
    """

    def decorator(async_func: Callable) -> Callable:
        def wrapper(*args, **kwargs):
            async def _execute():
                return await async_func(*args, **kwargs)

            return safe_execute(lambda: handle_async_execution(_execute), default_value)

        return wrapper

    return decorator


# ===== ENTITY CONVERTERS =====


def uuid_to_string(uuid_obj: Optional[UUID]) -> str:
    """Convert UUID to string safely"""
    return str(uuid_obj) if uuid_obj else ""


def safe_str(obj: Any) -> str:
    """Convert object to string safely"""
    return str(obj) if obj else ""


def convert_enum_to_graphql(domain_enum_value: str, graphql_enum_class):
    """Convert domain enum to GraphQL enum"""
    try:
        value_map = {item.value: item for item in graphql_enum_class}
        return value_map.get(domain_enum_value, list(graphql_enum_class)[0])
    except Exception:
        return list(graphql_enum_class)[0]


# ===== COMMON PATTERNS =====


def get_by_id_pattern(repository, entity_id: str, converter_func, entity_name: str = "Entity"):
    """
    DEPRECATED: Standard get by ID pattern

    WARNING: Use native async/await in Strawberry instead
    """

    async def _get():
        from src.core.application.use_cases.base_crud_use_cases import GetEntityByIdUseCase, GetEntityByIdQuery

        use_case = GetEntityByIdUseCase(repository, entity_name)
        query = GetEntityByIdQuery(entity_id=UUID(entity_id))
        entity = await use_case.execute(query)
        return converter_func(entity) if entity else None

    return safe_execute(lambda: handle_async_execution(_get), default_value=None)


def delete_pattern(repository, entity_id: str, response_class, entity_name: str = "Entity"):
    """
    DEPRECATED: Standard delete pattern

    WARNING: Use native async/await in Strawberry instead
    """

    async def _delete():
        from src.core.application.use_cases.base_crud_use_cases import DeleteEntityUseCase, DeleteEntityCommand

        use_case = DeleteEntityUseCase(repository, entity_name)
        command = DeleteEntityCommand(entity_id=UUID(entity_id))
        success = await use_case.execute(command)
        return success

    try:
        success = handle_async_execution(_delete)
        message = f"{entity_name} deleted successfully" if success else f"Failed to delete {entity_name.lower()}"
        return create_success_response(response_class, message, None)
    except Exception as e:
        return create_error_response(response_class, e)

