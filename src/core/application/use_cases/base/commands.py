# src/core/application/use_cases/base/commands.py
"""
Common commands and queries for CRUD operations
"""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class GetEntityByIdQuery:
    """Generic query for getting entity by ID"""

    entity_id: UUID


@dataclass
class DeleteEntityCommand:
    """Generic command for deleting entity"""

    entity_id: UUID
