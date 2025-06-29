from typing import Dict, Any

from src.core.infrastructure.database.mappers.base_mapper import BaseEntityMapper
from src.feature.sessions.domain.entities.session import Session
from src.feature.sessions.infrastructure.database.models import SessionModel
from src.feature.sessions.domain.schemes.session_fields import SessionFields


class SessionEntityMapper(BaseEntityMapper[Session, SessionModel]):
    def model_to_entity(self, model: SessionModel) -> Session:
        args = SessionFields.model_to_entity_args(model)
        return Session(**args)

    def entity_to_model_data(self, session: Session) -> Dict[str, Any]:
        data = SessionFields.entity_to_model_data(session)

        data.pop("user_id", None)

        return data
