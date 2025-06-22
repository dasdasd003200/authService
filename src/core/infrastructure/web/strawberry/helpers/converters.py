# src/core/infrastructure/web/strawberry/helpers/converters.py
"""
Utilities for converting between different data types in GraphQL context
"""

from typing import Optional, Any, Type
from uuid import UUID


def safe_uuid_str(uuid_obj: Optional[UUID]) -> str:
    """Convert UUID to string safely"""
    return str(uuid_obj) if uuid_obj else ""


def safe_str(obj: Any) -> str:
    """Convert any object to string safely"""
    return str(obj) if obj is not None else ""


def safe_int(value: Any, default: int = 0) -> int:
    """Convert to int safely"""
    try:
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default


def convert_domain_enum_to_graphql(domain_value: str, graphql_enum_class) -> Any:
    """Convert domain enum value to GraphQL enum"""
    try:
        for enum_item in graphql_enum_class:
            if enum_item.value == domain_value:
                return enum_item
        return list(graphql_enum_class)[0]
    except (AttributeError, IndexError):
        return None


def convert_datetime_to_iso(dt) -> Optional[str]:
    """Convert datetime to ISO string safely"""
    return dt.isoformat() if dt else None
