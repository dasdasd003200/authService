# src/core/domain/repositories/criteria/status_criteria.py
from django.db.models import QuerySet
from ..base_criteria import BaseCriteria


class StatusCriteria(BaseCriteria):
    """Generic criteria for status filtering"""

    def __init__(self, status: str, field_name: str = "status"):
        self.status = status
        self.field_name = field_name

    def apply(self, queryset: QuerySet) -> QuerySet:
        return queryset.filter(**{self.field_name: self.status})

    def to_dict(self) -> dict:
        return {
            "type": "status",
            "status": self.status,
            "field_name": self.field_name,
        }
