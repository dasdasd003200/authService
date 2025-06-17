# src/core/domain/entities/base_entity.py
from abc import ABC
from datetime import datetime, timezone
from uuid import uuid4, UUID
from typing import Optional


class BaseEntity(ABC):
    """Entidad base con ID y timestamps"""

    def __init__(
        self,
        id: Optional[UUID] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None,
    ):
        self.id = id or uuid4()
        self.created_at = created_at or datetime.now(timezone.utc)
        self.updated_at = updated_at or datetime.now(timezone.utc)

    def update_timestamp(self):
        """Actualiza el timestamp de modificación"""
        self.updated_at = datetime.now(timezone.utc)

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)

