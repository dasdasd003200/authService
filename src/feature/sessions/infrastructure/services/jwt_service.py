import jwt
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from uuid import UUID
from django.conf import settings

from src.core.exceptions.base_exceptions import ValidationException, UnauthorizedError
from ...domain.entities.session import Session
from ...domain.value_objects.token_type import TokenType


class JWTService:
    def __init__(self):
        self.secret_key = settings.JWT_SECRET_KEY
        self.algorithm = "HS256"

    def generate_token_pair(self, access_session: Session, refresh_session: Session, user_email: str) -> Dict[str, Any]:
        if access_session.token_type != TokenType.ACCESS:
            raise ValidationException("Invalid access session type")

        if refresh_session.token_type != TokenType.REFRESH:
            raise ValidationException("Invalid refresh session type")

        # Generate access token
        access_payload = {
            "session_id": str(access_session.id),
            "user_id": str(access_session.user_id),
            "user_email": user_email,
            "token_type": "access",
            "exp": int(access_session.expires_at.timestamp()),
            "iat": int(access_session.created_at.timestamp()),
        }
        access_token = jwt.encode(access_payload, self.secret_key, algorithm=self.algorithm)

        # Generate refresh token
        refresh_payload = {
            "session_id": str(refresh_session.id),
            "user_id": str(refresh_session.user_id),
            "token_type": "refresh",
            "exp": int(refresh_session.expires_at.timestamp()),
            "iat": int(refresh_session.created_at.timestamp()),
        }
        refresh_token = jwt.encode(refresh_payload, self.secret_key, algorithm=self.algorithm)

        # Calculate expires_in (seconds until access token expires)
        expires_in = int((access_session.expires_at - datetime.now(timezone.utc)).total_seconds())

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "expires_in": max(expires_in, 0),  # Don't return negative values
            "token_type": "Bearer",
            "session_id": str(access_session.id),
            "user_id": str(access_session.user_id),
            "user_email": user_email,
        }

    def generate_access_token(self, session: Session, user_email: str) -> Dict[str, Any]:
        if session.token_type != TokenType.ACCESS:
            raise ValidationException("Session must be ACCESS type")

        payload = {
            "session_id": str(session.id),
            "user_id": str(session.user_id),
            "user_email": user_email,
            "token_type": "access",
            "exp": int(session.expires_at.timestamp()),
            "iat": int(session.created_at.timestamp()),
        }

        access_token = jwt.encode(payload, self.secret_key, algorithm=self.algorithm)
        expires_in = int((session.expires_at - datetime.now(timezone.utc)).total_seconds())

        return {
            "access_token": access_token,
            "expires_in": max(expires_in, 0),
            "token_type": "Bearer",
            "session_id": str(session.id),
            "user_id": str(session.user_id),
            "user_email": user_email,
        }

    def decode_token(self, token: str) -> Dict[str, Any]:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except jwt.ExpiredSignatureError:
            raise UnauthorizedError("Token has expired")
        except jwt.InvalidTokenError:
            raise UnauthorizedError("Invalid token")

    def extract_session_id(self, token: str) -> UUID:
        payload = self.decode_token(token)
        session_id_str = payload.get("session_id")

        if not session_id_str:
            raise UnauthorizedError("Token does not contain session ID")

        try:
            return UUID(session_id_str)
        except ValueError:
            raise UnauthorizedError("Invalid session ID in token")

    def extract_user_id(self, token: str) -> UUID:
        payload = self.decode_token(token)
        user_id_str = payload.get("user_id")

        if not user_id_str:
            raise UnauthorizedError("Token does not contain user ID")

        try:
            return UUID(user_id_str)
        except ValueError:
            raise UnauthorizedError("Invalid user ID in token")

    def validate_token_type(self, token: str, expected_type: str) -> bool:
        payload = self.decode_token(token)
        token_type = payload.get("token_type")
        return token_type == expected_type

    def is_token_expired(self, token: str) -> bool:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            exp = payload.get("exp", 0)
            return datetime.fromtimestamp(exp, tz=timezone.utc) <= datetime.now(timezone.utc)
        except jwt.ExpiredSignatureError:
            return True
        except jwt.InvalidTokenError:
            return True
