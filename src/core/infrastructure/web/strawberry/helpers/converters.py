from typing import Optional, Any, Type
from uuid import UUID


def safe_uuid_str(uuid_obj: Optional[UUID]) -> str:
    return str(uuid_obj) if uuid_obj else ""


def safe_str(obj: Any) -> str:
    return str(obj) if obj is not None else ""


def safe_int(value: Any, default: int = 0) -> int:
    try:
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default


def convert_domain_enum_to_graphql(domain_value: str, graphql_enum_class) -> Any:
    try:
        for enum_item in graphql_enum_class:
            if enum_item.value == domain_value:
                return enum_item
        return list(graphql_enum_class)[0]
    except (AttributeError, IndexError):
        return None


def convert_datetime_to_iso(dt) -> Optional[str]:
    return dt.isoformat() if dt else None
