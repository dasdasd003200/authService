# src/core/infrastructure/web/strawberry/helpers/__init__.py
"""
Core helpers for Strawberry GraphQL - Modular structure with backward compatibility

This module exports all helper functions to maintain backward compatibility
while organizing code into specialized modules for better maintainability.
"""

# Converters
from .converters import (
    safe_uuid_str,
    safe_str,
    safe_int,
    convert_domain_enum_to_graphql,
    convert_datetime_to_iso,
)

# Validators
from .validators import (
    validate_uuid,
    validate_required,
    validate_email_format,
    validate_name,
    validate_password_strength,
)

# Execution utilities
from .execution import (
    create_success_response,
    create_error_response,
    execute_use_case,
)

# Response utilities
from .responses import (
    create_base_response_type,
    create_pagination_response,
    extract_domain_errors,
)

# Input processors
from .processors import (
    process_create_user_input,
    process_update_user_input,
    process_change_password_input,
)

# Export everything for backward compatibility
__all__ = [
    # Converters
    "safe_uuid_str",
    "safe_str",
    "safe_int",
    "convert_domain_enum_to_graphql",
    "convert_datetime_to_iso",
    # Validators
    "validate_uuid",
    "validate_required",
    "validate_email_format",
    "validate_name",
    "validate_password_strength",
    # Execution
    "create_success_response",
    "create_error_response",
    "execute_use_case",
    # Responses
    "create_base_response_type",
    "create_pagination_response",
    "extract_domain_errors",
    # Processors
    "process_create_user_input",
    "process_update_user_input",
    "process_change_password_input",
]
