import strawberry
from ...domain.inputs.login import LoginInput
from ...domain.inputs.refresh import RefreshTokenInput
from ...domain.inputs.logout import LogoutInput
from ...domain.inputs.find import SessionFindInput
from ...domain.inputs.find_one import SessionFindOneInput
from ...domain.types.standard_responses import LoginResponse, RefreshTokenResponse, LogoutResponse, SessionFindResponse, SessionFindOneResponse

from ...application.use_cases.session_use_cases import SessionUseCases
from src.feature.users.infrastructure.database.repositories import DjangoUserRepository
from ..database.repositories import DjangoSessionRepository
from ..services.auth_service import AuthService


@strawberry.type
class AuthResolvers:
    def __init__(self):
        self._session_repository = None
        self._user_repository = None
        self._use_cases = None
        self._service = None

    @property
    def session_repository(self):
        if self._session_repository is None:
            self._session_repository = DjangoSessionRepository()
        return self._session_repository

    @property
    def user_repository(self):
        if self._user_repository is None:
            self._user_repository = DjangoUserRepository()
        return self._user_repository

    @property
    def use_cases(self):
        if self._use_cases is None:
            self._use_cases = SessionUseCases(self.session_repository, self.user_repository)
        return self._use_cases

    @property
    def service(self):
        if self._service is None:
            self._service = AuthService(self.use_cases, self.user_repository)
        return self._service

    # ===== AUTH MUTATIONS =====
    @strawberry.mutation(name="login")
    async def login(self, input: LoginInput, info: strawberry.Info) -> LoginResponse:
        # Manejo seguro del contexto - versión simplificada
        request_info = {
            "ip_address": "127.0.0.1",  # Por ahora hardcodeado
            "user_agent": "GraphQL Client",  # Por ahora hardcodeado
        }

        # TODO: Implementar extracción real del contexto cuando sea necesario
        # try:
        #     if hasattr(info.context, 'request'):
        #         request_info["ip_address"] = info.context.request.META.get("REMOTE_ADDR", "127.0.0.1")
        #         request_info["user_agent"] = info.context.request.META.get("HTTP_USER_AGENT", "GraphQL Client")
        # except Exception:
        #     pass  # Usar valores por defecto

        return await self.service.login(input, request_info)

    @strawberry.mutation(name="refreshToken")
    async def refresh_token(self, input: RefreshTokenInput) -> RefreshTokenResponse:
        return await self.service.refresh_token(input)

    @strawberry.mutation(name="logout")
    async def logout(self, input: LogoutInput) -> LogoutResponse:
        # TODO: Extract user context from JWT token in middleware
        user_context = {}  # Will be populated by auth middleware
        return await self.service.logout(input, user_context)

    # ===== SESSION QUERIES =====
    @strawberry.field(name="sessionsFind")
    async def sessions_find(self, input: SessionFindInput) -> SessionFindResponse:
        return await self.service.find(input)

    @strawberry.field(name="sessionFindOne")
    async def session_find_one(self, input: SessionFindOneInput) -> SessionFindOneResponse:
        return await self.service.find_one(input)


# ===== SCHEMA MIXINS =====
@strawberry.type
class AuthQueries:
    @strawberry.field
    async def sessions_find(self, input: SessionFindInput) -> SessionFindResponse:
        resolver = AuthResolvers()
        return await resolver.sessions_find(input)

    @strawberry.field
    async def session_find_one(self, input: SessionFindOneInput) -> SessionFindOneResponse:
        resolver = AuthResolvers()
        return await resolver.session_find_one(input)


@strawberry.type
class AuthMutations:
    @strawberry.mutation
    async def login(self, input: LoginInput, info: strawberry.Info) -> LoginResponse:
        resolver = AuthResolvers()
        return await resolver.login(input, info)

    @strawberry.mutation
    async def refresh_token(self, input: RefreshTokenInput) -> RefreshTokenResponse:
        resolver = AuthResolvers()
        return await resolver.refresh_token(input)

    @strawberry.mutation
    async def logout(self, input: LogoutInput) -> LogoutResponse:
        resolver = AuthResolvers()
        return await resolver.logout(input)
