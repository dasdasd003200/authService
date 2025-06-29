import jwt
from django.conf import settings
from django.contrib.auth import get_user_model
from strawberry.types import Info
from typing import Optional
from uuid import UUID

User = get_user_model()


class GraphQLAuthenticationBackend:
    """
    Backend de autenticación para GraphQL usando JWT
    """

    def authenticate_request(self, request) -> Optional[User]:
        auth_header = request.headers.get("Authorization")

        if not auth_header:
            return None

        if not auth_header.startswith("Bearer "):
            return None

        token = auth_header.split(" ")[1]

        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])

            user_id = payload.get("user_id")
            if not user_id:
                return None

            user = User.objects.get(id=UUID(user_id))
            return user

        except (jwt.InvalidTokenError, User.DoesNotExist, ValueError):
            return None


def get_authenticated_user(info: Info) -> Optional[User]:
    auth_backend = GraphQLAuthenticationBackend()
    return auth_backend.authenticate_request(info.context.request)
