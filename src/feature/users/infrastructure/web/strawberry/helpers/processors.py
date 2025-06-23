# src/feature/users/infrastructure/web/strawberry/helpers/processors.py
"""
Input processors específicos del feature USERS
"""

from typing import Dict, Any

# Importar validadores genéricos del core
from src.core.infrastructure.web.strawberry.helpers.validators import validate_email_format, validate_required, validate_uuid

# Importar validadores específicos de users (mismo archivo)
from .validators import validate_user_name, validate_user_password


def process_create_user_input(input_data) -> Dict[str, Any]:
    """Process and validate CreateUserInput - ESPECÍFICO DE USERS"""
    return {
        "email": validate_email_format(input_data.email),
        "password": validate_user_password(input_data.password),
        "first_name": validate_user_name(input_data.first_name, "First name"),
        "last_name": validate_user_name(input_data.last_name, "Last name"),
        "email_verified": bool(input_data.email_verified),
    }


def process_update_user_input(input_data) -> Dict[str, Any]:
    """Process and validate UpdateUserInput - ESPECÍFICO DE USERS"""
    result = {
        "user_id": validate_uuid(input_data.user_id, "User ID"),
    }

    # Optional fields
    if input_data.first_name is not None:
        result["first_name"] = validate_user_name(input_data.first_name, "First name")

    if input_data.last_name is not None:
        result["last_name"] = validate_user_name(input_data.last_name, "Last name")

    return result


def process_change_password_input(input_data) -> Dict[str, Any]:
    """Process and validate ChangePasswordInput - ESPECÍFICO DE USERS"""
    return {
        "user_id": validate_uuid(input_data.user_id, "User ID"),
        "new_password": validate_user_password(input_data.new_password, "New password"),
    }
