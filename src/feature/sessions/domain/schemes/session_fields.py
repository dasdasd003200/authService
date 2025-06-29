from typing import Dict, Any
from dataclasses import dataclass
from ..value_objects.token_type import TokenType
from ..value_objects.session_status import SessionStatus


@dataclass
class SessionFields:
    @staticmethod
    def entity_to_model_data(entity) -> Dict[str, Any]:
        return {
            "id": entity.id,
            "user_id": entity.user_id,
            "token_type": entity.token_type.value,
            "status": entity.status.value,
            "expires_at": entity.expires_at,
            "ip_address": entity.ip_address,
            "user_agent": entity.user_agent,
            "device_info": entity.device_info,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }

    @staticmethod
    def model_to_entity_args(model) -> Dict[str, Any]:
        return {
            "id": model.id,
            "user_id": model.user_id,
            "token_type": TokenType.from_string(model.token_type),
            "status": SessionStatus.from_string(model.status),
            "expires_at": model.expires_at,
            "ip_address": model.ip_address,
            "user_agent": model.user_agent,
            "device_info": model.device_info,
            "created_at": model.created_at,
            "updated_at": model.updated_at,
        }

    # ===== INPUT CONVERTERS =====
    @staticmethod
    def login_args(input_data) -> Dict[str, Any]:
        return {
            "email": input_data.email,
            "password": input_data.password,
            "remember_me": input_data.remember_me,
            "device_info": input_data.device_info,
        }

    @staticmethod
    def refresh_args(input_data) -> Dict[str, Any]:
        return {
            "refresh_token": input_data.refresh_token,
        }

    @staticmethod
    def logout_args(input_data) -> Dict[str, Any]:
        return {
            "session_id": input_data.session_id,
            "logout_all": input_data.logout_all,
        }
