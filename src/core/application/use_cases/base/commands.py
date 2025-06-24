from dataclasses import dataclass
from uuid import UUID


@dataclass
class GetEntityByIdQuery:
    entity_id: UUID


@dataclass
class DeleteEntityCommand:
    entity_id: UUID
