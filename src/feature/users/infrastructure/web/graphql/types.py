# src/feature/users/infrastructure/web/graphql/types.py
import graphene
from graphene import ObjectType, String, Boolean, DateTime, ID


class UserType(ObjectType):
    """Tipo GraphQL para Usuario"""

    id = ID(description="ID único del usuario")
    email = String(description="Email del usuario")
    first_name = String(description="Nombre del usuario")
    last_name = String(description="Apellido del usuario")
    full_name = String(description="Nombre completo del usuario")
    status = String(description="Estado del usuario")
    email_verified = Boolean(description="Email verificado")
    last_login = DateTime(description="Último login")
    failed_login_attempts = graphene.Int(description="Intentos fallidos de login")
    created_at = DateTime(description="Fecha de creación")
    updated_at = DateTime(description="Fecha de actualización")

    def resolve_full_name(self, info):
        """Resolver nombre completo"""
        if hasattr(self, "full_name"):
            return self.full_name
        return f"{self.first_name} {self.last_name}"


class UserStatusEnum(graphene.Enum):
    """Enum para estados de usuario"""

    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"
    PENDING_VERIFICATION = "pending_verification"
