from typing import Dict, Any
from dataclasses import dataclass
from src.core.domain.value_objects.email import Email
from ..value_objects.user_status import UserStatus


@dataclass
class UserFields:
    @staticmethod
    def entity_to_model_data(entity) -> Dict[str, Any]:
        return {
            "id": entity.id,
            "email": str(entity.email),
            "first_name": entity.first_name,
            "last_name": entity.last_name,
            "status": entity.status.value,
            "email_verified": entity.email_verified,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
            "is_active": entity.status == UserStatus.ACTIVE,
        }

    @staticmethod
    def model_to_entity_args(model) -> Dict[str, Any]:
        return {
            "id": model.id,
            "email": Email(model.email),
            "first_name": model.first_name,
            "last_name": model.last_name,
            "status": UserStatus.from_string(model.status),
            "email_verified": model.email_verified,
            "created_at": model.created_at,
            "updated_at": model.updated_at,
        }

    # ===== INPUT CONVERTERS =====
    @staticmethod
    def create_user_args(input_data) -> Dict[str, Any]:
        return {
            "email": input_data.email,
            "password": input_data.password,
            "first_name": input_data.first_name,
            "last_name": input_data.last_name,
            "email_verified": input_data.email_verified,
        }

    @staticmethod
    def update_user_args(input_data) -> Dict[str, Any]:
        return {
            "first_name": input_data.first_name,
            "last_name": input_data.last_name,
        }
