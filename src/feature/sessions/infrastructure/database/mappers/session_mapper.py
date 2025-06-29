# src/feature/sessions/infrastructure/database/mappers/session_mapper.py
from typing import Dict, Any

from src.core.infrastructure.database.mappers.base_mapper import BaseEntityMapper
from src.feature.sessions.domain.entities.session import Session
from src.feature.sessions.infrastructure.database.models import SessionModel
from src.feature.sessions.domain.schemes.session_fields import SessionFields


class SessionEntityMapper(BaseEntityMapper[Session, SessionModel]):
    def model_to_entity(self, model: SessionModel) -> Session:
        """Convert Django Model to Entity"""
        args = SessionFields.model_to_entity_args(model)
        return Session(**args)

    def entity_to_model_data(self, session: Session) -> Dict[str, Any]:
        """Convert Entity to Django Model data"""
        data = SessionFields.entity_to_model_data(session)

        # Remove user_id from data since we'll handle the FK relationship separately
        data.pop("user_id", None)

        return data

