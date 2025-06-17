# src/feature/users/domain/repositories/user_repository.py
from abc import ABC, abstractmethod
from typing import Optional, List
from uuid import UUID

from src.core.domain.value_objects.email import Email
from src.feature.users.domain.entities.user import User
from src.core.domain.repositories.criteria.base_criteria import BaseCriteria


class UserRepository(ABC):
    """Interface del repositorio de usuarios"""

    @abstractmethod
    async def save(self, user: User) -> User:
        """Guarda o actualiza un usuario"""
        pass

    @abstractmethod
    async def find_by_id(self, user_id: UUID) -> Optional[User]:
        """Busca usuario por ID"""
        pass

    @abstractmethod
    async def find_by_email(self, email: Email) -> Optional[User]:
        """Busca usuario por email"""
        pass

    @abstractmethod
    async def exists_by_email(self, email: Email) -> bool:
        """Verifica si existe un usuario con el email"""
        pass

    @abstractmethod
    async def find_by_criteria(self, criteria: List[BaseCriteria]) -> List[User]:
        """Busca usuarios por criterios"""
        pass

    @abstractmethod
    async def delete(self, user_id: UUID) -> bool:
        """Elimina un usuario (soft delete recomendado)"""
        pass

    @abstractmethod
    async def count_by_criteria(self, criteria: List[BaseCriteria]) -> int:
        """Cuenta usuarios por criterios"""
        pass
