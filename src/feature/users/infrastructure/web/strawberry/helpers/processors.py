from typing import Dict, Any
from src.core.infrastructure.web.strawberry.helpers.validators import validate_email_format, validate_required, validate_uuid
from .validators import validate_user_name, validate_user_password


def process_create_user_input(input_data) -> Dict[str, Any]:
    return {
        "email": validate_email_format(input_data.email),
        "password": validate_user_password(input_data.password),
        "first_name": validate_user_name(input_data.first_name, "First name"),
        "last_name": validate_user_name(input_data.last_name, "Last name"),
        "email_verified": bool(input_data.email_verified),
    }


def process_update_user_input(input_data) -> Dict[str, Any]:
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
    return {
        "user_id": validate_uuid(input_data.user_id, "User ID"),
        "new_password": validate_user_password(input_data.new_password, "New password"),
    }
