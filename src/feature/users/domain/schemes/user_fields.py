# src/feature/users/domain/schemes/user_fields.py - CENTRALIZED FIELDS
from typing import Dict, Any, List
from dataclasses import dataclass
from src.core.domain.value_objects.email import Email
from ..value_objects.user_status import UserStatus


@dataclass
class UserFields:
    """CENTRALIZED field definitions for User entity"""

    # BASE FIELDS from BaseEntity
    BASE_FIELDS = ["id", "created_at", "updated_at"]

    # USER-SPECIFIC FIELDS
    USER_FIELDS = ["email", "first_name", "last_name", "status", "email_verified"]

    # ALL ENTITY FIELDS
    ALL_ENTITY_FIELDS = BASE_FIELDS + USER_FIELDS

    # COMPUTED FIELDS (not stored in DB)
    COMPUTED_FIELDS = ["full_name"]

    # GRAPHQL RESPONSE FIELDS
    GRAPHQL_FIELDS = ALL_ENTITY_FIELDS + COMPUTED_FIELDS

    # MODEL EXTRA FIELDS (Django specific)
    MODEL_EXTRA_FIELDS = ["is_active"]

    # ALL MODEL FIELDS
    ALL_MODEL_FIELDS = ALL_ENTITY_FIELDS + MODEL_EXTRA_FIELDS

    @staticmethod
    def extract_entity_data(entity) -> Dict[str, Any]:
        """Extract all entity fields as dict"""
        return {
            "id": entity.id,
            "email": entity.email,
            "first_name": entity.first_name,
            "last_name": entity.last_name,
            "status": entity.status,
            "email_verified": entity.email_verified,
            "created_at": entity.created_at,
            "updated_at": entity.updated_at,
        }

    @staticmethod
    def extract_graphql_data(entity) -> Dict[str, Any]:
        """Extract all GraphQL fields as dict"""
        data = UserFields.extract_entity_data(entity)
        data.update(
            {
                "full_name": entity.full_name,
            }
        )
        return data

    @staticmethod
    def extract_model_data(entity) -> Dict[str, Any]:
        """Extract all model fields as dict"""
        data = UserFields.extract_entity_data(entity)
        data.update(
            {
                "is_active": entity.status == UserStatus.ACTIVE,
            }
        )
        return data

    @staticmethod
    def entity_constructor_args(model) -> Dict[str, Any]:
        """Get args for User entity constructor"""
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

    @staticmethod
    def create_user_args(input_data) -> Dict[str, Any]:
        """Get args for create_user use case"""
        return {
            "email": input_data.email,
            "password": input_data.password,
            "first_name": input_data.first_name,
            "last_name": input_data.last_name,
            "email_verified": input_data.email_verified,
        }

    @staticmethod
    def update_user_args(input_data) -> Dict[str, Any]:
        """Get args for update_user use case"""
        return {
            "first_name": input_data.first_name,
            "last_name": input_data.last_name,
        }
